Control the Car with APP
==============================

This section will guide you through building a remote project using the Sunfounder Controller APP, which means you can use your phone/tablet to control your Pico-4wd car.

**1. Setup SunFounder Controller**

#. Install |link_sunfounder_controller| APP from APP Store(iOS) or Google Play(Android).

#. Open SunFounder Controller and click on the **+** to create a new controller.

    .. image:: img/app_control13.png

#. We have preset controller for Pico-4wd, you can choose it directly.

    .. image:: img/app_control4.png

#. Define a name for this Controller and click **Confirm**.

    .. image:: img/app_control5.png

#. Now that you are inside this preset controller, click the Grayscale Values widget's Settings button to change its reference value.

    .. image:: img/app_control7.png

#. The following thresholds should be modified based on the values obtained in the :ref:`test_grayscale_module` section.

    .. image:: img/app_control8.png

#. Once you have set it up, click the Save button in the upper right corner to save it. If you need to make any changes, click the Edit button again.

    .. image:: img/app_control9.png

**2. Make the app_control.py file run on boot**

In order for Pico-4wd to be able to run specific scripts without being connected to a computer, and then be controlled by SunFounder Controller. You need to save the specific script to the Raspberry Pi Pico with the name main.py, as follows.

#. Open the ``app_control.py`` file under the path of ``pico_4wd_car_main\examples``, then click "run current script" button or just press F5 to run it.

    .. image:: img/app_control1.png

#. If you run the code, you will see this **IP** in the shell; remember it, as it may be used to connect to SunFounder Controller later on.

    .. image:: img/app_control14.png

#. Press ``Ctrl+Shift+S`` and select **Raspberry Pi Pico** in the popup window that appears. If this pop-up does not appear on yours, make sure you have plugged the Pico into your computer with a micro USB cable and select the "MicroPython (Raspberry Pi Pico).COMXX" interpreter in the bottom right corner.

    .. image:: img/app_control2.png

#. Set the file name to ``main.py``. If you already have the same file in your Pico, it will prompt to overwrite it.

    .. image:: img/app_control3.png

Now you can unplug the USB cable, turn on the power switch of Pico-4wd, and Pico-4wd will automatically run this ``main.py`` script.

**3. Connect to Pico 4WD car**

#. Find ``my_4wd_car`` on the WLAN of the mobile phone (tablet), enter the password ``12345678`` and connect to it. 

    .. image:: img/seach_wifi.jpg

#. The default connection mode in ``app_control.py`` is |link_ap_mode|. So after you connect, there will be a prompt telling you that there is no Internet access on this WLAN network, please choose to continue connecting.

    .. image:: img/connect_anyway.png

#. Now go back to SunFounder Controller, when you click the **Connect** button, it will automatically search for robots nearby. 

    .. image:: img/app_control10.png
    
#. Click on the ``my_4wd_car``.

    .. image:: img/app_control11.png

    .. note::
        * You need to make sure that your mobile device is connected to the ``my_4wd_car`` LAN.

        * If it doesn’t search automatically, you can also manually enter your car's IP to connect.

        .. image:: img/app_control6.png

Once you click on ``my_4wd_car``, the message “Connected Successfully” will appear and the product name will appear in the upper right corner.

**4. Run this Controller**

    Click the **Run** button to start the controller.

    .. image:: img/app_control12.png

    Here are the functions of the widgets.

    * A: Drive the car at 0~100% power. Before controlling the car movement with the K widget, you must set the A widget to 30% or more.
    * B: The display of the car moving speed, unit: cm/s.
    * C: Display of car speed in digital format.
    * D: Radar display of obstacles detected by ultrasonic module.
    * G: Turn on/off WS2812 RGB board.
    * H: Show the data of the three sensors on the grayscale module, which have three states: black block: black line detected; white: white detected; exclamation point: cliff detected.
    * K: Control forward, backward, left, and right motions of the car.

