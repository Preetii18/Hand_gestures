# ✋ Hand Gesture Recognition (0–5)

## 📌 Objective
Developed a real-time system to detect hand gestures (0–5) using webcam input and map them to corresponding digits.

## 🛠️ Tools Used
- Python
- OpenCV
- MediaPipe
- NumPy

## ⚙️ How It Works
1. Captures webcam input  
2. Detects 21 hand landmarks using MediaPipe  
3. Counts raised fingers to determine digits 0–5  
4. Displays the digit on the video feed in real-time

## 💻 Installation

```bash
# 1. Create virtual environment
python -m venv env

# 2. Activate the environment
env\Scripts\activate  # On Windows
# source env/bin/activate  # On Linux/macOS

# 3. Install dependencies
pip install opencv-python mediapipe numpy

# 4. Run the project
python hand_detect.py
