from ws import WS_Server
import json
import time
import pico_4wd as car

NAME = 'my_4wd_car'

# Client Mode
WIFI_MODE = "sta"
SSID = "MakerStarsHall"
PASSWORD = "sunfounder"

# AP Mode
# WIFI_MODE = "ap"
# SSID = ""
# PASSWORD = "12345678"

ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
ws.start()
led_status = False

def on_receive(data):
    global led_status

    #Move
    if 'K_region' in data.keys() and 'H_region' in data.keys():
        car.move(data['K_region'], data['H_region'])
    
    # RGB LED
    if 'M_region' in data.keys():
        if data['M_region']:
            if not led_status:
                car.set_all_light_color([100, 100, 100])
                led_status = True
        else:
            if led_status:
                car.set_light_off()
                led_status = False
            
    # speed measurement
    ws.send_dict['A_region'] = car.speed.get_speed()
    
    # radar
    ws.send_dict['D_region'] = car.get_radar_distance()
    
    # greyscale
    ws.send_dict['L_region'] = car.get_grayscale_values()


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
