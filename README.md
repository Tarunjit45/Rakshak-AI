# Real-Time Threat Detection System

This project is a real-time threat detection system using AI technologies. It captures video input, performs object detection and facial recognition, sends real-time alerts, displays live feed with detected threats, and logs detected events with timestamps and geolocation.

## Features

- Video capture from live webcam feed or recorded video using OpenCV
- Object detection using YOLOv5 (weapons, vehicles, suspicious objects)
- Facial recognition using DeepFace to detect known suspects
- Real-time alerts via Telegram bot
- Live feed display with bounding boxes and labels
- Logging of detected threats with timestamps and geolocation (if available)
- Flask web interface to view live feed and logs
- SQLite database for logging data

## Project Structure

- `/data` - Store video files and data
- `/models` - Store trained models
- `/scripts` - Main processing scripts
- `/webapp` - Flask web interface

## Installation

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Configure the Telegram bot token and chat ID in `scripts/config.py`
2. Run the main detection script:

```
python scripts/main.py
```

3. Run the Flask web interface:

```
python webapp/app.py
```

4. Access the web interface at `http://localhost:5000`

## Notes

- Ensure you have a webcam connected or provide a video file path in the configuration.
- The system logs detected threats with timestamps and geolocation (if available).
- Customize the object detection and facial recognition models as needed.
