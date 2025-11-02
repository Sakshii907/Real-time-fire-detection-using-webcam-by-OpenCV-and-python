"""
Fire Color Debug Tool
Click on the flame to see its HSV values
This helps adjust detection ranges
"""

import cv2
import numpy as np

# Global variable to store clicked position
clicked_point = None

def mouse_callback(event, x, y, flags, param):
    """Capture mouse clicks to check HSV values"""
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)

print("=" * 60)
print("FIRE COLOR DEBUG TOOL")
print("=" * 60)
print("Instructions:")
print("1. Light a flame (candle, lighter, match)")
print("2. Hold it in front of camera")
print("3. CLICK on the flame in the video")
print("4. You'll see the HSV values of that pixel")
print("5. Press 'q' to quit")
print("=" * 60)

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot access webcam!")
    exit()

# Create window and set mouse callback
cv2.namedWindow("Debug - Click on Flame")
cv2.setMouseCallback("Debug - Click on Flame", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Draw crosshair at clicked point
    if clicked_point:
        x, y = clicked_point
        
        # Get HSV values at clicked point
        h, s, v = hsv[y, x]
        
        # Draw crosshair
        cv2.line(frame, (x-20, y), (x+20, y), (0, 255, 0), 2)
        cv2.line(frame, (x, y-20), (x, y+20), (0, 255, 0), 2)
        
        # Display HSV values
        text = f"HSV: H={h} S={s} V={v}"
        cv2.putText(frame, text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Print to console
        print(f"Clicked pixel HSV: H={h}, S={s}, V={v}")
        
        # Show suggested ranges
        lower_h = max(0, h - 10)
        upper_h = min(180, h + 10)
        lower_s = max(0, s - 50)
        upper_s = 255
        lower_v = max(0, v - 50)
        upper_v = 255
        
        suggestion = f"Try: [{lower_h}, {lower_s}, {lower_v}] to [{upper_h}, {upper_s}, {upper_v}]"
        cv2.putText(frame, suggestion, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Instructions on screen
    cv2.putText(frame, "Click on flame to see HSV values", (10, frame.shape[0] - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow("Debug - Click on Flame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nDebug tool closed.")
print("Use the HSV values shown to adjust your fire detection ranges!")