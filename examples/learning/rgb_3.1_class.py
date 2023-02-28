''' 
This file is only for learning, 
please refer to the libs file for actual use.
'''

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
import array
import time

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
        self.sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(self.pin))
        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)

        self.buf = array.array("I", [0 for _ in range(self.led_nums)])

    def write(self):
        self.sm.put(self.buf, 8)

    def __getitem__(self, i):
        return self.buf[i]

    def __setitem__(self, i, value):
        self.buf[i] = value


# Display a pattern on the LEDs via a color value.
LIGHT_PIN = 19
LIGHT_NUM = 24
np = WS2812(LIGHT_PIN, LIGHT_NUM)

for i in range(LIGHT_NUM):
    np[i] = 0x00aaff
np.write()