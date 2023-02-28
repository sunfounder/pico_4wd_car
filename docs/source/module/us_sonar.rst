7. ``sonar.py`` Module
==========================

Combine the servo and ultrasonic module and you get a mechanical scanning sonar.

.. note::

    The final encapsulated library ``sonar.py`` has been saved in ``pico_4wd_car-v2.0\libs``, which may differ from the ones shown in the course, so please refer to the file under ``libs`` path when using it.

You can learn how ``sonar.py`` is encapsulated in the following steps.

**1. sonar scanning**

The Pico 4WD Car scans for obstacles within 180° of the front. Simply put, the servo rotates back and forth and the ultrasonic module detects every specific angle.

.. code-block:: python

    from servo import Servo
    from ultrasonic import Ultrasonic
    import time

    servo = Servo(18)
    sonar = Ultrasonic(6, 7)

    sonar_angle = 0
    sonar_step = 30

    def get_distance_at(angle):
        global sonar_angle
        sonar_angle = angle
        servo.set_angle(sonar_angle)
        #time.sleep(0.04)
        while True: # avoid negative invalid values
            distance = sonar.get_distance()
            if distance > 0:
                return distance

    def sonar_move():
        global sonar_angle, sonar_step
        sonar_angle += sonar_step
        if sonar_angle >= 90:
            sonar_angle = 90
            sonar_step *= -1
        elif sonar_angle <= -90:
            sonar_angle = -90
            sonar_step *= -1 

    while True:
        sonar_move()
        distance = get_distance_at(sonar_angle)
        print("angle: ",sonar_angle, "   distance: ",distance)
        time.sleep(0.3)

**2. Output distances together**

For more comprehensive data, we need to have the distances detected in each direction output together.

.. code-block:: python
    :emphasize-lines: 14,15,16,41,42,43,44,45,46,47

    from servo import Servo
    from ultrasonic import Ultrasonic
    import time

    servo = Servo(18)
    sonar = Ultrasonic(6, 7)

    sonar_angle = 0
    sonar_step = 30

    sonar_MAX_ANGLE = 90
    sonar_MIN_ANGLE = -90

    sonar_data =[]
    for i in range((sonar_MAX_ANGLE-sonar_MIN_ANGLE)/sonar_step+1):
        sonar_data.append(None)

    def get_distance_at(angle):
        global sonar_angle
        sonar_angle = angle
        servo.set_angle(sonar_angle)
        #time.sleep(0.04)
        while True: # avoid negative invalid values
            distance = sonar.get_distance()
            if distance > 0:
                return distance

    def sonar_move():
        global sonar_angle, sonar_step
        if sonar_angle >= sonar_MAX_ANGLE:
            sonar_angle = sonar_MAX_ANGLE
            sonar_step = -abs(sonar_step)
        elif sonar_angle <= sonar_MIN_ANGLE:
            sonar_angle = sonar_MIN_ANGLE
            sonar_step = abs(sonar_step)
        sonar_angle += sonar_step

    def mapping(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def sonar_scan():
        global sonar_data
        sonar_move()
        distance = get_distance_at(sonar_angle)
        index= int(mapping(sonar_angle, sonar_MIN_ANGLE, sonar_MAX_ANGLE, 0, len(sonar_data)-1))
        sonar_data[index]=distance
        return sonar_data

    while True:
        print(sonar_scan())
        time.sleep(0.3)

**3. Determine if there are obstacles**

Most of the time, the car only needs to know whether there are obstacles in all directions.   

.. code-block:: python
    :emphasize-lines: 13,52,53

    from servo import Servo
    from ultrasonic import Ultrasonic
    import time

    servo = Servo(18)
    sonar = Ultrasonic(6, 7)

    sonar_angle = 0
    sonar_step = 30

    sonar_MAX_ANGLE = 90
    sonar_MIN_ANGLE = -90
    sonar_REFERENCE = 20

    sonar_data =[]
    for i in range((sonar_MAX_ANGLE-sonar_MIN_ANGLE)/sonar_step+1):
        sonar_data.append(None)

    def get_distance_at(angle):
        global sonar_angle
        sonar_angle = angle
        servo.set_angle(sonar_angle)
        #time.sleep(0.04)
        while True: # avoid negative invalid values
            distance = sonar.get_distance()
            if distance > 0:
                return distance

    def sonar_move():
        global sonar_angle, sonar_step
        if sonar_angle >= sonar_MAX_ANGLE:
            sonar_angle = sonar_MAX_ANGLE
            sonar_step = -abs(sonar_step)
        elif sonar_angle <= sonar_MIN_ANGLE:
            sonar_angle = sonar_MIN_ANGLE
            sonar_step = abs(sonar_step)
        sonar_angle += sonar_step

    def get_sonar_status(distance):
        if distance > sonar_REFERENCE:
            return 1
        else:
            return 0

    def mapping(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def sonar_scan():
        global sonar_data
        sonar_move()
        distance = get_distance_at(sonar_angle)
        index= int(mapping(sonar_angle, sonar_MIN_ANGLE, sonar_MAX_ANGLE, 0, len(sonar_data)-1))
        status=get_sonar_status(distance)
        sonar_data[index]=status
        return sonar_data

    while True:
        print(sonar_scan())
        time.sleep(0.1)

**4. Get complete data before judging**

Additionally, if we use ``sonar_data`` directly for obstacle determination, the data on the left becomes an interference item when the left side obstacle disappears and the sonar scans the right side.

It makes more sense to determine an obstacle after a sonar cycle has been scanned and complete data has been collected.

.. code-block:: python
    :emphasize-lines: 14,15,16,17,20,21

    from servo import Servo
    from ultrasonic import Ultrasonic
    import time

    ...

    def sonar_scan():
        global sonar_data
        sonar_move()
        distance = get_distance_at(sonar_angle)
        index=int(mapping(sonar_angle, sonar_MIN_ANGLE, sonar_MAX_ANGLE, 0, len(sonar_data)-1))
        status=get_sonar_status(distance)
        sonar_data[index]=status
        if (index == 0 or index == len(sonar_data)-1) and None not in sonar_data:
            return sonar_angle,distance,sonar_data
        else:
            return sonar_angle,distance,status

    while True:
        _,_,result = sonar_scan()
        if type(result) is not int:
            print(result)
        time.sleep(0.1)


**5. Further optimization**

In order to be compatible with more complex programs, we created two more functions to modify the rotation rules and distance determination of the sonar.

.. code-block:: python
    :emphasize-lines: 8,33,40,41

    from servo import Servo
    from ultrasonic import Ultrasonic
    import time

    ...
    ...

    def set_sonar_scan_config(scan_range=None,step=None):
        global sonar_MAX_ANGLE, sonar_MIN_ANGLE, sonar_angle, sonar_step, sonar_data
        
        # update changed
        item = 0
        if scan_range is None or scan_range is sonar_MAX_ANGLE-sonar_MIN_ANGLE:
            item+=1
        else:
            sonar_MAX_ANGLE = int(scan_range / 2)
            sonar_MIN_ANGLE = sonar_MAX_ANGLE-scan_range
        if step is None or abs(sonar_step) is abs(step):
            item+=1
        else:
            sonar_step=int(step)
        if item is 2: # if nothing change, return
            return
        
        # re-create the data list
        sonar_data =[]
        for i in range(scan_range/abs(sonar_step) +1):
            sonar_data.append(None)
        
        sonar_angle=0
        servo.set_angle(sonar_angle)

    def set_sonar_reference(ref):
        global sonar_REFERENCE
        sonar_REFERENCE = int(ref)


    if __name__ == '__main__':
        try:
            set_sonar_scan_config(180,30)
            set_sonar_reference(20)
            while True:
                _,_,status = sonar_scan()
                if type(status) is not int:
                    print(status)
                time.sleep(0.1)
        finally:
            servo.set_angle(0)


That's all the steps, the complete code for ``sonar.py`` is located in the ``pico_4wd_car-v2.0\libs`` path.