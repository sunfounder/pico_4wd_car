8. APP - Follow
===================

In this project, Pico-4wd car will follow the object in front of it. For example, if you put your hand in front of Pico 4WD, it will rush towards your hand.
And it will also play the advantage of sonar scanning, will judge your hand position and then adjust the forward direction.


**Quick User Guide**

#. Run the ``app_9_avoid.py`` file under the ``pico_4wd_car\examples\app_control`` path and then power on the Pico 4WD car.

#. As shown below, create a controller that adds **Radar**, **Number**, and **Button** widgets to the **D**, **J**, and **P** areas, respectively.

    .. image:: img/APP_DB_8_1.png

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. The car will follow your hand forward when you toggle the **Switch** widget in the **P** area to ON.

**How it works?**


#. In ``on_receive(data)``, the distances and angles are sent to the **D**  and **J** areas for showing, then responding to the data from the **P** area.


    .. code-block:: python

        def on_receive(data):
            global mode

            ''' if not connected, skip & stop '''
            if not ws.is_connected():
                return

            ''' data to display'''
            # # sonar and distance
            ws.send_dict['D'] = [sonar_angle, sonar_distance]
            ws.send_dict['J'] = sonar_distance   

            # mode select:
            if 'P' in data.keys() and data['P'] == True:
                if mode != 'follow':
                    mode = 'follow'
                    print(f"change mode to: {mode}")
            else:
                if mode != None:
                    mode = None
                    print(f"change mode to: {mode}")

#. Write the ``follow()`` and ``get_dir()`` functions to make the car go in a different direction based on the sonar detection.

    .. note::
        The explanation of the ``get_dir()`` function can be found in :ref:`py_follow`.

    .. code-block:: python

        '''------- get_dir (sonar sacn data to direction) ---------------------'''
        def get_dir(sonar_data, split_str="0"):
            # get scan status of 0, 1
            sonar_data = [str(i) for i in sonar_data]
            sonar_data = "".join(sonar_data)

            # Split 0, leaves the free path
            paths = sonar_data.split(split_str)

            # Calculate where is the widest
            max_paths = max(paths)
            if split_str == "0" and len(max_paths) < 4:
                return "left"
            elif split_str == "1" and len(max_paths) < 2:
                return "stop"

            # Calculate the direction of the widest
            pos = sonar_data.index(max_paths)
            pos += (len(max_paths) - 1) / 2
            delta = len(sonar_data) / 3
            if pos < delta:
                return "left"
            elif pos > 2 * delta:
                return "right"
            else:
                return "forward"

        '''----------------- follow ---------------------'''
        def follow():
            global sonar_angle, sonar_distance

            sonar.set_sonar_scan_config(FOLLOW_SCAN_ANGLE, FOLLOW_SCAN_STEP)
            sonar.set_sonar_reference(FOLLOW_REFERENCE)

            #--------- scan -----------
            sonar_angle, sonar_distance, sonar_data = sonar.sonar_scan()
            # time.sleep(0.02)

            # If sonar data return a int, means scan not finished, and the int is current angle status
            if isinstance(sonar_data, int):
                return

            #---- analysis direction -----
            direction = get_dir(sonar_data, split_str='1')

            #--------- move ------------
            if direction == "left":
                car.move("left", FOLLOW_TURNING_POWER)
            elif direction == "right":
                car.move("right", FOLLOW_TURNING_POWER)
            elif direction == "forward":
                car.move("forward", FOLLOW_FORWARD_POWER)
            else:
                car.move("stop")

#. In ``remote_handler()`` function, the ``follow()`` function will be called if the follow mode is turned on, otherwise the car is stopped.


    .. code-block:: python

        def remote_handler():

            ''' follow hand '''
            if mode == 'follow':
                follow()       

            ''' no operation '''
            if mode == None:
                car.move('stop')