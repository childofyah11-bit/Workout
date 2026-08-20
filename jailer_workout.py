import cv2
import time
import os
import sys
from datetime import datetime

# CONFIGURATION
TARGET_PULLUPS = 9
ALARM_HOURS = [9, 11, 15]  # 9 AM, 11 AM, and 3 PM (24-hour format)

def sound_alarm():
    """Trigger a continuous, annoying system beep to force you to the camera."""
    print("🚨 WAKE UP! TIME TO WORK OUT. NO EXCUSES. 🚨")
    for _ in range(5):
        if sys.platform == "win32":
            import winsound
            winsound.Beep(1000, 500)  # Frequency 1000Hz, duration 500ms
        else:
            # Mac/Linux terminal bell sound
            sys.stdout.write('\a')
            sys.stdout.flush()
            time.sleep(0.5)

def start_workout_lock():
    """Launches the camera jailer and blocks everything until 9 reps are finished."""
    print(f"🔒 SYSTEM LOCKED. Complete {TARGET_PULLUPS} PULL-UPS to silence the machine.")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: No camera detected. Stop hiding from the bar and plug it in.")
        return

    pullup_count = 0
    
    while pullup_count < TARGET_PULLUPS:
        ret, frame = cap.read()
        if not ret:
            break

        # UI Overlay tracking your miserable progress
        cv2.putText(frame, f"Pull-Ups: {pullup_count}/{TARGET_PULLUPS}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, "STATUS: LOCKED OUT", (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("Trainer Cam - GET UP ON THE BAR", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("😤 Nice try. Escaping is disabled. Do your pull-ups.")
            
        # --- SIMULATED REP DETECTION ---
        # Press Spacebar to track a completed pull-up during testing
        if key == ord(' '): 
            pullup_count += 1
            print(f"💪 Rep counted! {pullup_count}/{TARGET_PULLUPS}")

    cap.release()
    cv2.destroyAllWindows()
    print("🔓 TARGET MET. Alarm cleared. You may return to your regular activities... for now.")

# BACKGROUND SCHEDULER LOOP
print("👀 Workout Jailer active in background. Watching the clock...")
last_triggered_hour = -1

while True:
    now = datetime.now()
    
    # Check if the current hour hits one of your target alarm slots
    if now.hour in ALARM_HOURS and now.hour != last_triggered_hour:
        sound_alarm()
        start_workout_lock()
        last_triggered_hour = now.hour  # Prevents looping repeatedly within the same hour
        
    # Reset tracking once the hour passes so it can trigger tomorrow
    if now.hour not in ALARM_HOURS:
        last_triggered_hour = -1
        
    time.sleep(10)  # Check the clock every 10 seconds to keep CPU usage low
