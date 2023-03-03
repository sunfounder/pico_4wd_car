5. Detecting Distance
=============================

In this project, we will show you how to make the ultrasonic module detect the distance of the obstacle ahead.

The transmitting probe of the ultrasonic module emits high-frequency sound waves (ultrasonic waves), which are reflected back and detected by the receiving probe when they touch an object.

By calculating the time from the emission to the reception of ultrasonic waves, multiplied by the speed of sound, the distance of the obstacle can be obtained.

**Code**

.. code-block:: python

    import machine
    import time

    trig = machine.Pin(6,machine.Pin.OUT)
    echo = machine.Pin(7,machine.Pin.IN)

    def distance():
        # pulse
        trig.high()
        time.sleep_us(10)
        trig.low()

        # get time
        pulse_width_us = machine.time_pulse_us(echo, machine.Pin.on) 
        pulse_width_s= pulse_width_us/ 1000000.0

        # calculate the distance
        distance_m = pulse_width_s * 340 / 2
        distance_cm = (distance_m *100)

        return distance_cm

    while True:
        dis = distance()
        print ('Distance: %.2f' % dis)
        time.sleep_ms(300)

You can copy the above code into Thonny or open the ``sonar_5_get_distance.py`` under the path of ``pico_4wd_car-v2.0\examples\learn_modules``. Then click the |thonny_run| button or press ``F5`` to run it.

After powering up the Pico 4WD, move the obstacle in front of it back and forth to verify the distance value (unit: cm).