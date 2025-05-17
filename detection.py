# detection.py
from ultralytics import YOLO
import cv2
import json
import paho.mqtt.publish as publish

# Φορτώνει το YOLOv8n μοντέλο από τον φάκελο models/
model = YOLO('models/yolov8n.pt')

# Ανοίγει την web-κάμερα (0)
cap = cv2.VideoCapture(0)

drone_id = 1  # αν έχεις πολλαπλά drones, άλλαζε αυτό το ID

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Εκτελεί ανίχνευση
    results = model(frame)[0]

    # Μετατρέπει τα αποτελέσματα σε JSON-friendly μορφή
    detections = []
    for x1, y1, x2, y2, score, cls in results.boxes.data.tolist():
        detections.append({
            'class': int(cls),
            'score': float(score),
            'bbox': [int(x1), int(y1), int(x2), int(y2)]
        })

    # Δημοσιεύει σε topic swarm/detections
    payload = json.dumps({
        'drone_id': drone_id,
        'detections': detections
    })
    publish.single('swarm/detections', payload, hostname='localhost')

    # Εμφανίζει για οπτικό έλεγχο
    annotated = results.plot()
    cv2.imshow('Detections', annotated)
    if cv2.waitKey(1) == 27:  # ESC για έξοδο
        break

cap.release()
cv2.destroyAllWindows()
