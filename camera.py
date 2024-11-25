import cv2
import mediapipe as mp
import os
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

save_dir = "asl_frames"
os.makedirs(save_dir, exist_ok=True)

# mediapipe hands model
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)


cap = cv2.VideoCapture(0)
# keep track of how many frames captured
frame_count = 0
last_saved_time = time.time()
capture_interval = 0.5 # in seconds

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # convert the frame to RGB 
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # draw hand landmarks on the frame if hand is found
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        current = time.time()
        # saves every [capture_interval] amount of seconds
        if current - last_saved_time >= capture_interval: 
            frame_path = os.path.join(save_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"Saved {frame_path}")
            frame_count += 1
            last_saved_time = current

    cv2.imshow('Hand Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
