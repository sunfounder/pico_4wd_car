from machine import Timer, Pin
import math

class Speed():

    WP = 2.0 * math.pi * 3.3 # wheel_perimeter(cm): 2 * pi * r
    TIMER = 200 # ms, Timer interval

    def __init__(self, pin1, pin2):
        self.left_count = 0
        self.right_count = 0
        # Count per second
        self.left_cps = 0
        self.right_cps = 0
        self.speed = 0
        self.left_speed = 0
        self.right_speed = 0
        self.left_pin = Pin(pin1, Pin.IN, Pin.PULL_UP)
        self.right_pin = Pin(pin2, Pin.IN, Pin.PULL_UP)
        self.tim = Timer()
        self.left_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.on_left)
        self.right_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.on_right)
        self.tim.init(period=self.TIMER, mode=Timer.PERIODIC, callback=self.on_timer)
        self.mileage = 0
        
    def on_left(self, ch):
        if self.left_pin.value() == 0:
            self.left_count += 1

    def on_right(self, ch):
        if self.right_pin.value() == 0:
            self.right_count += 1

    def on_timer(self, ch):
        self.left_cps = (self.left_count) * (1000 / self.TIMER)
        self.left_rps = self.left_cps / 20.0
        self.left_speed = round(self.left_rps * self.WP, 2)
        self.right_cps = (self.right_count) * (1000 / self.TIMER)
        self.right_rps = self.right_cps / 20.0
        self.right_speed = round(self.right_rps * self.WP, 2)
        self.speed = round((self.left_speed + self.right_speed) / 2, 2)
        self.mileage += self.speed * (self.TIMER/1000)/ 100 # change unit to: meter
        self.left_count = 0
        self.right_count = 0

    def get_speed(self):
        return self.speed

    def get_mileage(self):
        return self.mileage

    def set_mileage(self, value):
        self.mileage = value

