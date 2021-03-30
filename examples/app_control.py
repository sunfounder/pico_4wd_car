from ws import WS_Server
import json
import time
import pico_4wd as car

NAME = 'my_4wd_car'

# Client Mode
# WIFI_MODE = "sta"
# SSID = "MakerStarsHall"
# PASSWORD = "sunfounder"

# AP Mode
WIFI_MODE = "ap"
SSID = ""
PASSWORD = "12345678"

ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
ws.start()
led_status = False

def on_receive(data):
    global led_status

    #Move
    if 'K_region' in data.keys() and 'H_region' in data.keys():
        if data['K_region'] == "left":
            car.write_light_color_at(0, [0, 0, 0])
            car.write_light_color_at(1, [0, 0, 0])
            car.write_light_color_at(6, [50, 50, 0])
            car.write_light_color_at(7, [50, 50, 0])
        elif data['K_region'] == "right":
            car.write_light_color_at(0, [50, 50, 0])
            car.write_light_color_at(1, [50, 50, 0])
            car.write_light_color_at(6, [0, 0, 0])
            car.write_light_color_at(7, [0, 0, 0])
        else:
            car.write_light_color_at(0, [0, 0, 0])
            car.write_light_color_at(1, [0, 0, 0])
            car.write_light_color_at(6, [0, 0, 0])
            car.write_light_color_at(7, [0, 0, 0])
            
        car.move(data['K_region'], data['H_region'])
    
    # RGB LED
    if 'M_region' in data.keys():
        if data['M_region']:
            if not led_status:
                car.set_light_all_color([100, 100, 100])
                led_status = True
        else:
            if led_status:
                car.set_light_off()
                led_status = False
            
    # speed measurement
    ws.send_dict['A_region'] = car.speed()
    # HUE color system, Red is 0, and Green is 120
    hue = car.mapping(car.speed(), 0, 70, 120, 0)
    rgb = car.hue2rgb(hue)
    for i in range(16):
        car.write_light_color_at(i+8, rgb)
    
    # radar
    ws.send_dict['D_region'] = car.get_radar_distance()
    
    # greyscale
    ws.send_dict['L_region'] = car.get_grayscale_values()
    
    car.light_excute()


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

