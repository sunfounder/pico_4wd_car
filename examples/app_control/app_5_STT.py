'''
This example adds the I widget for voice control.
This example needs to be connected to the Internet, so change to STA mode.
'''

import time
import motors as car
from ws import WS_Server
from machine import Pin


'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
# WIFI_MODE = "ap"
# SSID = "" # your wifi name, if blank, use the set name "NAME"
# PASSWORD = "12345678" # your password

# STA Mode
WIFI_MODE = "sta"
SSID = "xiaoming_PC"
PASSWORD = "bugaosuni"



'''------------ Configure Voice Control Commands -------------'''
voice_commands = {
    # action : [[command , similar commands], [run time(s)]
    "forward": [["forward", "forwhat", "for what"], 3],
    "backward": [["backward","backwood"], 3],
    "left": [["left", "turn left"], 1],
    "right": [["right", "turn right", "while", "white"], 1],
    "stop": [["stop"], 1],
}
current_voice_cmd = None
voice_start_time = 0
voice_max_time = 0

# voice control power
VOICE_CONTROL_POWER = 50


'''------------ Instantiate -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
onboard_led = Pin(25, Pin.OUT) 


'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):
    global current_voice_cmd, voice_start_time, voice_max_time

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        return

    # Voice control
    voice_text = None
    if 'I' in data.keys() and  data['I'] != '':
        ws.send_dict['I'] = 1
        voice_text = data['I']
    else:
        ws.send_dict['I'] = 0
        
    if voice_text != None:
        print(f"voice_text: {voice_text}")
        for vcmd in voice_commands:
            if voice_text in voice_commands[vcmd][0]:
                print(f"voice control match: {vcmd}")
                current_voice_cmd = vcmd
                voice_max_time =  voice_commands[vcmd][1]
                break
        else:
            print(f"voice control without match")

    

def remote_handler():
    global current_voice_cmd, voice_start_time, voice_max_time
    ''' Voice Control '''
    if current_voice_cmd != None :

        if voice_max_time != 0:
            if voice_start_time == 0:
                voice_start_time = time.time()
            if ((time.time() - voice_start_time) < voice_max_time):
                if current_voice_cmd == "forward":
                    car.move("forward", VOICE_CONTROL_POWER)
                elif current_voice_cmd == "backward":
                    car.move("backward", VOICE_CONTROL_POWER)
                elif current_voice_cmd == "right":
                    car.move("right", VOICE_CONTROL_POWER)
                elif current_voice_cmd == "left":
                    car.move("left", VOICE_CONTROL_POWER)
                elif current_voice_cmd == "stop":
                    car.move("stop")
            else:
                current_voice_cmd = None
                voice_start_time = 0
                voice_max_time = 0
    else:
        car.move("stop")



'''----------------- main ---------------------'''
   
try:
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