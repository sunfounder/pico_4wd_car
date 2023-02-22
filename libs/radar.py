from servo import Servo
from ultrasonic import Ultrasonic
import time

servo = Servo(18)
sonar = Ultrasonic(6, 7)

radar_angle = 0
radar_step = 30

RADAR_MAX_ANGLE = 90
RADAR_MIN_ANGLE = -90
RADAR_REFERENCE = 20

radar_data =[]
for i in range((RADAR_MAX_ANGLE-RADAR_MIN_ANGLE)/radar_step+1):
    radar_data.append(None)

def get_distance_at(angle):
    global radar_angle
    radar_angle = angle
    servo.set_angle(radar_angle)
    #time.sleep(0.04)
    while True: # avoid negative invalid values
        distance = sonar.get_distance()
        if distance > 0:
            return distance
    
def radar_move():
    global radar_angle, radar_step
    if radar_angle >= RADAR_MAX_ANGLE:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -abs(radar_step)
    elif radar_angle <= RADAR_MIN_ANGLE:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = abs(radar_step)
    radar_angle += radar_step

def get_radar_status(distance):
    if distance > RADAR_REFERENCE:
        return 1
    else:
        return 0

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def radar_scan():
    global radar_data
    radar_move()
    distance = get_distance_at(radar_angle)
    index=int(mapping(radar_angle, RADAR_MIN_ANGLE, RADAR_MAX_ANGLE, 0, len(radar_data)-1))
    status=get_radar_status(distance)
    radar_data[index]=status
    if (index == 0 or index == len(radar_data)-1) and None not in radar_data:
        return radar_angle,distance,radar_data
    else:
        return radar_angle,distance,status

def set_radar_scan_config(scan_range=None,step=None):
    global RADAR_MAX_ANGLE, RADAR_MIN_ANGLE, radar_angle, radar_step, radar_data
    
    # update changed
    item = 0
    if scan_range is None or scan_range is RADAR_MAX_ANGLE-RADAR_MIN_ANGLE:
        item+=1
    else:
        RADAR_MAX_ANGLE = int(scan_range / 2)
        RADAR_MIN_ANGLE = RADAR_MAX_ANGLE-scan_range
    if step is None or abs(radar_step) is abs(step):
        item+=1
    else:
        radar_step=int(step)
    if item is 2: # if nothing change, return
        return
    
    # re-create the data list
    radar_data =[]
    for i in range(scan_range/abs(radar_step) +1):
        radar_data.append(None)
    
    radar_angle=0
    servo.set_angle(radar_angle)

def set_radar_reference(ref):
    global RADAR_REFERENCE
    RADAR_REFERENCE = int(ref)


if __name__ == '__main__':
    try:
        set_radar_scan_config(180,30)
        set_radar_reference(20)
        while True:
            _,_,status = radar_scan()
            if type(status) is not int:
                print(status)
            time.sleep(0.1)
    finally:
        servo.set_angle(0)
