from flask import Flask, Response
from picamera2 import Picamera2
import cv2


# http://remote-control.local:5001/video_feed

app = Flask(__name__)

# Initialize Picamera2
picam2 = Picamera2()
picam2.start()

def generate_frames():
    while True:
        # Capture frame-by-frame from Picamera2 as a numpy array
        frame = picam2.capture_array()

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Stream the frame as part of a multipart response (MJPEG format)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the specific media type (mime type)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Run the Flask app and listen on all network interfaces (host='0.0.0.0')
    app.run(host='0.0.0.0', port=5001)
