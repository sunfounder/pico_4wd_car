from servo import Servo
from ultrasonic import Ultrasonic
import time

servo = Servo(18)
ultrasonic = Ultrasonic(6, 7)

sonar_angle = 0
sonar_step = 30

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
    sonar_angle += sonar_step
    if sonar_angle >= 90:
        sonar_angle = 90
        sonar_step *= -1
    elif sonar_angle <= -90:
        sonar_angle = -90
        sonar_step *= -1

while True:
    sonar_move()
    distance = get_distance_at(sonar_angle)
    print("angle: ",sonar_angle, "   distance: ",distance)
    time.sleep(0.3)