import cv2
import mediapipe as mp
import os
import time

# Initialize Mediapipe and Drawing utilities
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Initialize the hands model
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
)

# Prompt the user for the ASL sign label
label = input("Enter the label for the ASL sign (e.g., 'A', 'B', 'hello'): ").strip()

# Create a directory for the label
save_dir = os.path.join("asl_dataset", label)
os.makedirs(save_dir, exist_ok=True)

# Start video capture
cap = cv2.VideoCapture(0)

frame_count = 0
last_saved_time = time.time()
capture_interval = 0.5  # seconds

print(f"Collecting data for '{label}'. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Convert the image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Draw hand landmarks and save frames
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

        current_time = time.time()
        if current_time - last_saved_time >= capture_interval:
            frame_path = os.path.join(save_dir, f"{label}_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"Saved {frame_path}")
            frame_count += 1
            last_saved_time = current_time

    # Display the frame
    cv2.imshow('Data Collection - Press "q" to quit', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
