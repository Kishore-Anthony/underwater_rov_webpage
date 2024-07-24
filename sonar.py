from flask import Flask, render_template, Response
import pygame
import serial
import os
import math
import io
from PIL import Image

app = Flask(__name__)

# Initialize Pygame and serial connection
pygame.init()

size = (900, 700)
gameDisplay = pygame.Surface(size)
pygame.display.set_caption("ALBATROSS")

ser = None
try:
    ser = serial.Serial('COM8', 9600)
    print("Serial connection established.")
except serial.SerialException as e:
    print("Error: Serial port connection failed.")
    print(e)

# Colors and points calculation
GREEN = (0, 255, 0)
DORG = (0, 100, 0)
DARR = (100, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

def calcPoints(radius, angle):
    x = math.cos(math.radians(angle)) * radius
    y = math.sin(math.radians(angle)) * radius
    return (x, y)

listoflines = [((50, 600), (850, 600))]
for i in range(12):
    j = i + 1
    ang = j * 15
    x, y = calcPoints(400, ang)
    listoflines.append(((450 - x, 600 - y), (450, 600)))

listofgreen = []
listofred = []

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

    max_distance = 200
    scale_factor = 2

    if distance > max_distance:
        distance = max_distance

    x1, y1 = calcPoints(400, 180 - pos)
    x2, y2 = calcPoints(distance * scale_factor, 180 - pos)

    if 100 <= distance < 150:
        radar_color = WHITE
    elif 150 <= distance < 200:
        radar_color = YELLOW
    else:
        radar_color = RED

    pygame.draw.line(gameDisplay, GREEN, (450, 600), (450 - x2, 600 - y2))
    pygame.draw.line(gameDisplay, radar_color, (450 - x1, 600 - y1), (450 - x2, 600 - y2))

    listofgreen.append([(450, 600), (450 - x2, 600 - y2), 360])
    listofred.append([(450 - x1, 600 - y1), (450 - x2, 600 - y2), 360])

    pygame.draw.circle(gameDisplay, radar_color, (int(450 - x2), int(600 - y2)), 5)

    distance_text = font.render(f"Distance: {distance} cm", True, GREEN)
    angle_text = font.render(f"Angle: {pos} degrees", True, RED)
    gameDisplay.blit(distance_text, (10, 10))
    gameDisplay.blit(angle_text, (10, 40))

def generate():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        if ser and ser.is_open:
            try:
                rawdata = ser.readline().decode('utf-8').strip().split(' ')
                print(f"Raw data received: {rawdata}")
                if len(rawdata) == 2:
                    distance = int(rawdata[0])
                    pos = int(rawdata[1])
                    print(f"Distance: {distance}, Position: {pos}")
                    draw(pos, distance)

                    pygame.display.update()
                    image_str = pygame.image.tostring(gameDisplay, 'RGB')
                    image = Image.frombytes('RGB', size, image_str)
                    img_io = io.BytesIO()
                    image.save(img_io, 'JPEG')
                    img_io.seek(0)
                    frame = img_io.getvalue()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except ValueError as e:
                print("Error: Invalid data received from serial port.")
                print(e)
            except serial.SerialException as e:
                print("Error: Serial port reading failed.")
                print(e)
        else:
            # If the serial port is not open, yield a blank frame
            gameDisplay.fill((0, 0, 0))
            pygame.display.update()
            image_str = pygame.image.tostring(gameDisplay, 'RGB')
            image = Image.frombytes('RGB', size, image_str)
            img_io = io.BytesIO()
            image.save(img_io, 'JPEG')
            img_io.seek(0)
            frame = img_io.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/sonar_video_feed')
def sonar_video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        if ser:
            ser.close()
        pygame.quit()
