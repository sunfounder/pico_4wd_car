
4. ``speed.py`` Module
=======================

Similarly, in order to keep the code simple and organized when using the speed module with other modules, we have encapsulated all its related code into a library.

When you use it, you just need to import this library, and you can call the functions inside directly.

.. code-block:: python

    get_speed()
    get_mileage()

.. note::

    The encapsulated library ``speed.py`` has been saved in ``pico_4wd_car-v2.0\libs``, which may differ from the ones shown in the course, so please refer to the file under ``libs`` path when using it.


.. code-block:: python

    from machine import Timer, Pin
    import math

    class Speed():

        WP = 2 * math.pi * 3.3 # wheel_perimeter(cm): 2 * pi * r
        duration = 200 # ms, Timer interval
        
        def __init__(self, pin1, pin2):
            # value for return
            self.total_count = 0
            self.speed = 0

            # Interrupter, used to count        
            self.left_count = 0
            self.right_count = 0
            self.left_pin = Pin(pin1, Pin.IN, Pin.PULL_UP)
            self.left_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.on_left)
            self.right_pin = Pin(pin2, Pin.IN, Pin.PULL_UP)
            self.right_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.on_right)

            # Timer, print speed
            self.tim = Timer()
            self.tim.init(period=self.duration, mode=Timer.PERIODIC, callback=self.on_timer)   

        def on_left(self,ch):
            self.left_count += 1

        def on_right(self,ch):
            self.right_count += 1

        def on_timer(self,ch):
            # mileage
            self.total_count += self.left_count + self.right_count
            # revolutions per second
            rps = (self.left_count + self.right_count) * 1000 /self.duration /20.0 /2
            # speed
            self.speed = rps * self.WP
            # clear count
            self.left_count = 0
            self.right_count = 0

        def get_speed(self): # Unit: cm/s
            return self.speed

        def get_mileage(self): # Unit: m
            return self.total_count /20.0/2 * self.WP /100

        def reset_mileage(self):
            self.total_count = 0

    # init 
    sp = Speed(8, 9)

    # detect
    try:
        import motors
        import time
        while True:
            for i in range(20,100):
                power = round(i / 10) * 10
                motors.move("forward",power)
                print(f'Power(%%):{power}  Speed(cm/s):{sp.get_speed():.2f} Mileage(m):{sp.get_mileage():.2f}')
                time.sleep(0.2)
    finally:
        motors.stop()
        time.sleep(0.2) 

