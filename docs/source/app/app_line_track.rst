7. Line Track
================

Let Pico 4wd walk on its exclusive avenue! 
Tape a line on a light-colored ground (or table) with 
black insulating tape. 

You will see Pico-4wd track the line to forward.


.. warning::
    When pasting this line, 
    there should be no sharp turns so that the car does not drive off the path.


**Quick User Guide**


#. Run the ``app_7_line_track.py`` file under the ``pico_4wd_car\examples\app_control`` path and then power on the Pico 4WD car.

#. As shown below, create a controller that adds **Grayscale Indicator** and **Switch** widgets to **A** and **N** areas, respectively.


    .. image:: img/APP_DB_7_1.png


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

#. Now re-save the SunFounder Controller and toggle the **Switch** widget to ON. Place the car on the black line and you will see the Pico-4wd tracking line advancing.


**How it works?**

#. In ``on_receive(data)``, the grayscale values are sent to the **A** area for showing and responding to the data from the **N** area.

   * Send the grayscale value to area **A** for showing.
   * Then read the value of the widget in area **A**. If there are set thresholds, then use the set thresholds, otherwise use the default thresholds.
   * When the widget in area **N** is toggled to ON, the output value is ``True`` to let Pico 4WD car switch to the line track mode.

    .. code-block:: python

        '''----------------- on_receive (ws.loop()) ---------------------'''
        def on_receive(data):
            global mode

            ''' if not connected, skip & stop '''
            if not ws.is_connected():
                return
            
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
            if 'N' in data.keys() and data['N'] == True:
                if mode != 'line track':
                    mode = 'line track'
                    print(f"change mode to: {mode}")
            else:
                if mode != None:
                    mode = None
                    print(f"change mode to: {mode}")
    

#. Create a ``line_track()`` function to move the car in different directions based on the detection result of the grayscale module.

    * When the detected grayscale value of the corresponding channel is less than set threshold, a ``1`` will be output, which means a black line is detected.
    * Then all three sets of data (``[0, 1, 0]``) will be output by ``get_line_status()``.
    * Then make the car move in different directions according to the output data.


    .. code-block:: python

        '''----------------- line_track ---------------------'''
        def line_track():
            global line_out_time
            _power = LINE_TRACK_POWER
            gs_data = grayscale.get_line_status()
            #print(f"gs_data: {gs_data}, {grayscale.line_ref}")

            if gs_data == [0, 0, 0] or gs_data == [1, 1, 1] or gs_data == [1, 0, 1]:
                if line_out_time == 0:
                    line_out_time = time.time()
                if (time.time() - line_out_time > 2):
                    car.move('stop')
                    line_out_time = 0
                return
            else:
                line_out_time = 0

            if gs_data == [0, 1, 0]:
                car.set_motors_power([_power, _power, _power, _power]) # forward
            elif gs_data == [0, 1, 1]:
                car.set_motors_power([_power, int(_power/5), _power, int(_power/5)]) # right
            elif gs_data == [0, 0, 1]:
                car.set_motors_power([_power, int(-_power/2), _power, int(-_power/2)]) # right plus
            elif gs_data == [1, 1, 0]:
                car.set_motors_power([int(_power/5), _power, int(_power/5), _power]) # left
            elif gs_data == [1, 0, 0]:
                car.set_motors_power([int(-_power/2), _power, int(-_power/2), _power]) # left plus
    

#. In ``remote_handler()`` function, the ``line_track()`` function will be called if the line tracking mode is turned on, otherwise the car is stopped.

    .. code-block:: python

        def remote_handler():

            ''' move && anti-fall '''
            if mode == 'line track':
                line_track()             

            ''' no operation '''
            if mode == None:
                car.move('stop')