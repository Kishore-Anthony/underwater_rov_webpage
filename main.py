from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import threading

app = Flask(__name__)
net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')
classes = []
with open('yolov4.names', 'r') as f:
    classes = f.read().strip().split('\n')
confidence_threshold = 0.5

# Initialize dimensions with default values
desired_width = 1200
desired_height = 675

stop_event = threading.Event()

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

@app.route('/start_radar', methods=['POST'])
def start_radar():
    global stop_event
    stop_event.clear()
    threading.Thread(target=run_radar, args=(stop_event,)).start()
    return jsonify({'status': 'Radar started'})

@app.route('/stop_radar', methods=['POST'])
def stop_radar():
    global stop_event
    stop_event.set()
    return jsonify({'status': 'Radar stopped'})

def run_radar(stop_event):
    import pygame
    import serial
    import os
    import math

    GREEN = (0, 255, 0)
    DORG = (0, 100, 0)
    DARR = (100, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)  # Define blue color

    def calcPoints(radius, angle):
        x = math.cos(math.radians(angle)) * radius
        y = math.sin(math.radians(angle)) * radius
        return (x, y)

    pygame.init()

    size = (900, 700)
    gameDisplay = pygame.display.set_mode(size)
    pygame.display.set_caption("ALBATROSS")

    ser = None
    try:
        ser = serial.Serial('COM8', 9600)
    except serial.SerialException as e:
        print("Error: Serial port connection failed.")
        print(e)
        os.system('pause')
        quit()

    listoflines = [((50, 600), (850, 600))]
    for i in range(12):
        j = i + 1
        ang = j * 15
        x, y = calcPoints(400, ang)
        listoflines.append(((450 - x, 600 - y), (450, 600)))

    listofgreen = []
    listofred = []

    # Font initialization
    font = pygame.font.Font(None, 24)

    def draw(pos, distance):
        gameDisplay.fill((0, 0, 0))

        for line in listoflines:
            pygame.draw.line(gameDisplay, GREEN, line[0], line[1])

        for line in listofgreen:
            pygame.draw.line(gameDisplay, DORG, line[0], line[1])
            line[2] -= 1
            if line[2] < 0:
                listofgreen.remove(line)

        for line in listofred:
            pygame.draw.line(gameDisplay, DARR, line[0], line[1])
            line[2] -= 1
            if line[2] < 0:
                listofred.remove(line)

        x1, y1 = calcPoints(400, pos - 2)
        x2, y2 = calcPoints(400, pos + 2)

        radar_color = BLUE
        if distance < 50:
            radar_color = GREEN
        elif 50 <= distance < 100:
            radar_color = WHITE
        elif 100 <= distance < 150:
            radar_color = BLUE
        elif 150 <= distance < 200:
            radar_color = YELLOW
        else:
            radar_color = RED

        pygame.draw.line(gameDisplay, GREEN, (450, 600), (450 - x2, 600 - y2))
        pygame.draw.line(gameDisplay, radar_color, (450 - x1, 600 - y1), (450 - x2, 600 - y2))

        listofgreen.append([(450, 600), (450 - x2, 600 - y2), 360])
        listofred.append([(450 - x1, 600 - y1), (450 - x2, 600 - y2), 360])

        # Draw obstacle as colored dot
        pygame.draw.circle(gameDisplay, radar_color, (int(450 - x2), int(600 - y2)), 5)

        # Render distance and angle text
        distance_text = font.render(f"Distance: {distance} cm", True, GREEN)
        angle_text = font.render(f"Angle: {pos} degrees", True, RED)
        gameDisplay.blit(distance_text, (10, 10))
        gameDisplay.blit(angle_text, (10, 40))

    quit_game = False
    while not quit_game and not stop_event.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

        if ser and ser.is_open:
            rawdata = ser.readline().decode('utf-8').strip().split(' ')
            if len(rawdata) == 2:
                try:
                    distance = int(rawdata[0])
                    pos = int(rawdata[1])
                    draw(pos, distance)
                    pygame.display.update()
                except ValueError:
                    print("Error: Invalid data received from serial port.")
        else:
            print("Error: Serial port is not open.")
            quit_game = True

    pygame.quit()
    if ser:
        ser.close()

if __name__ == '__main__':
    app.run(debug=True)
