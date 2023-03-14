'''
This example adds the M widget for cliff detect.
"A" widget for display greyscale work.
'''

import time
import motors as car
from ws import WS_Server
from machine import Pin
from grayscale import Grayscale
import sys

'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
WIFI_MODE = "ap"
SSID = "" # your wifi name, if blank, use the set name "NAME"
PASSWORD = "12345678" # your password

'''------------ Global Variables -------------'''
# car move - D-pad & throttle
dpad_touched = False      
throttle_power = 0
steer_power = 0
steer_sensitivity = 0.8 # 0 ~ 1

# enable drive function # cliff / avoid / follow / line track
mode = None

'''Configure grayscale module'''
GRAYSCALE_LINE_REFERENCE_DEFAULT = 10000
GRAYSCALE_CLIFF_REFERENCE_DEFAULT = 2000

'''------------ Instantiate -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
onboard_led = Pin(25, Pin.OUT) 
grayscale = Grayscale(26, 27, 28)


'''----------------- motors fuctions ---------------------'''
def my_car_move(throttle_power, steer_power, gradually=False):
    power_l = 0
    power_r = 0

    if steer_power < 0:
        power_l = int((100 + 2*steer_sensitivity*steer_power)/100*throttle_power)
        power_r = int(throttle_power)
    else:
        power_l = int(throttle_power)
        power_r = int((100 - 2*steer_sensitivity*steer_power)/100*throttle_power)

    if gradually:
        car.set_motors_power_gradually([power_l, power_r, power_l, power_r])
    else:
        car.set_motors_power([power_l, power_r, power_l, power_r])


'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):
    global throttle_power, steer_power, dpad_touched
    global mode

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        return


    ''' data to display'''
    # greyscale
    ws.send_dict['A'] = grayscale.get_value()

    ''' remote control'''
    # Move - power
    if 'Q' in data.keys() and isinstance(data['Q'], int):
        throttle_power = data['Q']
    else:
        throttle_power = 0

    # Move - direction
    if 'K' in data.keys():
        #print(data['K'])
        if data['K'] == "left":
            dpad_touched = True
            if steer_power > 0:
                steer_power = 0
            steer_power -= int(throttle_power/2)
            if steer_power < -100:
                steer_power = -100
        elif data['K'] == "right":
            dpad_touched = True
            if steer_power < 0:
                steer_power = 0
            steer_power += int(throttle_power/2)
            if steer_power > 100:
                steer_power = 100
        elif data['K'] == "forward":
            dpad_touched = True
            steer_power = 0
        elif data['K'] == "backward":
            dpad_touched = True
            steer_power = 0
            throttle_power = -throttle_power
        else:
            dpad_touched = False
            steer_power = 0

    # grayscale reference
    if 'A' in data.keys() and isinstance(data['A'], list):
        grayscale.set_edge_reference(data['A'][0])
        grayscale.set_line_reference(data['A'][1])
    else:
        grayscale.set_edge_reference(GRAYSCALE_CLIFF_REFERENCE_DEFAULT)
        grayscale.set_line_reference(GRAYSCALE_LINE_REFERENCE_DEFAULT)


    # mode select:
    if 'M' in data.keys() and data['M'] == True:
        if mode != 'anti fall':
            mode = 'anti fall'
            print(f"change mode to: {mode}")
    else:
        if mode != None:
            mode = None
            print(f"change mode to: {mode}")
    

def remote_handler():
    global throttle_power, steer_power, dpad_touched

    ''' move && anti-fall '''
    if mode == "anti fall":
        if grayscale.is_on_edge():
            if dpad_touched and throttle_power<0: # only for backward
                my_car_move(throttle_power, steer_power, gradually=True)
            else:
                car.move("stop")
        else:
            if dpad_touched:
                my_car_move(throttle_power, steer_power, gradually=True)
            else:
                car.move("stop")                
    elif dpad_touched:
        my_car_move(throttle_power, steer_power, gradually=True)

    ''' no operation '''
    if not dpad_touched:
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