7. Sonar Scanning
==========================

In the previous projects, we have learned the servo and ultrasonic modules separately and encapsulated their related scripts into libraries.

In this project, we'll write scripts to make the servo and ultrasonic work together to output the distances of obstacles ahead at once.


**Code**

Simply put, the servo rotates back and forth and the ultrasonic module detects distances at specific angles.

To get more comprehensive data, we need to have the detected distances in each direction output together.


.. code-block:: python

    from servo import Servo
    from ultrasonic import Ultrasonic
    import time

    servo = Servo(18)
    ultrasonic = Ultrasonic(6, 7)

    sonar_angle = 0 # current angle
    sonar_step = 30 # Scan angle for each step

    SONAR_MAX_ANGLE = 90
    SONAR_MIN_ANGLE = -90

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

    def mapping(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def sonar_scan():
        global sonar_data
        sonar_move()
        distance = get_distance_at(sonar_angle)
        index= int(mapping(sonar_angle, SONAR_MIN_ANGLE, SONAR_MAX_ANGLE, 0, len(sonar_data)-1))
        sonar_data[index]=distance
        return sonar_data

    while True:
        print(sonar_scan())
        time.sleep(0.3)

You can copy the above code into Thonny or open the ``sonar_7_sonar_scan.py`` under the path of ``pico_4wd_car-v2.0\examples\learn_modules``. Then click the |thonny_run| button or press ``F5`` to run it.

When you power up the Pico 4WD car, you will see arrays like this ``[1, 0, 0, 1, 1, 1, 1]`` in the Shell.

**How it works?**

#. Import ``servo.py`` and ``ultrasonic.py``, and instantiate them. In addition, set the scan angle to -90 ~ 90, and the angle interval to 30°.

    .. code-block:: python


        from servo import Servo
        from ultrasonic import Ultrasonic
        import time

        servo = Servo(18)
        ultrasonic = Ultrasonic(6, 7)

        sonar_angle = 0 # current angle
        sonar_step = 30 # Scan angle for each step

        SONAR_MAX_ANGLE = 90
        SONAR_MIN_ANGLE = -90

#. Ultrasonic module detects every 30° as the servo rotates and returns ``distance``.

    .. code-block:: python

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

#. The ``sonar_move()`` here actually makes the servo rotate in the set angle range (-90 ~ 90) at 30° intervals.

    .. code-block:: python

        def sonar_move():
            global sonar_angle, sonar_step
            if sonar_angle >= SONAR_MAX_ANGLE:
                sonar_angle = SONAR_MAX_ANGLE
                sonar_step = -abs(sonar_step)
            elif sonar_angle <= SONAR_MIN_ANGLE:
                sonar_angle = SONAR_MIN_ANGLE
                sonar_step = abs(sonar_step)
            sonar_angle += sonar_step

#. Now to combine the above two functions, let the ultrasonic detect the distance while the servo is moving and output the 7 distance values as an array at once.

    .. code-block:: python

        def sonar_scan():
            global sonar_data
            sonar_move()
            distance = get_distance_at(sonar_angle)
            index= int(mapping(sonar_angle, SONAR_MIN_ANGLE, SONAR_MAX_ANGLE, 0, len(sonar_data)-1))
            sonar_data[index]=distance
            return sonar_data