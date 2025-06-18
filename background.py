import cv2
import mediapipe as mp
import socket
import json
import time

# Init MediaPipe and UDP
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
blender_address = ("127.0.0.1", 9001)

# Webcam
cap = cv2.VideoCapture(0)

# FPS tracking
last_time = time.time()
frame_count = 0

while True:
    success, frame = cap.read()
    if not success:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    ih, iw, _ = frame.shape

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0].landmark

        # Use key facial landmarks to calculate center
        center_points = [face[i] for i in [1, 33, 263, 168, 199]]  # nose tip, eye corners, forehead
        cx = sum([pt.x for pt in center_points]) / len(center_points)
        cy = sum([pt.y for pt in center_points]) / len(center_points)
        cz = sum([pt.z for pt in center_points]) / len(center_points)

        # Send to Blender
        head_pos = {'x': cx, 'y': cy, 'z': cz}
        sock.sendto(json.dumps(head_pos).encode(), blender_address)

        # Draw face bounding box
        xs = [int(pt.x * iw) for pt in face]
        ys = [int(pt.y * ih) for pt in face]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Padding
        pad = 20
        cv2.rectangle(frame, (min_x - pad, min_y - pad), (max_x + pad, max_y + pad), (0, 255, 0), 2)
        cv2.putText(frame, "HEAD TRACKED", (min_x, min_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # FPS overlay
    frame_count += 1
    now = time.time()
    if now - last_time >= 1.0:
        fps = frame_count / (now - last_time)
        frame_count = 0
        last_time = now
    else:
        fps = None

    if fps:
        cv2.putText(frame, f"{fps:.1f} FPS", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("Head Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
