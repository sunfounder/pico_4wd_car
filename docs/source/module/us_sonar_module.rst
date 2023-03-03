8. ``sonar.py`` Module
==========================
In the previous project, we learned how the sonar scanner detects obstacles. That is the servo is turned from left to right and the ultrasonic module detects every specific angle, then several sets of distance values are output at once.

However, this kind of data is not very convenient for calculation, so in practice, we can set a threshold value, and then compare the detected distance against this threshold value, and then output a ``0`` or ``1``.

In this way, we encapsulate the sonar scanning code into a library and then add more calculations to it, so that it can be easily imported for use in the project.


.. note::

    The final encapsulated library ``sonar.py`` has been saved in ``pico_4wd_car-v2.0\libs``, which may differ from the ones shown in the course, so please refer to the file under ``libs`` path when using it.


You can learn how ``sonar.py`` is encapsulated in the following steps.

**1. Determine if there are obstacles**

    * Most of the time, the car only needs to know whether there are obstacles in all directions.
    * So here set a distance threshold with the variable ``SONAR_REFERENCE``.
    * And then create the function ``get_sonar_status()`` to determine if the distance is greater than the threshold, then output ``1``, otherwise output ``0``.
    * Then output the processed data at once, and you get array like this ``[1, 0, 0, 1, 1, 1, 1]``.

    .. code-block:: python
        :emphasize-lines: 13,40,41,42,43,44,54,55

        from servo import Servo
        from ultrasonic import Ultrasonic
        import time

        servo = Servo(18)
        ultrasonic = Ultrasonic(6, 7)

        sonar_angle = 0
        sonar_step = 30

        SONAR_MAX_ANGLE = 90
        SONAR_MIN_ANGLE = -90
        SONAR_REFERENCE = 20

        sonar_data =[]
        for i in range((SONAR_MAX_ANGLE-SONAR_MIN_ANGLE)/sonar_step+1):
            sonar_data.append(None)

        def get_distance_at(angle):
            global sonar_angle
            sonar_angle = angle
            servo.set_angle(sonar_angle)
            #time.sleep(0.04)
            distance = ultrasonic.get_distance()
            if distance < 0:
                return -1
            else:
                return distance

        def sonar_move():
            global sonar_angle, sonar_step
            if sonar_angle >= SONAR_MAX_ANGLE:
                sonar_angle = SONAR_MAX_ANGLE
                sonar_step = -abs(sonar_step)
            elif sonar_angle <= SONAR_MIN_ANGLE:
                sonar_angle = SONAR_MIN_ANGLE
                sonar_step = abs(sonar_step)
            sonar_angle += sonar_step

        def get_sonar_status(distance):
            if distance > SONAR_REFERENCE or distance < 0:
                return 1
            else:
                return 0

        def mapping(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        def sonar_scan():
            global sonar_data
            sonar_move()
            distance = get_distance_at(sonar_angle)
            index= int(mapping(sonar_angle, SONAR_MIN_ANGLE, SONAR_MAX_ANGLE, 0, len(sonar_data)-1))
            status=get_sonar_status(distance)
            sonar_data[index]=status
            return sonar_data

        while True:
            print(sonar_scan())
            time.sleep(0.1)




**2. Get complete data before judging**

    Additionally, if we use ``sonar_data`` directly for obstacle determination, the data on the left becomes an interference item when the left side obstacle disappears and the sonar scans the right side.

    It makes more sense to determine an obstacle after a sonar cycle has been scanned and complete data has been collected.

    .. code-block:: python
        :emphasize-lines: 21,22,23,24,27,28

        ...
        ...

        def get_distance_at(angle):
            ...

        def sonar_move():
            ...
        def get_sonar_status(distance):
            ...
        def mapping(x, in_min, in_max, out_min, out_max):
            ...

        def sonar_scan():
            global sonar_data
            sonar_move()
            distance = get_distance_at(sonar_angle)
            index=int(mapping(sonar_angle, SONAR_MIN_ANGLE, SONAR_MAX_ANGLE, 0, len(sonar_data)-1))
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


**3. Further optimization**

    In order to be compatible with more complex programs, we created two more functions to modify the rotation rules and distance determination of the sonar.

    .. code-block:: python
        :emphasize-lines: 16,41,48,49

        ...
        ...

        def get_distance_at(angle):
            ...

        def sonar_move():
            ...
        def get_sonar_status(distance):
            ...
        def mapping(x, in_min, in_max, out_min, out_max):
            ...
        def sonar_scan():
            ...

        def set_sonar_scan_config(scan_range=None,step=None):
            global SONAR_MAX_ANGLE, SONAR_MIN_ANGLE, sonar_angle, sonar_step, sonar_data
            
            # update changed
            item = 0
            if scan_range is None or scan_range is SONAR_MAX_ANGLE-SONAR_MIN_ANGLE:
                item+=1
            else:
                SONAR_MAX_ANGLE = int(scan_range / 2)
                SONAR_MIN_ANGLE = SONAR_MAX_ANGLE-scan_range
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

        def set_SONAR_REFERENCE(ref):
            global SONAR_REFERENCE
            SONAR_REFERENCE = int(ref)


        if __name__ == '__main__':
            try:
                set_sonar_scan_config(180,30)
                set_SONAR_REFERENCE(20)
                while True:
                    _,_,status = sonar_scan()
                    if type(status) is not int:
                        print(status)
                    time.sleep(0.1)
            finally:
                servo.set_angle(0)