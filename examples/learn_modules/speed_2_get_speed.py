from machine import Timer, Pin
import math

WP = 2 * math.pi * 3.3 # wheel_perimeter(cm): 2 * pi * r
duration = 200

def on_left(ch):
    global left_count
    left_count += 1

def on_right(ch):
    global right_count
    right_count += 1

def on_timer(ch):
    global left_count,right_count
    # revolutions per second
    rps = (left_count + right_count) * 1000 /duration /20.0 /2
    # speed
    speed = rps * WP
    print(speed)
    # clear count
    left_count = 0
    right_count = 0

# Interrupter, used to count
left_count = 0
right_count = 0
left_pin = Pin(8, Pin.IN, Pin.PULL_UP)
left_pin.irq(trigger=Pin.IRQ_FALLING, handler=on_left)
right_pin = Pin(9, Pin.IN, Pin.PULL_UP)
right_pin.irq(trigger=Pin.IRQ_FALLING, handler=on_right)

# Timer, print speed
tim = Timer()
tim.init(period=duration, mode=Timer.PERIODIC, callback=on_timer)

# motor run
import motors
import time

try:
    while True:
        for i in range(20,100,10):
            motors.move("forward",i)
            time.sleep(1)
finally:
    motors.stop()
    time.sleep(0.2)