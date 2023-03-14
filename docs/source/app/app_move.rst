.. _app_move:

2. APP - Car Move
====================

In this project, you will learn how to adjust the car's movement and speed using the APP.


**Quick User Guide**


#. Run the ``app_2_move.py`` file under the ``pico_4wd_car\examples\app_control`` path.

#. Then connect your device (phone/tablet) to ``my_4wd_car``.

    .. image:: img/seach_wifi.jpg

#. After opening the SunFounder controller, create a new controller and then add a **D-pad** widget to the **K** area and a **Throttle** widget to the **Q** area.

    .. image:: img/APP_DB_2_0.png

#. Click on the **set** button of the **Throttle** widget, change the maximum value to 100, the minimum value to 0, and the initial value to 20.

    .. image:: img/APP_DB_2_C.png

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. Now, you can use the D-Pad to control the movement of the car; the Throttle widget is used to adjust the power of the car (if it is 0, the car is not moving).


**How it works?**

This code can be seen in several steps.

#. Communication-related has been explained in the previous project, so we will skip it here.

#. Now let's see how to respond to the data transferred by the APP. In the ``on_receive(data)`` function, it responds to the data from the **Q** and **K** areas to change the values of ``throttle_power`` and ``steer_power``, which together affect the movement and turning power of the car.

    .. code-block:: python

        '''----------------- on_receive (ws.loop()) ---------------------'''
        def on_receive(data):
            global throttle_power, steer_power, dpad_touched

            ''' if not connected, skip & stop '''
            if not ws.is_connected():
                return
            
            # Move - power
            if 'Q' in data.keys() and isinstance(data['Q'], int):
                throttle_power = data['Q']
            else:
                throttle_power = 0

            # Move - direction
            if 'K' in data.keys():
                #print(data['K'])
                if data['K'] == "left":
                    dpad_touched = True
                    if steer_power > 0:
                        steer_power = 0
                    steer_power -= int(throttle_power/2)
                    if steer_power < -100:
                        steer_power = -100
                elif data['K'] == "right":
                    dpad_touched = True
                    if steer_power < 0:
                        steer_power = 0
                    steer_power += int(throttle_power/2)
                    if steer_power > 100:
                        steer_power = 100
                elif data['K'] == "forward":
                    dpad_touched = True
                    steer_power = 0
                elif data['K'] == "backward":
                    dpad_touched = True
                    steer_power = 0
                    throttle_power = -throttle_power
                else:
                    dpad_touched = False
                    steer_power = 0

   * ``throttle_power``: Used to adjust the moving power of the car.
   * ``steer_power``: For adjusting the turning power.
   * ``dpad_touched``: The default is ``False``, ``True`` when receiving data from **K** area, thus making the car move.

#. Make the car move. The function ``my_car_move()`` is created to convert ``throttle_power`` and ``steer_power`` to left and right motors rotation power.

    .. code-block:: python

        '''----------------- motors fuctions ---------------------'''
        def my_car_move(throttle_power, steer_power, gradually=False):
            power_l = 0
            power_r = 0

            if steer_power < 0:
                power_l = int((100 + 2*steer_sensitivity*steer_power)/100*throttle_power)
                power_r = int(throttle_power)
            else:
                power_l = int(throttle_power)
                power_r = int((100 - 2*steer_sensitivity*steer_power)/100*throttle_power)

            if gradually:
                car.set_motors_power_gradually([power_l, power_r, power_l, power_r])
            else:
                car.set_motors_power([power_l, power_r, power_l, power_r])

#. Handler. The ``remote_handler()`` function is used to execute all the code related to the actual action of the car. The role in this project is to make the car move when the D-pad is tapped.

    .. code-block:: python

        def remote_handler():
            global throttle_power, steer_power, dpad_touched

            if dpad_touched: # The car only moves when you press the K widget
                my_car_move(throttle_power, steer_power, gradually=True)

            ''' no operation '''
            if not dpad_touched:
                car.move('stop')