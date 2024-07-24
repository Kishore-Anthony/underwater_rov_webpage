from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)
net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')
classes = []
with open('yolov4.names', 'r') as f:
    classes = f.read().strip().split('\n')
confidence_threshold = 0.5

# Initialize dimensions with default values
desired_width = 800
desired_height = 600


@app.route('/')
def index():
    return render_template('index.html')


def detect_objects():
    global desired_width, desired_height
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (desired_width, desired_height))
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layer_names = net.getUnconnectedOutLayersNames()
        detections = net.forward(layer_names)
        frame_copy = frame.copy()
        for detection in detections:
            for object_detection in detection:
                scores = object_detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confidence_threshold:
                    if 0 <= class_id < len(classes):
                        class_name = classes[class_id]
                        center_x = int(object_detection[0] * desired_width)
                        center_y = int(object_detection[1] * desired_height)
                        width = int(object_detection[2] * desired_width)
                        height = int(object_detection[3] * desired_height)
                        x = int(center_x - width / 2)
                        y = int(center_y - height / 2)
                        if class_name == 'person':
                            cv2.rectangle(frame_copy, (x, y), (x + width, y + height), (0, 255, 0), 2)
                            cv2.putText(frame_copy, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame_copy)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
