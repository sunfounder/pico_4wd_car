from machine import Timer, Pin, PWM, ADC
from machine import time_pulse_us
import array, time
from rp2 import PIO, StateMachine, asm_pio
import math

import time

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Speed():

    # wheel_perimeter(cm): 2 * pi * r
    WP = 2.0 * math.pi * 3.3
    TIMER = 200

    def __init__(self, pin1, pin2):
        self.count = 0
        # Count per second
        self.cps = 0
        self.speed = 0
        left_pin = Pin(pin1, Pin.IN, Pin.PULL_UP)
        right_pin = Pin(pin2, Pin.IN, Pin.PULL_UP)
        self.tim = Timer()
        left_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.on_left)
        right_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.on_right)
        self.tim.init(period=self.TIMER, mode=Timer.PERIODIC, callback=self.on_timer)
        
    def on_left(self, ch):
        self.count += 1

    def on_right(self, ch):
        self.count += 1

    def on_timer(self, ch):
        self.cps = (self.count) / 2.0 * (1000 / self.TIMER)
        # 20 count per turn
        rps = self.cps / 20.0
        self.speed = round(rps * self.WP, 2)
        self.count =0

    def __call__(self):
        return self.speed

    def get_speed(self):
        return self.speed

class Servo():
    MAX_PW = 2500
    MIN_PW = 500
    PERIOD = 0xffff
    
    def __init__(self, pin):
        self.servo = PWM(Pin(pin, Pin.OUT))
        self.servo.freq(50)
        
    def set_angle(self, angle):
        try:
            angle = int(angle)
        except:
            raise ValueError("Angle value should be int value, not %s"%angle)
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        High_level_time = mapping(angle, -90, 90, self.MAX_PW, self.MIN_PW)
        pwr =  High_level_time / 20000
        value = int(pwr*self.PERIOD)
        self.servo.duty_u16(value)


class Ultrasonic():
    def __init__(self, trig_Pin, echo_Pin):
        """Initialize Input(echo) and Output(trig) Pins."""
        self._trig = Pin(trig_Pin, Pin.OUT)
        self._echo = Pin(echo_Pin, Pin.IN)
        self._sound_speed = 340.0  # m/s

    def _pulse(self):
        """Trigger ultrasonic module with 10us pulse."""
        self._trig.high()
        time.sleep_us(10)
        self._trig.low()

    def get_distance(self):
        """Measure pulse length and return calculated distance [cm]."""
        self._pulse()
        pulse_width_s = time_pulse_us(self._echo, Pin.on) / 10000
        #print(pulse_width_s)
        dis = (pulse_width_s / 2.0) * self._sound_speed
        return dis


class Motor():
    def __init__(self, pin_a, pin_b, dir=1):
        self.pin_1 = PWM(Pin(pin_a, Pin.OUT))
        self.pin_2 = PWM(Pin(pin_b, Pin.OUT))
        self.pin_1.freq(500)
        self.pin_2.freq(500)
        self.dir = dir
        self._power = 0
        self._value = 0

    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, power):
        self._power = power
        dir = -1 if power < 0 else 1
        value = abs(power)
        if value != 0:
            value = mapping(value, 0, 100, 30, 100)
        else:
            value = 0
        value = int(value / 100.0 * 0xffff)

        dir *= self.dir
        if power == 0:
            value = 0
        else:
            value = mapping(abs(power), 0, 100, 20, 100)
        value = int(value / 100.0 * 0xffff)
        if dir > 0:
            self.pin_1.duty_u16(0)
            self.pin_2.duty_u16(value)
        elif dir < 0:
            self.pin_1.duty_u16(value)
            self.pin_2.duty_u16(0)
        else:
            self.pin_1.duty_u16(0)
            self.pin_2.duty_u16(0)

    def set_motor_power(self, power):
        self.power = power


@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]

class WS2812():
    
    def __init__(self, pin, num):
        # Configure the number of WS2812 LEDs.
        self.led_nums = num
        self.pin = pin
        self.sm = StateMachine(0, ws2812, freq=8000000, sideset_base=self.pin)
        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)
        
        self.buf = array.array("I", [0 for _ in range(self.led_nums)])

    def write(self):
        self.sm.put(self.buf, 8)

    def write_all(self, value):
        for i in range(self.led_nums):
            self.__setitem__(i, value)
        self.write()

    def list_to_hex(self, color):
        if isinstance(color, list) and len(color) == 3:
            c = (color[0] << 8) + (color[1] << 16) + (color[2])
            return c
        elif isinstance(color, int):
            value = (color & 0xFF0000)>>8 | (color & 0x00FF00)<<8 | (color & 0x0000FF)
            return value
        else:
            raise ValueError("Color must be 24-bit RGB hex or list of 3 8-bit RGB, not %s"%color)

    def hex_to_list(self, color):
        if isinstance(color, list) and len(color) == 3:
            return color
        elif isinstance(color, int):
            r = color >> 8 & 0xFF
            g = color >> 16 & 0xFF
            b = color >> 0 & 0xFF
            return [r, g, b]
        else:
            raise ValueError("Color must be 24-bit RGB hex or list of 3 8-bit RGB, not %s"%color)

    def __getitem__(self, i):
        return self.hex_to_list(self.buf[i])

    def __setitem__(self, i, value):
        value = self.list_to_hex(value)
        self.buf[i] = value
