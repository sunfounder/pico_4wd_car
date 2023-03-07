
'''
This example adds the N widget for line track.
"A" widget for display greyscale work.
'''

import time
import motors as car
from ws import WS_Server
from machine import Pin
from grayscale import Grayscale

'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
WIFI_MODE = "ap"
SSID = "" # your wifi name, if blank, use the set name "NAME"
PASSWORD = "12345678" # your password

# line track
line_out_time = 0

# enable drive function # cliff / avoid / follow / line track
mode = None

'''Configure the power of the line_track mode'''
LINE_TRACK_POWER = 80

'''Configure grayscale module'''
GRAYSCALE_LINE_REFERENCE_DEFAULT = 10000
GRAYSCALE_CLIFF_REFERENCE_DEFAULT = 2000

'''------------ Instantiate -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
onboard_led = Pin(25, Pin.OUT) 
grayscale = Grayscale(26, 27, 28)


'''----------------- line_track ---------------------'''
def line_track():
    global line_out_time
    _power = LINE_TRACK_POWER
    gs_data = grayscale.get_line_status()
    #print(f"gs_data: {gs_data}, {grayscale.line_ref}")

    if gs_data == [0, 0, 0] or gs_data == [1, 1, 1] or gs_data == [1, 0, 1]:
        if line_out_time == 0:
            line_out_time = time.time()
        if (time.time() - line_out_time > 2):
            car.move('stop')
            line_out_time = 0
        return
    else:
        line_out_time = 0

    if gs_data == [0, 1, 0]:
        car.set_motors_power([_power, _power, _power, _power]) # forward
    elif gs_data == [0, 1, 1]:
        car.set_motors_power([_power, int(_power/5), _power, int(_power/5)]) # right
    elif gs_data == [0, 0, 1]:
        car.set_motors_power([_power, int(-_power/2), _power, int(-_power/2)]) # right plus
    elif gs_data == [1, 1, 0]:
        car.set_motors_power([int(_power/5), _power, int(_power/5), _power]) # left
    elif gs_data == [1, 0, 0]:
        car.set_motors_power([int(-_power/2), _power, int(-_power/2), _power]) # left plus

'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):
    global mode

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        return
    
    ''' data to display'''
    # greyscale
    ws.send_dict['A'] = grayscale.get_value()

    # grayscale reference
    if 'A' in data.keys() and isinstance(data['A'], list):
        grayscale.set_edge_reference(data['A'][0])
        grayscale.set_line_reference(data['A'][1])
    else:
        grayscale.set_edge_reference(GRAYSCALE_CLIFF_REFERENCE_DEFAULT)
        grayscale.set_line_reference(GRAYSCALE_LINE_REFERENCE_DEFAULT)

    # mode select:
    if 'N' in data.keys() and data['N'] == True:
        if mode != 'line track':
            mode = 'line track'
            print(f"change mode to: {mode}")
    else:
        if mode != None:
            mode = None
            print(f"change mode to: {mode}")
    

def remote_handler():

    ''' move && anti-fall '''
    if mode == 'line track':
        line_track()             

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
    print(e)
finally:
    onboard_led.off()       
    car.move("stop")