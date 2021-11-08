from ws import WS_Server
import json
import time
import pico_4wd as car

NAME = 'my_pico_car'

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

def on_receive(data):
    gs_l , gs_c, gs_r = car.get_grayscale_values()
    ws.send_dict['N'] = gs_l
    ws.send_dict['O'] = gs_c
    ws.send_dict['P'] = gs_r

ws.on_receive = on_receive

def main():
    print("start")
    while True:
        ws.loop()

try:
    main()
finally:
    car
