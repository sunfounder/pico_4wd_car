from servo import Servo
from ultrasonic import Ultrasonic
import time

servo = Servo(18)
ultrasonic = Ultrasonic(6, 7)

sonar_angle = 0 # current angle
sonar_step = 30 # Scan angle for each step

sonar_MAX_ANGLE = 90
sonar_MIN_ANGLE = -90

sonar_data =[]
for i in range((sonar_MAX_ANGLE-sonar_MIN_ANGLE)/sonar_step+1):
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
    if sonar_angle >= sonar_MAX_ANGLE:
        sonar_angle = sonar_MAX_ANGLE
        sonar_step = -abs(sonar_step)
    elif sonar_angle <= sonar_MIN_ANGLE:
        sonar_angle = sonar_MIN_ANGLE
        sonar_step = abs(sonar_step)
    sonar_angle += sonar_step

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sonar_scan():
    global sonar_data
    sonar_move()
    distance = get_distance_at(sonar_angle)
    index= int(mapping(sonar_angle, sonar_MIN_ANGLE, sonar_MAX_ANGLE, 0, len(sonar_data)-1))
    sonar_data[index]=distance
    return sonar_data

while True:
    print(sonar_scan())
    time.sleep(0.3)
