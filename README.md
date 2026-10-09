# 🛡️ Rakshak AI — Autonomous Real-Time Threat Detection & Defense System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLOv5](https://img.shields.io/badge/Vision-YOLOv5-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)](https://github.com/ultralytics/yolov5)
[![DeepFace](https://img.shields.io/badge/Facial_Recognition-DeepFace-FF6F00?style=for-the-badge)](https://github.com/serengil/deepface)
[![Telegram](https://img.shields.io/badge/Alerts-Telegram%20Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org)
[![Flask](https://img.shields.io/badge/Dashboard-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Rakshak AI** (*रक्षक* — The Protector) is an end-to-end autonomous security and surveillance system. Integrating **YOLOv5 object detection**, **DeepFace facial recognition**, and an **automated Telegram emergency dispatch bot**, Rakshak AI monitors video streams in real time, logs threat events in a local SQLite database, and instantly alerts security personnel with incident snapshots and GPS geolocation.

---

## 📌 Threat Detection & Alert Pipeline

```
[ Video Feed / IP Camera / CCTV ]
               |
               v
+-------------------------------------------------------------+
|                 OpenCV Video Frame Ingestion                |
+-------------------------------------------------------------+
               |
               +----------------------------+
               |                            |
               v                            v
+-----------------------------+ +-----------------------------+
|     YOLOv5 Threat Model     | |    DeepFace Recognition     |
|   (`yolov5s.pt` Detection)  | |  Facial identity matching   |
|   Weapons, Intruders, Gear  | |   & known blacklist check   |
+-----------------------------+ +-----------------------------+
               |                            |
               +--------------+-------------+
                              |
                              v  (Threat Detected?)
+-------------------------------------------------------------+
|                  Threat Verification Engine                 |
|       - Logs incident to SQLite Database                    |
|       - Updates cumulative `threat_count.txt`               |
|       - GeoPy resolves GPS coordinates                      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 Automated Telegram Bot Dispatch             |
|   Sends high-priority photo alert + timestamp + coordinates |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                   Flask Web Dashboard (`webapp/`)           |
|        Real-time telemetry, threat stats & live feeds       |
+-------------------------------------------------------------+
```

---

## ✨ Core Features

* 👁️ **Multi-Threat Classification:** Leverages PyTorch YOLOv5 (`yolov5s.pt`) for identifying weapons, unauthorized intruders, and abnormal activity.
* 👤 **Facial Identification:** DeepFace integration checks detected faces against a local database of authorized personnel vs. unknown subjects.
* 📲 **Instant Telegram Incident Dispatch:** Sends instantaneous photo snapshots of the intrusion and geocoded location to designated Telegram chat IDs.
* 📊 **Local SQLite Audit Trail:** Complete audit trail of past security incidents.
* 🌐 **Web Dashboard:** Clean Flask-powered web interface for security monitoring.

---

## 📁 Repository Structure

```text
Rakshak-AI/
├── yolov5s.pt            # Pre-trained YOLOv5 weights
├── threat_count.txt      # Real-time incident counter
├── requirements.txt      # Dependencies (torch, deepface, opencv, telegram, flask)
├── scripts/
│   └── main.py           # Core surveillance engine, detection loop & Telegram dispatcher
├── webapp/               # Flask surveillance dashboard
├── data/                 # Local SQLite database & reference face datasets
├── LICENSE               # MIT License
└── README.md
```

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and install requirements:

```bash
git clone https://github.com/Tarunjit45/Rakshak-AI.git
cd Rakshak-AI

pip install -r requirements.txt
```

### 2. Configure Telegram Bot
Open `scripts/main.py` and supply your Telegram Bot Token and Chat ID:

```python
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
```

### 3. Run the Detection Engine
```bash
python scripts/main.py
```

### 4. Run the Web Dashboard
```bash
python webapp/app.py
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
