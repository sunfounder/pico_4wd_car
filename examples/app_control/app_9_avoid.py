'''
This example adds the P widget for follow hand.
D & J widgets for display sonar work.
'''

import time
import motors as car
from ws import WS_Server
from machine import Pin
import sonar as sonar

'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
WIFI_MODE = "ap"
SSID = "" # your wifi name, if blank, use the set name "NAME"
PASSWORD = "12345678" # your password

'''------------ Global Variables -------------'''

# sonar
sonar_angle = 0
sonar_distance = 0

# obstacle_avoid
avoid_proc = "scan" # obstacle process, "scan", "getdir", "stop", "forward", "left", "right"
avoid_has_obstacle = False

# obstacle_avoid
OBSTACLE_AVOID_SCAN_ANGLE = 60
OBSTACLE_AVOID_SCAN_STEP = 10
OBSTACLE_AVOID_REFERENCE = 25   # distance referenece (cm)
OBSTACLE_AVOID_FORWARD_POWER = 30
OBSTACLE_AVOID_TURNING_POWER = 50

# enable drive function # cliff / avoid / follow / line track
mode = None


'''------------ Instantiate -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
onboard_led = Pin(25, Pin.OUT) 


'''------- get_dir (sonar sacn data to direction) ---------------------'''
def get_dir(sonar_data, split_str="0"):
    # get scan status of 0, 1
    sonar_data = [str(i) for i in sonar_data]
    sonar_data = "".join(sonar_data)

    # Split 0, leaves the free path
    paths = sonar_data.split(split_str)

    # Calculate where is the widest
    max_paths = max(paths)
    if split_str == "0" and len(max_paths) < 4:
        return "left"
    elif split_str == "1" and len(max_paths) < 2:
        return "stop"

    # Calculate the direction of the widest
    pos = sonar_data.index(max_paths)
    pos += (len(max_paths) - 1) / 2
    delta = len(sonar_data) / 3
    if pos < delta:
        return "left"
    elif pos > 2 * delta:
        return "right"
    else:
        return "forward"

'''----------------- obstacle_avoid ---------------------'''
def obstacle_avoid():
    global sonar_angle, sonar_distance, avoid_proc, avoid_has_obstacle

    # scan
    if avoid_proc == 'scan':
        if not avoid_has_obstacle:
            sonar.set_sonar_scan_config(OBSTACLE_AVOID_SCAN_ANGLE, OBSTACLE_AVOID_SCAN_STEP)
            car.move('forward', OBSTACLE_AVOID_FORWARD_POWER)
        else:
            sonar.set_sonar_scan_config(180, OBSTACLE_AVOID_SCAN_STEP)
            car.move('stop')
        sonar_angle, sonar_distance, sonar_data = sonar.sonar_scan()
        if isinstance(sonar_data, int):
            # 0 means distance too close, 1 means distance safety
            if sonar_data == 0:
                avoid_has_obstacle = True
                return
            else:
                return
        else:
            avoid_proc = 'getdir'

    # getdir
    if avoid_proc == 'getdir':
        avoid_proc = get_dir(sonar_data)
    # move: stop, forward
    if avoid_proc == 'stop':
        avoid_has_obstacle = True
        car.move('stop')
        avoid_proc = 'scan'
    elif avoid_proc == 'forward':
        avoid_has_obstacle = False
        car.move('forward', OBSTACLE_AVOID_FORWARD_POWER)
        avoid_proc = 'scan'
    elif avoid_proc == 'left' or avoid_proc == 'right':
        avoid_has_obstacle = True
        if avoid_proc == 'left':
            car.move('left', OBSTACLE_AVOID_TURNING_POWER)
            sonar_angle = 20 # servo turn right 20 
        else:
            car.move('right', OBSTACLE_AVOID_TURNING_POWER)
            sonar_angle = -20 # servo turn left 20 
        sonar.servo.set_angle(sonar_angle)
        time.sleep(0.2)
        avoid_proc = 'turn'

    # turn: left, right
    if avoid_proc == 'turn':
        sonar_distance = sonar.get_distance_at(sonar_angle)
        status = sonar.get_sonar_status(sonar_distance)
        if status == 1:
            avoid_has_obstacle = False
            avoid_proc = 'scan'
            car.move("forward", OBSTACLE_AVOID_FORWARD_POWER)
            sonar.servo.set_angle(0)

'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):
    global mode

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        return
    
    ''' data to display'''
    # # sonar and distance
    ws.send_dict['D'] = [sonar_angle, sonar_distance]
    ws.send_dict['J'] = sonar_distance   

    # mode select:
    if 'O' in data.keys() and data['O'] == True:
        if mode != 'obstacle avoid':
            mode = 'obstacle avoid'
            sonar.set_sonar_reference(OBSTACLE_AVOID_REFERENCE)
            print(f"change mode to: {mode}")
    else:
        if mode != None:
            mode = None
            print(f"change mode to: {mode}")
    

def remote_handler():

    ''' enable avoid function '''
    if mode == 'obstacle avoid':
        obstacle_avoid()      
    
    ''' no operation '''
    if mode is None:
        car.move('stop')


'''----------------- main ---------------------'''
   
try:
   car.move('stop')
   ws.on_receive = on_receive
   if ws.start():
        onboard_led.on()
        while True:
            ws.loop()
            remote_handler() 
except Exception as e:
    print(e)
finally:
    onboard_led.off()       
    car.move("stop")