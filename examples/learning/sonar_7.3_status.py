from servo import Servo
from ultrasonic import Ultrasonic
import time

servo = Servo(18)
ultrasonic = Ultrasonic(6, 7)

sonar_angle = 0
sonar_step = 30

SONAR_MAX_ANGLE = 90
SONAR_MIN_ANGLE = -90
SONAR_REFERENCE = 20

sonar_data =[]
for i in range((SONAR_MAX_ANGLE-SONAR_MIN_ANGLE)/sonar_step+1):
    sonar_data.append(None)

def get_distance_at(angle):
    global sonar_angle
    sonar_angle = angle
    servo.set_angle(sonar_angle)
    #time.sleep(0.04)
    distance = ultrasonic.get_distance()
    if distance < 0:
        return -1
    else:
        return distance

def sonar_move():
    global sonar_angle, sonar_step
    if sonar_angle >= SONAR_MAX_ANGLE:
        sonar_angle = SONAR_MAX_ANGLE
        sonar_step = -abs(sonar_step)
    elif sonar_angle <= SONAR_MIN_ANGLE:
        sonar_angle = SONAR_MIN_ANGLE
        sonar_step = abs(sonar_step)
    sonar_angle += sonar_step

def get_sonar_status(distance):
    if distance > SONAR_REFERENCE or distance < 0:
        return 1
    else:
        return 0

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sonar_scan():
    global sonar_data
    sonar_move()
    distance = get_distance_at(sonar_angle)
    index= int(mapping(sonar_angle, SONAR_MIN_ANGLE, SONAR_MAX_ANGLE, 0, len(sonar_data)-1))
    status=get_sonar_status(distance)
    sonar_data[index]=status
    return sonar_data

while True:
    print(sonar_scan())
    time.sleep(0.1)