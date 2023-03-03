5. ``motor.py`` Module (Control Motor)
===============================================


When Pico 4WD's various components work together, the code can be very long and difficult to understand.

So here we will learn how to encapsulate the motor code into a module (library), so that later we can import the library and call the functions inside.


The steps are as follows.

#. Now encapsulate the motor code from the previous project as ``Motor()`` |link_class|.

    .. code-block:: python

        from machine import Pin, PWM

        def mapping(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        class Motor():
            def __init__(self, pin_a, pin_b, dir=1):
                self.pwm1 = PWM(Pin(pin_a, Pin.OUT))
                self.pwm2 = PWM(Pin(pin_b, Pin.OUT))
                self.pwm1.freq(20000)
                self.pwm2.freq(20000)
                self.dir = dir

            def run(self, power:int):
                if power == 0:
                    self.pwm1.duty_u16(0xffff)
                    self.pwm2.duty_u16(0xffff)
                else:
                    value = mapping(abs(power), 0, 100, 20, 100) # power less than 20 is useless
                    value = int(value / 100.0 * 0xffff)

                    if power*self.dir > 0:
                        self.pwm1.duty_u16(0xffff - value)
                        self.pwm2.duty_u16(0xffff)
                    else:
                        self.pwm1.duty_u16(0xffff)
                        self.pwm2.duty_u16(0xffff - value)

#. To use this class, first declare four ``Motor`` objects.

    .. code-block:: python

        left_front  = Motor(17, 16, dir=-1)
        right_front = Motor(15, 14, dir= 1)
        left_rear   = Motor(13, 12, dir=-1)
        right_rear  = Motor(11, 10, dir= 1)    

#. Then use the ``run()`` function to get the individual motors to turn. Here the speed is set to a positive ``power(80)``, so the car will move forward.

    .. code-block:: python

        power = 80
        left_front.run(power)
        right_front.run(power)
        left_rear.run(power)
        right_rear.run(power)


#. Then, the complete code is shown below.

    .. code-block:: python

        from machine import Pin, PWM


        def mapping(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        class Motor():
            def __init__(self, pin_a, pin_b, dir=1):
                self.pwm1 = PWM(Pin(pin_a, Pin.OUT))
                self.pwm2 = PWM(Pin(pin_b, Pin.OUT))
                self.pwm1.freq(20000)
                self.pwm2.freq(20000)
                self.dir = dir

            def run(self, power:int):
                if power == 0:
                    self.pwm1.duty_u16(0xffff)
                    self.pwm2.duty_u16(0xffff)
                else:
                    value = mapping(abs(power), 0, 100, 20, 100)
                    value = int(value / 100.0 * 0xffff)

                    if power*self.dir > 0:
                        self.pwm1.duty_u16(0xffff - value)
                        self.pwm2.duty_u16(0xffff)
                    else:
                        self.pwm1.duty_u16(0xffff)
                        self.pwm2.duty_u16(0xffff - value)

        if __name__ == '__main__':

            # init
            left_front  = Motor(17, 16, dir=-1)
            right_front = Motor(15, 14, dir= 1)
            left_rear   = Motor(13, 12, dir=-1)
            right_rear  = Motor(11, 10, dir= 1)

            try:
                # forward
                power = 80
                left_front.run(power)
                right_front.run(power)
                left_rear.run(power)
                right_rear.run(power)  
                time.sleep(5)

            finally:
                # stop
                power = 0
                left_front.run(power)
                right_front.run(power)
                left_rear.run(power)
                right_rear.run(power) 
                time.sleep(0.2)  

#. Now, create a new script on Thonny. Copy all the above code into this script. After pressing ``Ctrl+S``, select **Raspberry Pi Pico** as the save path.

    .. image:: img/motor_class2.png

#. Fill in ``motor.py`` as the filename.

    .. note::

        * You will notice that the Raspberry Pi Pico already has a file called ``motor.py`` in it.

        * The Pico 4WD car already has the modules(libraries) pre-installed, so it can be played right out of the box.

        * So here you can choose to overwrite to the original file.

    .. image:: img/motor_class1.png

#. To run the script, click the |thonny_run| button or press ``F5``. When you power up the Pico 4WD car, you will see it move forward.

.. warning::

    At the moment, this ``motor.py`` is not the final version. It needs a smooth speed effect, which is included in the :ref:`motor_speed_smooth` project.