2. Get the Motor Rotating
=================================

**Principle of Motor Rotation**

As shown in :ref:`cpn_tt_motor`, the motors of the Pico 4WD Car are driven by the TC1508S chips.
The control pins corresponding to the 4 motors and the direction of rotation are shown below.

.. list-table:: **Motor-Pin List**

    *   - **Motor**
        - **PinA**
        - **PinB**
    *   - Left Front
        - GP17
        - GP16
    *   - Right Front
        - GP15
        - GP14
    *   - Left Rear
        - GP13
        - GP12
    *   - Right Rear
        - GP11
        - GP10

.. list-table:: **Motor Work**

    *   - **PinA**
        - **PinB**
        - **Work**
    *   - H
        - L
        - Rotate Clockwise(CW)
    *   - L
        - H
        - Rotate Counter-clockwise(CCW)
    *   - H
        - H
        - Stop

Now let's start writing the script to see how the motors turn.

**Motor Turns Clockwise**

#. Take Right Rear Motor for example, it is controlled by GP11 and GP10. Write ``low`` for GP11 and ``high`` for GP10.


    .. code-block:: python

        import machine

        pinA = machine.Pin(11, machine.Pin.OUT)
        pinB = machine.Pin(10, machine.Pin.OUT)

        pinA.low()
        pinB.high()

#. Copy the above code into Thonny or open the ``motor_2_cw.py`` under the path of ``pico_4wd_car-v2.0\examples\learn_modules``.

#. Use a micro USB cable to connect the Pico to your computer and select the "MicroPython (Raspberry Pi Pico) COMxx" interpreter.

    .. image:: img/sec_inter12.png

#. Click |thonny_run| button or simply press ``F5`` to run it.

#. Start the Pico 4WD car.

    * When first used or when the battery cable is unplugged, Pico RDP will activate its over-discharge protection circuitry(Unable to get power from battery).
    * Therefore, you'll need to plug in a Type-C cable for about 5 seconds to release the protection status.
    * At this time look at the battery indicators, if both battery indicators are off, please continue to plug in the Type-C cable to charge the battery.

        .. image:: img/pico_rdp_power.png

#. As you hold the Pico 4WD Car up high, you will be able to see the right rear motor turning clockwise.

Next you can run the following scripts in sequence to see what happens.

**Stop the Motor**

    Write two ``high`` levels, motor stops.

    .. code-block:: python

        import machine

        pinA = machine.Pin(11, machine.Pin.OUT)
        pinB = machine.Pin(10, machine.Pin.OUT)

        pinA.high()
        pinB.high()

**Motor Turns Counter-clockwise**

    Reversing the ``high`` and ``low`` levels, the motor will rotate counterclockwise.

    .. code-block:: python

        import machine

        pinA = machine.Pin(11, machine.Pin.OUT)
        pinB = machine.Pin(10, machine.Pin.OUT)

        pinA.high()
        pinB.low()

**Stop 4 Motors**

    Stop all motors.


    .. code-block:: python

        import machine

        for i in range(10,18):
            pin = machine.Pin(i, machine.Pin.OUT)
            pin.high()