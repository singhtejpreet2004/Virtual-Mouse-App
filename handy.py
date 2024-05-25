import cv2
import mediapipe as mp
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QImage, QPixmap

class VirtualMouseThread(QThread):
    stop_signal = pyqtSignal()
    change_pixmap_signal = pyqtSignal(QPixmap)

    def run(self):
        # Initialize video capture and hand detector
        cap = cv2.VideoCapture(0)
        hand_detector = mp.solutions.hands.Hands()
        drawing_utils = mp.solutions.drawing_utils
        screen_width, screen_height = pyautogui.size()

        index_y = 0
        thumb_y = 0
        middle_y = 0
        ring_y = 0
        pinky_y = 0

        while True:
            # Capture frame and flip it
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)

            # Get dimensions and convert frame color
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame with hand detector
            output = hand_detector.process(rgb_frame)
            hands = output.multi_hand_landmarks

            if hands:
                for hand in hands:
                    # Draw landmarks and connections on the frame
                    drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

                    # Draw bounding box and label for the hand
                    x_min = min(landmark.x for landmark in hand.landmark)
                    y_min = min(landmark.y for landmark in hand.landmark)
                    x_max = max(landmark.x for landmark in hand.landmark)
                    y_max = max(landmark.y for landmark in hand.landmark)
                    cv2.rectangle(frame, (int(x_min * frame_width), int(y_min * frame_height)),
                                  (int(x_max * frame_width), int(y_max * frame_height)), (0, 255, 0), 2)
                    # Get the landmarks
                    landmarks = hand.landmark

                    # Iterate over each landmark to get the finger tip coordinates
                    for id, landmark in enumerate(landmarks):
                        x = int(landmark.x * frame_width)
                        y = int(landmark.y * frame_height)

                        # Identify finger tips and perform actions
                        if id == 8:  # Index finger tip
                            index_x = screen_width / frame_width * x
                            index_y = screen_height / frame_height * y

                        if id == 4:  # Thumb tip
                            thumb_x = screen_width / frame_width * x
                            thumb_y = screen_height / frame_height * y

                            # Calculate distance between index finger and thumb
                            distance = abs(index_y - thumb_y)

                            # Scroll action if distance is greater than 100 pixels
                            if distance > 100:
                                pyautogui.scroll(-distance)  # Negative value for upward scroll
                                pyautogui.sleep(0.1)  # Optional: Pause execution to see the scroll effect
                                print("Scrolling")

                            # Move cursor to index finger position if closer than 100 pixels
                            elif distance <= 100:
                                pyautogui.moveTo(index_x, index_y)
                                print("Moving cursor")

                        if id == 12:  # Middle finger tip
                            middle_x = screen_width / frame_width * x
                            middle_y = screen_height / frame_height * y

                        if id == 16:  # Ring finger tip
                            ring_x = screen_width / frame_width * x
                            ring_y = screen_height / frame_height * y

                        if id == 20:  # Pinky finger tip
                            pinky_x = screen_width / frame_width * x
                            pinky_y = screen_height / frame_height * y

                    # Calculate distances between fingers
                    distance_index_middle = abs(index_y - middle_y)
                    distance_middle_ring = abs(middle_y - ring_y)
                    distance_ring_pinky = abs(ring_y - pinky_y)

                    # Left click action if index and middle fingers are close together
                    if distance_index_middle < 50:
                        pyautogui.click(button='left')
                        print("Left click")

                    # Right click action if ring and pinky fingers are close together
                    if distance_ring_pinky < 50:
                        pyautogui.click(button='right')
                        print("Right click")

                    # If all fingers are close together, stop the program
                    if distance_index_middle < 50 and distance_middle_ring < 50 and distance_ring_pinky < 50:
                        self.stop_signal.emit()
                        print("Stopping program")
                        return

            # Convert the image from OpenCV BGR format to QImage
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            self.change_pixmap_signal.emit(QPixmap.fromImage(p))

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

class VirtualMouseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Handy - Virtual Mouse")
        self.setGeometry(100, 100, 300, 200)

        widget = QWidget()
        layout = QVBoxLayout()

        # Welcome label
        welcome_label = QLabel("Welcome to Handy!\n The Mouse at Your Fingertips")
        welcome_label.setFont(QFont("Helvetica", 16))
        layout.addWidget(welcome_label)

        # Instructions button
        self.instructions_button = QPushButton("Instructions")
        self.instructions_button.clicked.connect(self.show_instructions)
        layout.addWidget(self.instructions_button)

        # Start and stop buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        layout.addWidget(self.stop_button)

        # Image label
        self.image_label = QLabel(self)
        self.image_label.resize(640, 480)
        layout.addWidget(self.image_label)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.thread = VirtualMouseThread()
        self.thread.stop_signal.connect(self.stop)
        self.thread.change_pixmap_signal.connect(self.update_image)

    def show_instructions(self):
        instructions = [
            "1. Place your hand in front of the camera",
            "2. Move your index finger to move the cursor",
            "3. Bring your index and middle fingers close together to left click",
            "4. Bring your ring and pinky fingers close together to right click",
            "5. Move your thumb away from your index finger to scroll",
            "6. Bring all fingers close together to stop the program"
        ]

        QMessageBox.information(self, "Instructions", "\n".join(instructions))

    def start(self):
        if not self.thread.isRunning():
            self.thread.start()

    def stop(self):
        if self.thread.isRunning():
            self.thread.terminate()

    def update_image(self, pixmap):
        self.image_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication([])
    window = VirtualMouseApp()
    window.show()
    app.exec_()