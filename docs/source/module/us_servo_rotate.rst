2. Let Servo Rotate
=======================

In this chapter, we will show you how to make the servo work.


In a nutshell, to make the servo work you need to write 0.5ms to 2.5ms pulses to it every 20ms, for the principle see :ref:`cpn_servo` .

So we get the following code.

**Code**

.. code-block:: python

    import machine
    import time
    servo = machine.PWM(machine.Pin(18))
    servo.freq(50)
    def mapping(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    def set_angle(pin,angle):
        pulse_width=mapping(angle, -90, 90, 2.5,0.5)
        duty=int(mapping(pulse_width, 0, 20, 0,65535))
        pin.duty_u16(duty)
    for angle in range(0,180,5):
        set_angle(servo,angle)
        time.sleep(0.1)

You can copy the above code into Thonny or open the ``sonar_servo_2.1_rotate.py`` under the path of ``pico_4wd_car-v2.0\examples``. Then click the |thonny_run| button or press ``F5`` to run it.

When you power up the Pico 4WD car, you will see the servo rotate from 0° to 180°.


**How it works?**

Let's analyze this code.

* The servo needs to accept the signal in a 20ms cycle, which means setting a PWM with a frequency of 50Hz(1/20ms).

.. code-block:: python

    servo = machine.PWM(machine.Pin(18))
    servo.freq(50)

* Use the ``mapping()`` function to map the servo angle range (-90 ~ 90) to pulse width range (0.5 ~ 2.5ms).

.. code-block:: python

    pulse_width=mapping(angle, -90, 90, 0.5,2.5)

* Converts the pulse width from period to duty cycle. Since ``duty_u16()`` cannot be used with decimals (the value cannot be of floating point type), we use ``int()`` to force the duty to int type.

.. code-block:: python

    duty=int(mapping(pulse_width, 0, 20, 0,65535))
    pin.duty_u16(duty)