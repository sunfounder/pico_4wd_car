Data transfer between APP and Pico
=============================================

**From APP to Pico-4wd**

    Let's take a look at what kind of data Pico-4wd will get from the APP. Print ``data`` directly in ``on_receive``.

.. note::
    
    * Open the ``app_test.py`` file under the path of ``pico_4wd_car\tests`` or copy this code into Thonny.

    * Rewrite the ``on_receive(data)`` function to only print ``data`` as shown below.

    * Then click “Run Current Script” or simply press F5 to run it.

    * Don’t forget to click on the “MicroPython (Raspberry Pi Pico)” interpreter in the bottom right corner.

    * Each time you rerun the code, you need to connect your device’s Wi-Fi to ``my_4wd_car`` , then turn on SunFounder Controller and reconnect.
    
    .. code-block:: python
        :emphasize-lines: 21,23

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
            print(data)
            
            # write sensor codes here.
            pass

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




    You will be able to see the following string:

    .. code-block:: 

        {'J': None, 'A': None, 'L': None, 'K': None, 'F': None, 'M': None, 'H': 50, 'Q': None, 'G': None, 'I': None, 'B': None, 'D': None, 'C': None, 'N': None, 'E': None, 'P': None, 'O': None}

    As we can see, the value of H Box is 50 (``'H': 50``), and the others are None. 
    This is because we only add one control widget (H Box), and the slide widget was dragged to the **50** position. 
    The widget in the D area is not used for control but only for show.

    We can also add other control widgets, and use the same method to view the values ​​sent by these widgets to Pico-4wd.

    You can get the value of the corresponding widget by just using the label. 
    Let's rewrite ``on_receive(data)`` again. As shown below, print the value of the H Box widget:

    .. code-block:: python

        def on_receive(data):
            # write control codes here.
            print(data['H'])
            
            # write sensor codes here.
            pass
    
    .. code-block::

        >>> %Run -c $EDITOR_CONTENT
            Connecting
            WebServer started on ws://192.168.4.1:8765
            start
            Connected from 192.168.4.3
            50
            50
            50

    The values obtained from the app can be used to control the car.
    Rewrite ``on_receive(data)`` once again. As shown below, use the obtained H Box widget (Slider) value to control the RGB Board at the rear of the car.

    .. code-block:: python

        def on_receive(data):
            # write control codes here.            
            num = int(data['H']*9/100)
            for i in range(0,num):
                car.write_light_color_at(i, [80, 50, 0])
            for i in range(num,8):
                car.write_light_color_at(i, [0, 0, 0])
            car.light_excute()

    You can use `API <https://github.com/sunfounder/pico_4wd_car/blob/main/api_reference_pico_4wd.md>`_ file to help you understand the functions in the code.

**From Pico-4wd to APP**

    Now let's see what kind of data Pico-4wd will send to the APP. 
    Rewrite ``on_receive(data)`` as shown below. 
    The following code is used to obtain the ultrasonic detection distance.



    .. code-block:: python
        :emphasize-lines: 21,23,24

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
            # write sensor codes here.
            data = car.get_radar_distance()
            print(data)

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


    .. code-block:: 

        >>> %Run -c $EDITOR_CONTENT
            Connecting
            WebServer started on ws://192.168.4.1:8765
            start
            Connected from 192.168.4.2
            [-10, 49.249]
            [-20, 37.417]
            [-30, 38.947]
            [-40, 36.193]
            [-50, 40.12]
            [-60, 36.431]  
    
    You can use `API <https://github.com/sunfounder/pico_4wd_car/blob/main/api_reference_pico_4wd.md>`_ file to help you understand the functions in the code.

    Now, Rewrite ``on_receive(data)``, use the ``send_dict`` function to show the distance value in D Widget.

    .. code-block:: python
        :emphasize-lines: 5

        def on_receive(data):
            # write sensor codes here.
            data = car.get_radar_distance()
            print(data)
            ws.send_dict['D'] = data