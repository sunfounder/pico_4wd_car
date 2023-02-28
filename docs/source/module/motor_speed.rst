3. Controlling the Speed of Motors
========================================

In the previous project, we can give high and low levels to the motor to make it spin or stop in a constant speed.

But how to set different speed?

**About PWM**

In this case, you can use |link_pwm|, it allows you to give analogue behaviours to digital devices, such as motors. This means that rather than motor being simply spin or stop, you can control its speed.

Happily, handling Pico PWM in MicroPython is very simple, requiring only three simple commands.

* Create a ``pin`` as a PWM object.

.. code-block:: python

    pin = machine.PWM(machine.Pin(17))

* Tell Raspberry Pi Pico how often to switch the power between ON and OFF.

.. code-block:: python

    pin.freq(20000)

* Tell the ``pin`` for how long it should be ON each time. For Raspberry Pi Pico in MicroPython, this can range from 0 to 65535. 655535 would be 100% of the time, a value of around 32727 indicates 50%.

.. code-block:: python

    pin.duty_u16(0xFFFF)


**Rotating the motor at high speed** (``motor_3.1_speed_high.py``)

    * Set pinB to high, i.e. PWM value is 0xFFFF (65535).
    * Then the motor will rotate clockwise by setting pinA to any value between 0 and 0xFFFF. In general, the smaller the value, the faster the speed, and the maximum speed is obtained at 0.

    .. code-block:: python

        import machine

        pinA = machine.Pin(17, machine.Pin.OUT)
        pinB = machine.Pin(16, machine.Pin.OUT)

        pwmA = machine.PWM(pinA) # Create PWM object
        pwmB = machine.PWM(pinB) # Create PWM object
        pwmA.freq(20000)
        pwmB.freq(20000)

        # fast
        pwmA.duty_u16(0x0000)
        pwmB.duty_u16(0xFFFF)


**Rotating motor at slow speed** (``motor_3.2_speed_low.py``)

    Now come and turn the left front motor clockwise in the same way, but you will find that it will spin much slower.

        .. code-block:: python

            import machine

            pinA = machine.Pin(13, machine.Pin.OUT)
            pinB = machine.Pin(12, machine.Pin.OUT)

            pwmA = machine.PWM(pinA)
            pwmB = machine.PWM(pinB)
            pwmA.freq(20000)
            pwmB.freq(20000)

            # slow
            pwmA.duty_u16(0xFFFF)
            pwmB.duty_u16(0xAAAA)

**Stop 4 Motors** (``motor_3.3_speed_stop_all.py``)

    To stop all motors, write ``0xFFFF`` to all PWM pins.

    .. code-block:: python

        import machine

        for i in range(10,18):
            pin = machine.PWM(machine.Pin(i, machine.Pin.OUT))
            pin.freq(20000)
            pin.duty_u16(0xFFFF)