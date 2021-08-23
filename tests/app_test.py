from ws import WS_Server
import json
import time
import pico_4wd as car

NAME = 'my_4wd_car'

## Client Mode
# WIFI_MODE = "sta"
# SSID = "YOUR SSID HERE"
# PASSWORD = "YOUR PASSWORD HERE"

## AP Mode
WIFI_MODE = "ap"
SSID = ""
PASSWORD = "12345678"

ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
ws.start()

def on_receive(data):
    # write control codes here.
    num = int(data['H']*9/100)
    for i in range(0,num):
        car.write_light_color_at(i, [80, 50, 0])
    for i in range(num,8):
        car.write_light_color_at(i, [0, 0, 0])
    car.light_excute()
    
    # write sensor codes here.    
    data = car.get_radar_distance()
    ws.send_dict['D'] = data

ws.on_receive = on_receive

def main():
    print("start")
    while True:
        ws.loop()

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()