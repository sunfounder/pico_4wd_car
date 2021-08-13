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

        # self.data = fileDB("data")
        # self._mileage = float(self.data.get("mileage", default=0))
        self._mileage = 0
        
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
        self._mileage += self.speed * (self.TIMER/1000)/ 100
        # self.data.set("mileage",  self._mileage)
        self.left_count = 0
        self.right_count = 0

    def __call__(self):
        return self.speed

    def get_speed(self):
        return self.speed

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        self._mileage = value
        # raise ValueError("Mileage changing is not allowed!")

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
        High_level_time = mapping(angle, 90, -90, self.MAX_PW, self.MIN_PW)
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
        self.pin_1.freq(20000)
        self.pin_2.freq(20000)
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
        value = 0xffff - value
        if dir > 0:
            self.pin_1.duty_u16(value)
            self.pin_2.duty_u16(0xffff)
        elif dir < 0:
            self.pin_1.duty_u16(0xffff)
            self.pin_2.duty_u16(value)
        else:
            self.pin_1.duty_u16(0xffff)
            self.pin_2.duty_u16(0xffff)

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

class fileDB(object):
	"""A file based database.

    A file based database, read and write arguements in the specific file.
    """
	def __init__(self, db=None):
		'''Init the db_file is a file to save the datas.'''

		# Check if db_file is defined
		if db != None:
			self.db = db
		else:
			self.db = "config"

	def get(self, name, default=None):
		"""Get value by data's name. Default value is for the arguemants do not exist"""
		try:
			conf = open(self.db,'r')
			lines=conf.readlines()
			conf.close()
			file_len=len(lines)-1
			flag = False
			# Find the arguement and set the value
			for i in range(file_len):
				if lines[i][0] != '#':
					if lines[i].split('=')[0].strip() == name:
						value = lines[i].split('=')[1].replace(' ', '').strip()
						flag = True
			if flag:
				return value
			else:
				return default
		except OSError:
			conf = open(self.db,'w')
			conf.write("")
			conf.close()
			return default
		except :
			return default
	
	def set(self, name, value):
		"""Set value by data's name. Or create one if the arguement does not exist"""

		# Read the file
		conf = open(self.db,'r')
		lines=conf.readlines()
		conf.close()
		file_len=len(lines)-1
		flag = False
		# Find the arguement and set the value
		for i in range(file_len):
			if lines[i][0] != '#':
				if lines[i].split('=')[0].strip() == name:
					lines[i] = '%s = %s\n' % (name, value)
					flag = True
		# If arguement does not exist, create one
		if not flag:
			lines.append('%s = %s\n\n' % (name, value))

		# Save the file
		conf = open(self.db,'w')
		conf.write("\n".join(lines))
		conf.close()
