This project is a real-time fire detection system built with Python and OpenCV. It uses computer vision techniques to identify fire or flame patterns from live webcam footage. Ideal for smart surveillance, safety monitoring, and early fire warning systems.
📸 Demo
Fire Detection Demo
🚀 Features
- 🔍 Real-time fire detection from webcam feed
- 📦 Lightweight and easy to deploy
- 🎯 HSV-based color filtering for flame detection
- 🧠 Contour detection to highlight fire zones
- 🛠️ Easy to integrate with alert systems (e.g., alarms, notifications)
🧰 Technologies Used
- Python 3.x
- OpenCV (cv2)
- NumPy
📦 Installation
- Clone the repository:
git clone https://github.com/yourusername/fire-detection-opencv.git
cd fire-detection-opencv
- Install dependencies:
pip install -r requirements.txt
- Run the script:
python fire_detection.py


⚙️ How It Works
- Captures video frames from the webcam.
- Converts frames to HSV color space.
- Applies color thresholding to isolate fire-like regions.
- Uses contour detection to identify and highlight fire zones.
- Displays bounding boxes around detected fire areas in real time.




