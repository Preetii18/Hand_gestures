import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_number(hand_landmarks):
    """Detect the number shown by the hand gesture."""
    finger_tips = [8, 12, 16, 20]  # Index, middle, ring, pinky fingertips
    finger_bases = [6, 10, 14, 18]  # Corresponding base joints

    # Check if fingers are open
    fingers_open = []
    for tip, base in zip(finger_tips, finger_bases):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
            fingers_open.append(True)  # Finger is open
        else:
            fingers_open.append(False)  # Finger is closed

    # Thumb detection (robust across positions)
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    thumb_mcp = hand_landmarks.landmark[2]
    wrist = hand_landmarks.landmark[0]

    if thumb_tip.x > thumb_ip.x:  # Thumb is open (relative to hand orientation)
        thumb_open = True
    else:
        thumb_open = False

    # Map conditions to numbers
    if all(not f for f in fingers_open) and not thumb_open:
        return "Zero"
    elif fingers_open == [True, False, False, False] and not thumb_open:
        return "One"
    elif fingers_open == [True, True, False, False] and not thumb_open:
        return "Two"
    elif fingers_open == [True, True, True, False] and not thumb_open:
        return "Three"
    elif fingers_open == [True, True, True, True] and not thumb_open:
        return "Four"
    elif all(fingers_open) and thumb_open:
        return "Five"
    else:
        return "Unknown"

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Flip the frame for a selfie view
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect number
                number = detect_number(hand_landmarks)
                print(f"Detected: {number}")
                cv2.putText(frame, f"Detected: {number}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
