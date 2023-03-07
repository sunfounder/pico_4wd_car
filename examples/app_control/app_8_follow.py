'''
This example adds the P widget for follow hand.
D & J widgets for display sonar work.
'''

import time
import motors as car
from ws import WS_Server
from machine import Pin
import sonar as sonar
import sys

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

# follow
FOLLOW_SCAN_ANGLE = 90
FOLLOW_SCAN_STEP = 5
FOLLOW_REFERENCE = 20 # distance referenece (m)
FOLLOW_FORWARD_POWER = 20
FOLLOW_TURNING_POWER = 15

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

'''----------------- follow ---------------------'''
def follow():
    global sonar_angle, sonar_distance

    sonar.set_sonar_scan_config(FOLLOW_SCAN_ANGLE, FOLLOW_SCAN_STEP)
    sonar.set_sonar_reference(FOLLOW_REFERENCE)

    #--------- scan -----------
    sonar_angle, sonar_distance, sonar_data = sonar.sonar_scan()
    # time.sleep(0.02)

    # If sonar data return a int, means scan not finished, and the int is current angle status
    if isinstance(sonar_data, int):
        return

    #---- analysis direction -----
    direction = get_dir(sonar_data, split_str='1')

    #--------- move ------------
    if direction == "left":
        car.move("left", FOLLOW_TURNING_POWER)
    elif direction == "right":
        car.move("right", FOLLOW_TURNING_POWER)
    elif direction == "forward":
        car.move("forward", FOLLOW_FORWARD_POWER)
    else:
        car.move("stop")

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
    if 'P' in data.keys() and data['P'] == True:
        if mode != 'follow':
            mode = 'follow'
            print(f"change mode to: {mode}")
    else:
        if mode != None:
            mode = None
            print(f"change mode to: {mode}")
    

def remote_handler():

    ''' follow hand '''
    if mode == 'follow':
        follow()       

    ''' no operation '''
    if mode == None:
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
    sys.print_exception(e)
    print(e)
finally:
    onboard_led.off()       
    car.move("stop")