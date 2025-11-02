"""
Camera-Based Fire Detection System
Detects fire/flames using webcam and color analysis
Press 'q' to quit
"""

import cv2
import numpy as np
from datetime import datetime
import threading
import time

class FireDetector:
    def __init__(self):
        self.fire_detected = False
        self.alarm_active = False
        self.frame_count = 0
        self.detection_count = 0
        self.confidence_threshold = 3
        
    def detect_fire(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_fire1 = np.array([0, 50, 50])      # Lower thresholds
        upper_fire1 = np.array([25, 255, 255])   # Wider range

        lower_fire2 = np.array([25, 50, 50])     # Lower thresholds  
        upper_fire2 = np.array([40, 255, 255])   # Wider range
        
        mask1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
        mask2 = cv2.inRange(hsv, lower_fire2, upper_fire2)
        
        fire_mask = cv2.bitwise_or(mask1, mask2)
        
        kernel = np.ones((5, 5), np.uint8)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        fire_detected = False
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area > 500:
                fire_detected = True
                
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                
                cv2.putText(frame, "FIRE DETECTED!", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        return fire_detected, frame, fire_mask
    
    def sound_alarm(self):
        while self.alarm_active:
            try:
                import winsound
                winsound.Beep(1000, 500)
                time.sleep(0.5)
            except:
                print("\a🔥 FIRE ALERT! 🔥")
                time.sleep(0.5)
    
    def run(self):
        print("=" * 50)
        print("FIRE DETECTION SYSTEM - STARTING")
        print("=" * 50)
        print("Press 'q' to quit")
        print("Accessing webcam...")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("ERROR: Cannot access webcam!")
            print("Make sure no other application is using the camera.")
            return
        
        print("Webcam active. Monitoring for fire...")
        print("=" * 50)
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("ERROR: Cannot read from webcam!")
                break
            
            self.frame_count += 1
            
            fire_detected, processed_frame, fire_mask = self.detect_fire(frame)
            
            if fire_detected:
                self.detection_count += 1
            else:
                self.detection_count = 0
            
            if self.detection_count >= self.confidence_threshold:
                self.fire_detected = True
                
                if not self.alarm_active:
                    self.alarm_active = True
                    alarm_thread = threading.Thread(target=self.sound_alarm)
                    alarm_thread.daemon = True
                    alarm_thread.start()
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n🔥 FIRE ALERT! - {timestamp}")
                
            else:
                self.fire_detected = False
                self.alarm_active = False
            
            status_text = "STATUS: FIRE DETECTED!" if self.fire_detected else "STATUS: Normal"
            status_color = (0, 0, 255) if self.fire_detected else (0, 255, 0)
            
            cv2.putText(processed_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            cv2.putText(processed_frame, timestamp, (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            confidence = min(self.detection_count / self.confidence_threshold * 100, 100)
            cv2.putText(processed_frame, f"Confidence: {confidence:.0f}%", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("Fire Detection - Main View", processed_frame)
            cv2.imshow("Fire Detection - Mask View", fire_mask)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nStopping fire detection system...")
                break
        
        self.alarm_active = False
        cap.release()
        cv2.destroyAllWindows()
        print("Fire detection system stopped.")
        print("=" * 50)

if __name__ == "__main__":
    detector = FireDetector()
    detector.run()