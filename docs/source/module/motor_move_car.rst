4. Move the Car
=================

Previously, we have learned how to make a single motor turn at different speeds.

In this project, we will learn how 4 motors work together to make the Pico 4WD car go forward, backward, left and right.


You can push the Pico 4WD car forward to see how the 4 wheels (motors) are turning. You will find that the two wheels (motors) on the left side are turning counterclockwise, while the two wheels (motors) on the right side are turning clockwise.

So you can use a parameter to determine whether the motor is on the left or the right side, and thus set its direction of rotation.


**Move Forward** (``motor_4_forward.py``)

    * Here, create a function ``motor_run()`` to control the movement of the car, and use the parameter ``position`` to determine the position of the motors.
    * When ``position`` > 0, it means the corresponding motor is on the **right side**, so let the motor turn clockwise.
    * When ``position`` < 0, it means the corresponding motor is on the **left side**, so let the motor turn counterclockwise.


    .. code-block:: python
        :emphasize-lines: 14,18

        import machine
        import time

        pin = []
        motor_pin = [17,16,15,14,13,12,11,10]

        for i in range(8):
            pin.append(None)
            pin[i] = machine.PWM(machine.Pin(motor_pin[i],machine.Pin.OUT))
            pin[i].freq(20000)

        def motor_run(power,pinA,pinB,position):
            power= int(power/100.0*0xFFFF)
            if position>0:
                # clockwise
                pinA.duty_u16(0xFFFF-power)
                pinB.duty_u16(0xFFFF)
            elif position<0:
                # anticlockwise
                pinA.duty_u16(0xFFFF)
                pinB.duty_u16(0xFFFF-power)

        try:

            power = 50

            # forward
            motor_run(power,pin[0],pin[1],-1) #left front
            motor_run(power,pin[2],pin[3],1) #right front
            motor_run(power,pin[4],pin[5],-1) #left rear
            motor_run(power,pin[6],pin[7],1) #right rear
            time.sleep(2)

        finally:
                # stop
            power = 0
            motor_run(power,pin[0],pin[1],-1) #left front
            motor_run(power,pin[2],pin[3],1) #right front
            motor_run(power,pin[4],pin[5],-1) #left rear
            motor_run(power,pin[6],pin[7],1) #right rear


    * Copy the above code into Thonny or open the ``motor_4_forward.py`` under the path of ``pico_4wd_car-v2.0\examples\learn_modules``.
    * After running and powering up the Pico 4WD car, you will see the car move forward.

    .. note::
        In order to allow the car to move on the ground without the USB cable connected, you need to save this script as ``main.py`` to Raspberry Pi Pico, see :ref:`run_script_offline` for a tutorial.



**Move Backward**

    * As well as forward, the car also has stop, backward, and steering situations. To reverse the direction of the motor, we would normally write a negative number to power, but the above code would return errors.
    * Therefore, the above code requires one more layer of conditional judgment, as shown below.

    .. code-block:: python
        :emphasize-lines: 12,13,16,21

        import machine
        import time

        pin = []
        motor_pin = [17,16,15,14,13,12,11,10]

        for i in range(8):
            pin.append(None)
            pin[i] = machine.PWM(machine.Pin(motor_pin[i],machine.Pin.OUT))
            pin[i].freq(20000)

        def motor_run(power,pinA,pinB,position):
            value= int(abs(power)/100.0*0xFFFF)
            if position*power>0:
                # clockwise
                pinA.duty_u16(0xFFFF-value)
                pinB.duty_u16(0xFFFF)
            elif position*power<0:
                # anticlockwise
                pinA.duty_u16(0xFFFF)
                pinB.duty_u16(0xFFFF-value)
            elif position*power==0:
                # stop
                pinA.duty_u16(0xFFFF)
                pinB.duty_u16(0xFFFF)


        try:

            power = 50

            # backward
            motor_run(-power,pin[0],pin[1],-1) #left front
            motor_run(-power,pin[2],pin[3],1) #right front
            motor_run(-power,pin[4],pin[5],-1) #left rear
            motor_run(-power,pin[6],pin[7],1) #right rear
            time.sleep(2)
            
        finally:
                # stop
            power = 0
            motor_run(power,pin[0],pin[1],-1) #left front
            motor_run(power,pin[2],pin[3],1) #right front
            motor_run(power,pin[4],pin[5],-1) #left rear
            motor_run(power,pin[6],pin[7],1) #right rear


    The car can now go backward, turn left or right by changing the positive and negative values of ``power``.

**About the Steering** 

The movement of the Pico 4WD car is controlled by 4 motors. So you have two ways to make it steer. 

Take turning right as an example

#. The left motors turn clockwise and the right motors turn counterclockwise.

    .. code-block:: python

        power = 50

        # turn right
        motor_run(power,pin[0],pin[1],-1) #left front
        motor_run(-power,pin[2],pin[3],1) #right front
        motor_run(power,pin[4],pin[5],-1) #left rear
        motor_run(-power,pin[6],pin[7],1) #right rear

#. The speed of the left motors is greater than the speed of the right motors.

    .. code-block:: python

        power = 80

        # also turn right
        motor_run(power,pin[0],pin[1],-1) #left front
        motor_run(power/2,pin[2],pin[3],1) #right front
        motor_run(power,pin[4],pin[5],-1) #left rear
        motor_run(power/2,pin[6],pin[7],1) #right rear