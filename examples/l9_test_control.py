from ws import WS_Server
import json
import time
import pico_4wd as car

NAME = 'my_4wd_car'

# Client Mode
WIFI_MODE = "sta"
SSID = "MakerStarsHall"
PASSWORD = "sunfounder"
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)

# AP Mode
# WIFI_MODE = "ap"
# PASSWORD = "12345678"
# ws = WS_Server(name=NAME, mode=WIFI_MODE, password=PASSWORD)

ws.start()

temp = None
temp_send = None

def on_receive(data):
    # coding the control function here.
    
    # coding the sensor function here.
    print(data["K_region"])
    # ws.send_dict['L_region'] = car.get_grayscale_list() # example for test sensor date sending.

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
