import io
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)

def process(videoPath):
    cap = cv2.VideoCapture(videoPath)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    frame_count = 0
    saved_count = 0
    while ret:
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Blur to reduce noise
        gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
        gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)

        # Compute difference
        diff = cv2.absdiff(gray1, gray2)

        # Threshold
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Dilate to fill gaps
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours (motion areas)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Adjust sensitivity
                motion_detected = True
                break

        if motion_detected:
            cv2.imwrite(f"{UPLOAD_FOLDER}/frame_{frame_count}.jpg", frame1)
            saved_count += 1

        frame1 = frame2
        ret, frame2 = cap.read()
        frame_count += 1

    cap.release()


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    process(filepath)

    return send_file(
        filepath,
        as_attachment=True,
        download_name="returnFile",
        mimetype="video/mp4"
    )

@app.route('/')
def start():
    return render_template('Index.html')

@app.route('/Index.html')
def home():
    return render_template('Index.html')

@app.route('/downloadGuide.html')
def about():
    return render_template('downloadGuide.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)