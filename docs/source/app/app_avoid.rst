9. APP - Avoid
===============

Pico 4WD can avoid obstacles automatically!

When an obstacle is detected, instead of simply backing up, 
the sonar scans the surrounding area and finds the widest way 
to move forward.


**Quick User Guide**

#. Run the ``app_8_follow.py`` file under the ``pico_4wd_car\examples\app_control`` path and then power on the Pico 4WD car.

#. As shown below, create a controller that adds **Radar**, **Number**, and **Button** widgets to the **D**, **J**, and **O** areas, respectively.

    .. image:: img/APP_DB_9_1.png

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. As soon as you toggle the **Switch** widget in the **O** area to ON, the Pico 4WD car will move forward freely and change direction automatically when it encounters obstacles.


**How it works?**


#. In ``on_receive(data)``, the distances and angles are sent to the **D**  and **J** areas for showing, then responding to the data from the **P** area.


    .. code-block:: python

        '''----------------- on_receive (ws.loop()) ---------------------'''
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
            if 'O' in data.keys() and data['O'] == True:
                if mode != 'obstacle avoid':
                    mode = 'obstacle avoid'
                    sonar.set_sonar_reference(OBSTACLE_AVOID_REFERENCE)
                    print(f"change mode to: {mode}")
            else:
                if mode != None:
                    mode = None
                    print(f"change mode to: {mode}")
        

#. Write the ``obstacle_avoid()`` and ``get_dir()`` functions to make the car go in a different direction based on the sonar detection.

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

    '''----------------- obstacle_avoid ---------------------'''
    def obstacle_avoid():
        global sonar_angle, sonar_distance, avoid_proc, avoid_has_obstacle

        # scan
        if avoid_proc == 'scan':
            if not avoid_has_obstacle:
                sonar.set_sonar_scan_config(OBSTACLE_AVOID_SCAN_ANGLE, OBSTACLE_AVOID_SCAN_STEP)
                car.move('forward', OBSTACLE_AVOID_FORWARD_POWER)
            else:
                sonar.set_sonar_scan_config(180, OBSTACLE_AVOID_SCAN_STEP)
                car.move('stop')
            sonar_angle, sonar_distance, sonar_data = sonar.sonar_scan()
            if isinstance(sonar_data, int):
                # 0 means distance too close, 1 means distance safety
                if sonar_data == 0:
                    avoid_has_obstacle = True
                    return
                else:
                    return
            else:
                avoid_proc = 'getdir'

        # getdir
        if avoid_proc == 'getdir':
            avoid_proc = get_dir(sonar_data)
        # move: stop, forward
        if avoid_proc == 'stop':
            avoid_has_obstacle = True
            car.move('stop')
            avoid_proc = 'scan'
        elif avoid_proc == 'forward':
            avoid_has_obstacle = False
            car.move('forward', OBSTACLE_AVOID_FORWARD_POWER)
            avoid_proc = 'scan'
        elif avoid_proc == 'left' or avoid_proc == 'right':
            avoid_has_obstacle = True
            if avoid_proc == 'left':
                car.move('left', OBSTACLE_AVOID_TURNING_POWER)
                sonar_angle = 20 # servo turn right 20 
            else:
                car.move('right', OBSTACLE_AVOID_TURNING_POWER)
                sonar_angle = -20 # servo turn left 20 
            sonar.servo.set_angle(sonar_angle)
            time.sleep(0.2)
            avoid_proc = 'turn'

        # turn: left, right
        if avoid_proc == 'turn':
            sonar_distance = sonar.get_distance_at(sonar_angle)
            status = sonar.get_sonar_status(sonar_distance)
            if status == 1:
                avoid_has_obstacle = False
                avoid_proc = 'scan'
                car.move("forward", OBSTACLE_AVOID_FORWARD_POWER)
                sonar.servo.set_angle(0)


#. In ``remote_handler()`` function, the ``obstacle_avoid()`` function will be called if the obstacle avoid mode is turned on, otherwise the car is stopped.


    .. code-block:: python

        def remote_handler():

            ''' enable avoid function '''
            if mode == 'obstacle avoid':
                obstacle_avoid()      
            
            ''' no operation '''
            if mode is None:
                car.move('stop')
