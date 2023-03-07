import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio
# Configure the number of WS2812 LEDs.
LIGHT_NUM = 24
LIGHT_PIN = 19

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]

# Create the StateMachine with the ws2812 program, outputting on Pin(19).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(LIGHT_PIN))
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via a color value.
ar = array.array("I", [0 for _ in range(LIGHT_NUM)])

for i in range(LIGHT_NUM):
    ar[i] = 0xffaa00
sm.put(ar,8)