# Sign Language Detector

A real-time hand gesture recognition system built with Python and MediaPipe that translates hand gestures into words and speaks them aloud.

## Demo

Point your hand at the camera and watch it recognize your gestures in real time.

## Features

- Real-time hand gesture detection via webcam
- Upload and process pre-recorded videos
- Text-to-speech that speaks the detected sentence out loud
- Clean dark-themed GUI built with Tkinter
- Stability threshold to avoid flickering detections

## Supported Gestures

| Gesture | Meaning |
|--------|---------|
| All fingers open | Hi |
| All fingers closed | No |
| Index + Pinky | Rock It |
| Thumb only | Thumbs Up |
| Index only | Wait |
| Index + Middle | What's Up |
| Index + Middle + Ring + Pinky | Four |
| Index + Middle + Ring | Good |

## Tech Stack

- Python
- OpenCV
- MediaPipe
- Tkinter
- Pillow
- pyttsx3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/izhaan-mubeen/Sign-Language-Detector.git
cd Sign-Language-Detector
```

2. Install required libraries:
```bash
pip install opencv-python mediapipe pillow pyttsx3
```

3. Run the application:
```bash
python main.py
```

## How to Use

1. Launch the app
2. Choose Start Camera for live detection or Upload Video for a recorded file
3. Show your hand gestures to the camera
4. Watch words appear in real time
5. Click Speak Sentence to hear the detected words spoken aloud
6. Click Stop to end the session

## Author

Izhaan Mubeen
Mechatronics and Control Engineer
GitHub: https://github.com/izhaan-mubeen
