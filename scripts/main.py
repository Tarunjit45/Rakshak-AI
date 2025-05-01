import cv2
import torch
import sqlite3
import time
import threading
from deepface import DeepFace
from geopy.geocoders import Nominatim
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime

# Configuration
VIDEO_SOURCE = 0  # 0 for webcam, or path to video file
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'
DB_PATH = 'data/threat_logs.db'
ALERT_COOLDOWN = 30  # seconds between alerts for the same threat

# Load YOLOv5 model (pretrained or custom trained for weapons, vehicles, suspicious objects)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Initialize geolocator
geolocator = Nominatim(user_agent="threat_detection_app")

# Threat alert cooldown tracking
last_alert_time = {}

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            threat_type TEXT,
            description TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

# Log threat to database
def log_threat(threat_type, description, latitude=None, longitude=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute('''
        INSERT INTO threats (timestamp, threat_type, description, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, threat_type, description, latitude, longitude))
    conn.commit()
    conn.close()

# Send alert via Telegram
def send_telegram_alert(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Telegram error: {e}")

# Get geolocation (latitude, longitude) - placeholder for actual GPS integration
def get_geolocation():
    # For demo, return None or fixed coordinates
    return None, None

# Process frame for object detection and facial recognition
def process_frame(frame):
    global last_alert_time

    # Object detection with YOLOv5
    results = model(frame)

    # Parse detections
    detections = results.pandas().xyxy[0]

    print("Detections:")
    threat_detected = False
    alert_messages = []
    for _, row in detections.iterrows():
        label = row['name']
        confidence = row['confidence']
        print(f"Label: {label}, Confidence: {confidence:.2f}")
        if label in ['person', 'car', 'truck', 'knife', 'gun']:  # example threat labels
            threat_detected = True
            bbox = (int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']))
            alert_msg = f"Threat detected: {label} with confidence {confidence:.2f}"
            alert_messages.append((alert_msg, bbox, label))

    # Facial recognition with DeepFace
    try:
        faces = DeepFace.extract_faces(frame, detector_backend='opencv')
        for face in faces:
            # For demo, assume all faces are unknown
            # In real use, compare with known suspects database
            threat_detected = True
            alert_msg = "Known suspect detected"
            alert_messages.append((alert_msg, face['facial_area'], 'face'))
    except Exception as e:
        print(f"DeepFace error: {e}")

    # Send alerts and log threats
    if threat_detected:
        lat, lon = get_geolocation()
        for msg, bbox, label in alert_messages:
            now = time.time()
            if msg not in last_alert_time or (now - last_alert_time[msg]) > ALERT_COOLDOWN:
                send_telegram_alert(msg)
                log_threat(label, msg, lat, lon)
                last_alert_time[msg] = now

    # Draw bounding boxes and labels on frame
    for _, row in detections.iterrows():
        label = row['name']
        if label in ['person', 'car', 'truck', 'knife', 'gun']:
            xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Draw face bounding boxes
    for msg, bbox, label in alert_messages:
        if label == 'face':
            x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, msg, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return frame

# Video capture and processing loop
def video_loop():
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)

        cv2.imshow('Threat Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    init_db()
    video_loop()
