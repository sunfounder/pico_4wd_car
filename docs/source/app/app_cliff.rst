6. Anti-Fall
============

Here, we added an anti-fall mode to the Pico 4WD car. If you move the Pico 4WD car to the edge of a table or stairs, it will stop moving. Unless you let it back up to a safe area, it will continue to move.

**Quick User Guide**


#. Run the ``app_6_cliff.py`` file under the ``pico_4wd_car\examples\app_control`` path and then power on the Pico 4WD car.

#. Based on :ref:`app_move`, add **Grayscale Indicator** and **Switch** widgets to **A** and **M** areas as shown below.

    .. image:: img/APP_DB_6_1.png

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. While this controller is running, **Grayscale Value(A)** will show the values of the three grayscale sensors in real time.

#. Place the grayscale module in three environments: white, black and hanging in the air (10cm or more) to see how the data in the changes.

    **White surface**
        You will find that the value of the white surface is generally large, for example mine is around 240,000.

    .. image:: img/grayscale_white.png
        :width: 500
        :align: center

    **Black line**
        The value on the black line will be smaller, and now I'm at about 2000.

    .. image:: img/grayscale_black.png
        :width: 500
        :align: center

    **Overhang (10cm or more)**
        And the value of the overhang will be even smaller, already less than 1000 in my environment.

    .. image:: img/grayscale_cliff.png
        :width: 500
        :align: center

#. Set the threshold value.

    * My car reads around 24000 in the white area and around 2000 in the black line, so I set ``line_ref`` to about the middle value of ``10000``.
    * In the cliff area it reads less than 1000, so I set ``cliff_ref`` to ``1000``.

    * Now click the |app_edit| button to enter edit mode.

        .. image:: img/edit_controller.png

    * Click on the **Settings** button in the upper right corner of the **Grayscale Value(A)** widget.

        .. image:: img/set_grayscale.png

    * Fill in the cliff and line thresholds.

        .. image:: img/grayscale_refer.png

#. Now re-save the SunFounder Controller and toggle the **Switch** widget to ON. If you move the Pico 4WD car to the edge of a table or stairs, it will stop moving. Unless you let it back up to a safe area, it will continue to move.


**How it works?**

#. This project is based on :ref:`app_move` and adds some responsiveness to the grayscale module, as reflected in the widgets in the **A** and **M** areas.


   * Send the grayscale value to area **A** for showing.
   * Then read the value of the widget in area **A**. If there are set thresholds, then use the set thresholds, otherwise use the default thresholds.
   * When the widget in area **M** is toggled to ON, the output value is ``True`` to let Pico 4WD car switch to the anti-fall mode.

    .. code-block:: python

        def on_receive(data):
            global throttle_power, steer_power, dpad_touched
            global mode

            ''' if not connected, skip & stop '''
            if not ws.is_connected():
                return

            ''' remote control'''
            # Move - power
            ...

            # Move - direction
            ...

            ''' data to display'''
            # grayscale
            ws.send_dict['A'] = grayscale.get_value()

            # grayscale reference
            if 'A' in data.keys() and isinstance(data['A'], list):
                grayscale.set_edge_reference(data['A'][0])
                grayscale.set_line_reference(data['A'][1])
            else:
                grayscale.set_edge_reference(GRAYSCALE_CLIFF_REFERENCE_DEFAULT)
                grayscale.set_line_reference(GRAYSCALE_LINE_REFERENCE_DEFAULT)


            # mode select:
            if 'M' in data.keys() and data['M'] == True:
                if mode != 'anti fall':
                    mode = 'anti fall'
                    print(f"change mode to: {mode}")
            else:
                if mode != None:
                    mode = None
                    print(f"change mode to: {mode}")


#. Then, in the ``remote_handler()`` function, add some judgments.

    * After switching to anti-fall mode, if the Pico 4WD car is at the edge of the table and stairs, it will stop and the D-pad can only control the car to back up.
    * The car can only continue to move with D-apd control after backing up to a safe area.

    .. code-block:: python

        def remote_handler():
            global throttle_power, steer_power, dpad_touched

            ''' move && anti-fall '''
            if mode == "anti fall":
                if grayscale.is_on_edge():
                    if dpad_touched and throttle_power<0: # only for backward
                        my_car_move(throttle_power, steer_power, gradually=True)
                    else:
                        car.move("stop")
                else:
                    if dpad_touched:
                        my_car_move(throttle_power, steer_power, gradually=True)
                    else:
                        car.move("stop")                
            elif dpad_touched:
                my_car_move(throttle_power, steer_power, gradually=True)

            ''' no operation '''
            if not dpad_touched:
                car.move('stop')
