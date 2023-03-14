import time
from ws import WS_Server
from machine import Pin

'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
WIFI_MODE = "ap"
SSID = "" # your wifi name, if blank, use the set name "NAME"
PASSWORD = "12345678" # your password

# STA Mode
# WIFI_MODE = "sta"
# SSID = "ssid"
# PASSWORD = "password"

'''------------ Instantiate -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
onboard_led = Pin(25, Pin.OUT) 

'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):

    ''' the data from APP to PICO '''
    #print("recv_data: %s"%data)

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        return
 
    if 'K' in data.keys():
        print(data['K'])
 
    
    ''' the data send to APP '''
    ws.send_dict['J'] = 34.67

'''----------------- main ---------------------'''
try:
   ws.on_receive = on_receive
   if ws.start():
        onboard_led.on()
        while True:
            ws.loop() 
except Exception as e:
    print(e)
finally:
    onboard_led.off()       