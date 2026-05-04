"""
Driver Drowsiness Detection using OpenCV + MediaPipe (STRICT CLOSED-EYE LOGIC)

Install:
    pip install opencv-python mediapipe numpy

Controls:
    - Press 'q' to quit.
"""

from collections import deque
import math
import cv2
import mediapipe as mp
import numpy as np
import winsound


# 🔥 TUNE THESE
FULLY_CLOSED_EAR = 0.18   # lower = stricter (0.16–0.20 range)
DROWSY_FRAMES = 18        # frames before alert
EAR_SMOOTHING_WINDOW = 5  # smoothing


# Eye landmark indices
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]


def dist(a, b):
    return math.dist(a, b)


def compute_ear(eye):
    v1 = dist(eye[1], eye[5])
    v2 = dist(eye[2], eye[4])
    h = dist(eye[0], eye[3])
    return (v1 + v2) / (2.0 * h) if h != 0 else 0


def to_pixel(lm, w, h):
    return (int(lm.x * w), int(lm.y * h))


def get_eye_points(face, idxs, w, h):
    return [to_pixel(face.landmark[i], w, h) for i in idxs]


def draw_eye(frame, pts):
    for p in pts:
        cv2.circle(frame, p, 2, (0, 255, 255), -1)
    cv2.polylines(frame, [np.array(pts)], True, (0, 255, 255), 1)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not working")
        return

    counter = 0
    alarm_on = False
    ear_history = deque(maxlen=EAR_SMOOTHING_WINDOW)

    mp_face_mesh = mp.solutions.face_mesh

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = mesh.process(rgb)

            status = "AWAKE"
            color = (0, 255, 0)
            ear_val = None

            if result.multi_face_landmarks:
                face = result.multi_face_landmarks[0]

                left = get_eye_points(face, LEFT_EYE_IDX, w, h)
                right = get_eye_points(face, RIGHT_EYE_IDX, w, h)

                draw_eye(frame, left)
                draw_eye(frame, right)

                ear = (compute_ear(left) + compute_ear(right)) / 2.0
                ear_history.append(ear)
                ear_val = sum(ear_history) / len(ear_history)

                # 🔥 STRICT CLOSED EYE LOGIC
                if ear_val < FULLY_CLOSED_EAR:
                    counter += 1
                else:
                    counter = 0
                    alarm_on = False

                if counter >= DROWSY_FRAMES:
                    status = "DROWSY"
                    color = (0, 0, 255)

                    if not alarm_on:
                        winsound.Beep(2500, 700)
                        alarm_on = True

                    cv2.putText(frame, "DROWSINESS ALERT!",
                                (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (0, 0, 255), 3)

            else:
                status = "NO FACE"
                color = (0, 255, 255)
                counter = 0
                alarm_on = False
                ear_history.clear()

            # UI
            cv2.putText(frame, f"Status: {status}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, color, 2)

            if ear_val:
                cv2.putText(frame, f"EAR: {ear_val:.3f}",
                            (20, 120), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 2)

            cv2.putText(frame, f"Counter: {counter}",
                        (20, 155), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), 2)

            cv2.imshow("EyeSentinel", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
