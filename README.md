# Handy - Virtual Mouse
The Power of Mouse at your Fingertips! 

## What is this project?

Handy is a Python application that transforms hand gestures into mouse actions. Using your webcam, it detects hand movements in real-time and translates them into corresponding mouse movements, clicks, and scrolls. It's an innovative, interactive, and fun way to navigate your computer.

## What does it do?

The application uses your webcam to track your hand movements and translates them into mouse actions. Here's what you can do:

- Move your index finger to move the cursor.
- Bring your index and middle fingers close together to perform a left click.
- Bring your ring and pinky fingers close together to perform a right click.
- Move your thumb away from your index finger to scroll.
- Bring all fingers close together to stop the program.

## Dependencies and Versions

The project uses the following Python libraries:

| Library | Version | Purpose |
| --- | --- | --- |
| OpenCV (cv2) | 4.5.3 | Image and video processing |
| MediaPipe | 0.8.7.1 | Hand landmarks detection |
| PyAutoGUI | 0.9.53 | Automating mouse movements and clicks |
| PyQt5 | 5.15.4 | Creating the GUI |

## Tech Stack

The project is entirely written in Python, using the following packages:

- **OpenCV (cv2)**: Used for capturing video from the webcam, flipping the video frames, and drawing on the frames.
- **MediaPipe**: Used for detecting the hand and its landmarks in each video frame.
- **PyAutoGUI**: Used for controlling the mouse based on the position of the hand landmarks.
- **PyQt5**: Used for creating the GUI of the application, which includes start and stop buttons, an instructions button, and an image label to display the video from the webcam.

## How to Run Handy on Your Personal Computer

Follow these steps to get Handy up and running on your machine:

1. **Clone the Repository**: First, clone the Handy repository from GitHub to your local machine. You can do this by running the following command in your terminal:

   ```
   git clone https://github.com/singhtejpreet2004/Virtual-Mouse-App
   ```†

2. **Navigate to the Project Directory**: Use the `cd` command to navigate into the `Virtual-Mouse-App` directory:

   ```
   cd Virtual-Mouse-App
   ```

3. **Install Dependencies**: Handy requires several Python libraries to run. Install them using pip:

   ```
   pip install opencv-python mediapipe pyautogui PyQt5
   ```

4. **Run the Script**: Finally, you can run the Handy script with the following command:

   ```
   python handy.py
   ```

   This will start the application.

5. **Use the Application**: In the application window, click the 'Start' button to start tracking your hand movements. Move your hand in front of your webcam to control the mouse. To stop the application, bring all your fingers close together or click the 'Stop' button in the application window.

And that's it! You're now controlling your mouse with your hand movements. Enjoy using Handy!


## Contributing

Feel free to use and edit this project as you see fit. If you find any errors or see any room for improvement, please let me know. I appreciate any and all feedback.

And if you find this project useful, don't forget to give it an upvote! Your support means a lot. Happy coding!
