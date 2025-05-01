from flask import Flask, render_template, Response, g
import cv2
import sqlite3
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from main import process_frame

app = Flask(__name__)
DB_PATH = 'data/threat_logs.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            processed_frame = process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT timestamp, threat_type, description, latitude, longitude FROM threats ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    return render_template('live_and_logs.html', logs=logs)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def logs():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT timestamp, threat_type, description, latitude, longitude FROM threats ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    return render_template('logs.html', logs=logs)

@app.route('/api/logs')
def api_logs():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT timestamp, threat_type, description, latitude, longitude FROM threats ORDER BY timestamp DESC LIMIT 50')
    logs = cursor.fetchall()
    logs_list = []
    for log in logs:
        logs_list.append({
            'timestamp': log[0],
            'threat_type': log[1],
            'description': log[2],
            'latitude': log[3] if log[3] else 'N/A',
            'longitude': log[4] if log[4] else 'N/A'
        })
    from flask import jsonify
    return jsonify(logs_list)

if __name__ == '__main__':
    app.run(debug=True)
