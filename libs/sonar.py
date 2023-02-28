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
    index=int(mapping(sonar_angle, SONAR_MIN_ANGLE, SONAR_MAX_ANGLE, 0, len(sonar_data)-1))
    status=get_sonar_status(distance)
    sonar_data[index]=status
    if (index == 0 or index == len(sonar_data)-1) and None not in sonar_data:
        return sonar_angle,distance,sonar_data
    else:
        return sonar_angle,distance,status

def set_sonar_scan_config(scan_range=None,step=None):
    global SONAR_MAX_ANGLE, SONAR_MIN_ANGLE, sonar_angle, sonar_step, sonar_data
    
    # update changed
    item = 0
    if scan_range is None or scan_range is SONAR_MAX_ANGLE-SONAR_MIN_ANGLE:
        item+=1
    else:
        SONAR_MAX_ANGLE = int(scan_range / 2)
        SONAR_MIN_ANGLE = SONAR_MAX_ANGLE-scan_range
    if step is None or abs(sonar_step) is abs(step):
        item+=1
    else:
        sonar_step=int(step)
    if item is 2: # if nothing change, return
        return
    
    # re-create the data list
    sonar_data =[]
    for i in range(scan_range/abs(sonar_step) +1):
        sonar_data.append(None)
    
    sonar_angle=0
    servo.set_angle(sonar_angle)

def set_sonar_reference(ref):
    global SONAR_REFERENCE
    SONAR_REFERENCE = int(ref)


if __name__ == '__main__':
    try:
        set_sonar_scan_config(180,30)
        set_sonar_reference(20)
        while True:
            _,_,status = sonar_scan()
            if type(status) is not int:
                print(status)
            time.sleep(0.1)
    finally:
        servo.set_angle(0)
