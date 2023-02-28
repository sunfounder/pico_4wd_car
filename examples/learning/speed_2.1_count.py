from machine import Timer, Pin

def on_left(ch):
    global left_count
    left_count += 1

def on_timer(ch):
    global left_count
    print(left_count)
    left_count = 0

# Interrupter, used to count
left_count = 0
left_pin = Pin(8, Pin.IN, Pin.PULL_UP)
left_pin.irq(trigger=Pin.IRQ_FALLING, handler=on_left)

# Timer, print count every 1000ms
tim = Timer()
tim.init(period=1000, mode=Timer.PERIODIC, callback=on_timer)

# motor run
import motors
import time

try:
    while True:
#         for i in range(20,100,10):
        motors.move("forward",50)
#             time.sleep(1)
finally:
    motors.stop()
    time.sleep(0.2)