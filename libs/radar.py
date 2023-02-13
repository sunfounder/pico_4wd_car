from servo import Servo
from ultrasonic import Ultrasonic
import time

servo = Servo(18)
sonar = Ultrasonic(6, 7)

radar_data = []
RADAR_REFERENCE = 20
RADAR_MAX_ANGLE = 90
RADAR_MIN_ANGLE = -90
RADAR_STEP_ANGLE = 10
radar_step = -RADAR_STEP_ANGLE
radar_angle = 0
radar_scan_angle = 180

def get_radar_distance_at(angle):
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = sonar.get_distance()
    return distance

def get_radar_distance():
    global radar_angle, radar_step
    radar_angle += radar_step
    if radar_angle >= RADAR_MAX_ANGLE:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -RADAR_STEP_ANGLE
    elif radar_angle <= RADAR_MIN_ANGLE:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = RADAR_STEP_ANGLE
    distance = get_radar_distance_at(radar_angle)
    return [radar_angle, distance]

def set_radar_scan_angle(angle):
    global RADAR_MAX_ANGLE, RADAR_MIN_ANGLE, radar_angle, radar_step, radar_scan_angle
    if radar_scan_angle == angle:
        return
    radar_scan_angle = angle
    RADAR_MAX_ANGLE = int(angle / 2)
    RADAR_MIN_ANGLE = -RADAR_MAX_ANGLE
    if radar_step < 0:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = RADAR_STEP_ANGLE
    else:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -RADAR_STEP_ANGLE
    servo.set_angle(radar_angle)

def get_radar_status(distance):
    if distance > RADAR_REFERENCE:
        return 1
    else:
        return 0

def radar_scan():
    global radar_data
    angle, distance = get_radar_distance()
    status = get_radar_status(distance)

    radar_data.append(status)
    if angle == RADAR_MIN_ANGLE or angle == RADAR_MAX_ANGLE:
        if radar_step < 0:
            # print("reverse")
            radar_data.reverse()
        # print(radar_data)
        tmp = radar_data.copy()
        radar_data = []
        return angle, distance, tmp
    else:
        return angle, distance, status

