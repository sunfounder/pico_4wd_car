EXAMPLE - Play ``app_control.py``
-----------------------------------------------

Now, please open the ``app_control.py`` in **examples** and try the complete APP remote control gameplay!

|sc_app_control_example|

.. code-block:: python

    from ws import WS_Server
    import json
    import time
    import pico_4wd as car

    NAME = 'my_pico_car'

    # Client Mode
    # WIFI_MODE = "sta"
    # SSID = "YOUR_SSID_HERE"
    # PASSWORD = "YOUR_PASSWORD_HERE"

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
        if 'K' in data.keys() and 'A' in data.keys():
            if data['K'] == "left":
                car.write_light_color_at(0, [50, 50, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(1, [50, 50, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(6, [0, 0, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(7, [0, 0, 0], preset=car.LIGHT_REAR)
            elif data['K'] == "right":
                car.write_light_color_at(0, [0, 0, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(1, [0, 0, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(6, [50, 50, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(7, [50, 50, 0], preset=car.LIGHT_REAR)
            else:
                car.write_light_color_at(0, [0, 0, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(1, [0, 0, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(6, [0, 0, 0], preset=car.LIGHT_REAR)
                car.write_light_color_at(7, [0, 0, 0], preset=car.LIGHT_REAR)
            car.light_excute()
                
            car.move(data['K'], data['A'])
        
        # RGB LED
        if 'G' in data.keys():
            led_status = data['G']
                
        # Speed measurement
        ws.send_dict['B'] = car.speed()
        if led_status:
            # HUE color system, Red is 0, and Green is 120
            hue = car.mapping(car.speed(), 0, 70, 120, 0)
            rgb = car.hue2rgb(hue)
            car.set_light_bottom_color(rgb)
        else:
            car.set_light_bottom_color([0,0,0])
        
        # mileage
        ws.send_dict['C'] = car.speed.mileage

        # radar
        ws.send_dict['D'] = car.get_radar_distance()
        
        # greyscale
        ws.send_dict['H'] = car.get_grayscale_values()

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
