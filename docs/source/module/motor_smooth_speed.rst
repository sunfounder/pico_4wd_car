.. _motor_speed_smooth:

7. Smooth Speed Effect
=====================================

The motor is a high power device and will generate high current during fast reversal, which may cause the Raspberry Pi Pico to not work.

Therefore, we need to add code for smooth speed in both ``motor.py`` and ``motors.py``.

.. note::
    You need to open ``motor.py`` and ``motors.py`` in Raspberry Pi Pico separately, add the following highlighted sections to them and save them.


* ``motor.py``


.. code-block:: python
    :emphasize-lines: 14,17

    from machine import Pin, PWM
    import time

    def mapping(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    class Motor():
        def __init__(self, pin_a, pin_b, dir=1):
            self.pwm1 = PWM(Pin(pin_a, Pin.OUT))
            self.pwm2 = PWM(Pin(pin_b, Pin.OUT))
            self.pwm1.freq(20000)
            self.pwm2.freq(20000)
            self.dir = dir
            self.current_power = 0

        def run(self, power:int):
            self.current_power = power
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

* ``motors.py``

.. code-block:: python
    :emphasize-lines: 22,29,30,31,32,33,34,35,36,37,38


    from motor import Motor
    import time

    left_front  = Motor(17, 16, dir=-1)
    right_front = Motor(15, 14, dir= 1)
    left_rear   = Motor(13, 12, dir=-1)
    right_rear  = Motor(11, 10, dir= 1)
    motors = [left_front, right_front, left_rear, right_rear]


    def set_motors_power(powers:list):
        ''' set motors power 
            powers list, 1*4 list powers of each motor, the order is [left_front, right_front, left_rear, right_rear]
        '''
        if len(powers) != 4:
            raise ValueError("powers should be a 1*4 list.")

        for i, motor in enumerate(motors):
            motor.run(powers[i])


    def set_motors_power_gradually(powers:list):
        '''
            slowly increase power of the motor, to avoid hight reverse voltage from motors
        '''
        if len(powers) != 4:
            raise ValueError("powers should be a 1*4 list.")

        flags = [True, True, True, True]
        while flags[0] or flags[1] or flags[2] or flags[3]:
            for i, motor in enumerate(motors):
                if motor.current_power > powers[i]:
                    motor.run(motor.current_power - 1)
                elif motor.current_power < powers[i]:
                    motor.run(motor.current_power + 1)
                else:
                    flags[i] = False
            time.sleep_ms(1)


    def stop():
        set_motors_power([0, 0, 0, 0])


    def move(action, power=0):
        if action == "forward":
            set_motors_power_gradually([power, power, power, power])
        elif action == "backward":
            set_motors_power_gradually([-power, -power, -power, -power])
        elif action == "left":
            set_motors_power_gradually([-power, power, -power, power])
        elif action == "right":
            set_motors_power_gradually([power, -power, power, -power])
        else:
            set_motors_power_gradually([0, 0, 0, 0])



    if __name__ == "__main__":
        speed = 50
        act_list = [
            "forward",
            "backward",
            "left",
            "right",
            "stop",
        ]
        for act in act_list:
            print(act)
            move(act, speed)
            time.sleep(1)




After optimizing the code, you still only need to write ``move(forward, 50)`` to make the car move, but avoid the damage caused by the motor's extremely fast reverse rotation.
