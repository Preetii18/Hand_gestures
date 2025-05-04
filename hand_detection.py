import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Example: Get fingertip coordinates
            landmarks = hand_landmarks.landmark
            fingertip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            print(f"Index Finger Tip: {fingertip.x}, {fingertip.y}")

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


def count_raised_fingers(landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Landmark indices for fingertips
    finger_bases = [3, 6, 10, 14, 18]  # Landmark indices for finger bases
    
    count = 0
    for tip, base in zip(finger_tips, finger_bases):
        if landmarks[tip].y < landmarks[base].y:  # Tip is above base
            count += 1
    return count

cv2.putText(frame, f"Number: {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

