4. APP - LIGHT
==================

Now to control the RGB boards of the Pico 4WD car.


**Quick User Guide**

#. Run the ``app_4_light.py`` file under the ``pico_4wd_car\examples\app_control`` path.

#. Based on :ref:`app_move`, add **Button** and **Switch** widgets to the **E** and **F** areas as shown below.

    .. image:: img/APP_DB_4_1.png

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. When you use the **D-pad** widget to make the car move, the tail light will show the direction. The on/off and color of underglow can be controlled through the **Switch** and **Button** widgets.

**How it works?**

This project is based on :ref:`app_move` with the addition of lighting effects.

#. Here, a total of three lighting effects are added and called in ``remote_handler()``.

    .. code-block:: python

        def remote_handler():
            global throttle_power, steer_power, move_status, dpad_touched

            if dpad_touched:
                my_car_move(throttle_power, steer_power, gradually=True)

            ''' no operation '''
            if not dpad_touched:
                move_status = "stop"
                car.move('stop')

            # ''' Bottom Lights '''
            bottom_lights_handler()
            # ''' Singal lights '''
            singal_lights_handler()
            # ''' Brake lights '''
            brake_lights_handler()

    * ``bottom_lights_handler()``: Controls the on/off and colors of the two RGB boards at the bottom.
    * ``singal_lights_handler()``: Control the left and right RGB LEDs of the rear RGB board, for example, when the car turns left, make the left two LEDs of the rear RGB board light up, and the same for the turn right.
    * ``brake_lights_handler()``: Controls the tail RGB board to light up red in breathing mode when the car stops or brakes.

#. About ``singal_lights_handler()`` function.

    * When ``left`` is received, make the left two LEDs of the rear RGB board light up orange (``singal_on_color``).
    * When ``right`` is received, make the right two LEDs of the rear RGB board light up orange (``singal_on_color``).
    * Otherwise, let the left and right LEDs are off (``0x000000``).

    .. code-block:: python

        def singal_lights_handler():
            if move_status == 'left':
                lights.set_rear_left_color(singal_on_color)
                lights.set_rear_right_color(0x000000)
            elif move_status == 'right':
                lights.set_rear_left_color(0x000000)
                lights.set_rear_right_color(singal_on_color)
            else:
                lights.set_rear_left_color(0x000000)
                lights.set_rear_right_color(0x000000)


#. About ``brake_lights_handler()`` function.
    
    When ``stop`` is received, let the RGB board on the tail light up red(``brake_on_color``) in breathing mode(The brightness slowly goes from bright to dark and dark to bright.).

    .. code-block:: python

        def brake_lights_handler():
            global is_move_last , brake_light_status, brake_light_time, led_status, brake_light_brightness
            global brake_light_brightness, brake_light_brightness_flag

            if move_status == 'stop':
                if brake_light_brightness_flag == 1:
                    brake_light_brightness += 5
                    if brake_light_brightness > 255:
                        brake_light_brightness = 255
                        brake_light_brightness_flag = -1
                elif brake_light_brightness_flag == -1:
                    brake_light_brightness -= 5
                    if brake_light_brightness < 0:
                        brake_light_brightness = 0
                        brake_light_brightness_flag = 1          
                brake_on_color = [brake_light_brightness, 0, 0]
                lights.set_rear_color(brake_on_color)
            else:
                if is_move_last:
                    lights.set_rear_middle_color(0x000000)
                else:
                    lights.set_rear_color(0x000000)
                is_move_last = True
                brake_light_brightness = 255


#. About ``bottom_lights_handler()`` function.

    * The variable ``led_status`` is ``True`` when the widget in the **E** area is ON, which causes the bottom two RGB boards to light up in a specific color.
    * This specific color is selected from the array (``led_theme[]``) by tapping on the widget in the **F** area.

    .. code-block:: python

        def bottom_lights_handler():
            global led_status
            if led_status:
                color = list(led_theme[str(led_theme_code)])
            else:
                color = [0, 0, 0]
            lights.set_bottom_color(color)



#. And the ``on_receive(data)`` function also has some changes based on :ref:`app_move`.

   * When you tap the D-apd buttons, the return ``left``, ``right``, ``forward`` or ``backward`` will cause the variable ``move_status`` to change simultaneously.
   * This will allow the 3 RGB boards to display different effects as the car move.


    .. code-block:: python
    
        def on_receive(data):
            global throttle_power, steer_power, move_status, dpad_touched
            global led_status, led_theme_code, led_theme_sum

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
                    move_status = 'left'
                    if steer_power > 0:
                        steer_power = 0
                    steer_power -= int(throttle_power/2)
                    if steer_power < -100:
                        steer_power = -100
                elif data['K'] == "right":
                    dpad_touched = True
                    move_status = 'right'
                    if steer_power < 0:
                        steer_power = 0
                    steer_power += int(throttle_power/2)
                    if steer_power > 100:
                        steer_power = 100
                elif data['K'] == "forward":
                    dpad_touched = True
                    move_status = 'forward'
                    steer_power = 0
                elif data['K'] == "backward":
                    dpad_touched = True
                    move_status = 'backward'
                    steer_power = 0
                    throttle_power = -throttle_power
                else:
                    dpad_touched = False
                    move_status = 'stop'
                    steer_power = 0

            if throttle_power == 0:
                move_status = 'stop'

#. In addition, the ``on_receive(data)`` function also responds to widgets in the **E** and **F** areas.

    * The widget in the **E** area is used to turn on/off the bottom RGB boards, while the widget in the **F** area is used to change colors.
    * Assign the return value of the **E** area widget to the variable ``led_status``.
    * If ``led_status`` is ``True`` (the widget in the **E** area is toggled ON), then determine if the widget in the **F** area is tapped.
    * If so, switch to the next color in the array ``led_theme[]``.


    .. code-block:: python

        def on_receive(data):
            global throttle_power, steer_power, move_status, dpad_touched
            global led_status, led_theme_code, led_theme_sum

            ''' if not connected, skip & stop '''
            if not ws.is_connected():
                return

            ...
            ...

            # LEDs switch
            if 'E' in data.keys():
                led_status = data['E']

            if led_status:
                # LEDs color theme change
                if 'F' in data.keys() and data['F'] == True:
                    led_theme_code = (led_theme_code + 1) % led_theme_sum
                    print(f"set led theme color: {led_theme_code}, {led_theme[str(led_theme_code)][0]}")

