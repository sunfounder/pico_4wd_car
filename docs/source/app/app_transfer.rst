1. Basic Communication
===========================================

If you have finished :ref:`play_mode`, you should know how to control Pico 4WD Car with SunFounder Controller. Here we will show you how they transfer data to each other.


**Quick User Guide**


#. Install `SunFounder Controller <https://docs.sunfounder.com/projects/sf-controller/en/latest/>`_ from **APP Store(iOS)** or **Google Play(Android)**.

#. Run the ``app_1_transfer.py`` file under the ``pico_4wd_car\examples\app_control`` directory.


#. Let's start the Pico 4WD Car.

    * When first used or when the battery cable is unplugged, Pico RDP will activate its over-discharge protection circuitry(Unable to get power from battery).
    * Therefore, you'll need to plug in a Type-C cable for about 5 seconds to release the protection status.
    * At this time look at the battery indicators, if both battery indicators are off, please continue to plug in the Type-C cable to charge the battery.

        .. image:: img/pico_rdp_power.png

    .. note::
        Additionally, the LED on the ESP01S module will blink indicating that your mobile device is not connected.


#. Connect to ``my_4wd_car`` LAN.

    Your mobile device should now be connected to Pico 4WD Car's LAN so that they are on the same network.

    * Find ``my_4wd_car`` on the WLAN of the mobile phone (tablet), enter the password ``12345678`` and connect to it. 

        .. image:: img/seach_wifi.jpg

    * The default connection mode is AP mode. So after you connect, there will be a prompt telling you that there is no Internet access on this WLAN network, please choose to continue connecting.

        .. image:: img/connect_anyway.png


#. Create a controller.

    * Open SunFounder Controller and click on the **+** to create a new controller.

        .. image:: img/app_control13.png

    * Select the **Blank** and **Dual Stick** template, enter a name and click **Confirm**.

        .. image:: img/choose_preset_blank.PNG

    * You are now inside the controller. Click on the **K** area and select the **D-pad** widget.

        .. image:: img/APP_DB_N_1.png

    * Then add a **Number** widget to the **J** area.

        .. image:: img/APP_DB_N_2.png

    * Now you should see the interface like this.

        .. image:: img/APP_DB_1_6.png

    * Click the |app_save| button in the upper right corner.

        .. image:: img/APP_DB_N_3.png

#. Connect and run the Controller.

    * Now connect the SunFounder Controller to the Pico 4WD Car via the |app_connect| button to start communication.Wait a few seconds and ``my_4wd_car(IP)`` will appear, click on it to connect.

        .. image:: img/connect_4wd.png

        .. note::
            You need to make sure that your mobile device is connected to the ``my_4wd_car`` LAN, if you are not seeing the above message for a long time.

    * After the "Connected Successfully" message appears and the product name will appear in the upper right corner.

    * At the same time, the LED on the ESP01S module will stop flashing.

        .. image:: img/esp01s_led.png

    * After clicking the |app_run| button. The widget in the J area will show 34.67. The Shell in the Thonny IDE will return ``stop``, and when you tap the D-Pad in the APP, it will return ``forward``, ``backward``, ``left``, or ``right``.

**How it works?**

The communication between Pico and Sunfounder Controller 
is based on the ``websocket protocol``.

* `WebSocket - Wikipedia <https://en.wikipedia.org/wiki/WebSocket>`_

The specific workflow of APP Control gameplay is as follows:

    .. image:: img/flowchart_app_control.png

.. code-block:: python

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


This code constitutes the basic framework of APP control. 
Here, you need to pay attention to the following two parts:

1. Setup websocket

    There are two connection mode between Sunfounder Controller and Pico: One is **AP** mode, the other is **STA** mode.

    * **AP Mode**: You need to connect Sunfounder Contorller to the hotspot released by pico.
    * **STA Mode**: You need to connect Sunfounder Controller and pico to the same WLAN.
    
    * **AP Mode**

    The default connection mode is **AP Mode**: The Pico releases the hotspot (the Wifi name is ``NAME`` in the code, here is ``my_4wd_car``), the mobile phone (tablet) is connected to this LAN. 
    This mode allows you to remotely control pico in any situation, but will make your phone (tablet) temporarily unable to connect to the Internet.

    .. code-block:: python
        :emphasize-lines: 3

        from ws import WS_Server

        '''Set name'''
        NAME = 'my_4wd_car'

        '''Configure wifi'''
        # AP Mode
        WIFI_MODE = "ap"
        SSID = "" # your wifi name, if blank, use the set name "NAME"
        PASSWORD = "12345678" # your password

        # STA Mode
        # WIFI_MODE = "sta"
        # SSID = "<ssid>"
        # PASSWORD = "<password>"

        '''------------ Instantiate -------------'''
        ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)


    * **STA Mode**

    You can also use **STA** mode: Let the pico connects to your home WLAN, and your mobile phone (tablet) should also be connected to the same WLAN. 
    
    This mode is opposite to the **AP** mode and will not affect the normal use of the mobile phone (tablet), but will limit your pico from leaving the WLAN radiation range.

    The way to start this mode is to comment out the three lines under ``## AP Mode``, uncomment the three lines under ``## STA Mode``, and change the ``SSID`` and ``PASSWORD`` to your home WIFI at the same time.

    .. code-block:: python
        :emphasize-lines: 3,4

        from ws import WS_Server

        '''Set name'''
        NAME = 'my_4wd_car'

        '''Configure wifi'''
        # AP Mode
        # WIFI_MODE = "ap"
        # SSID = "" # your wifi name, if blank, use the set name "NAME"
        # PASSWORD = "12345678" # your password

        # STA Mode
        WIFI_MODE = "sta"
        SSID = "<ssid>"
        PASSWORD = "<password>"

        '''------------ Instantiate -------------'''
        ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)

    After completing the connection mode settings, 
    Websocket will set up and start the server.

    .. code-block:: python

        ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)  

#. Responding

    The specific operation code of Pico and Sunfounder Controller is written on the ``on_receive()`` function. Usually, 
    we need to write the codes for APP to control Pico on the front and the codes for APP to show Pico sensor data on the back.

    .. code-block:: python

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

    Finally, ``on_receive()`` will be assigned to ``ws.on_receive`` and then called by ``ws.loop``.

    .. code-block:: python
        :emphasize-lines: 2,6

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
