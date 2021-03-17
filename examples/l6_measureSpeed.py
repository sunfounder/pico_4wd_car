import pico_4wd as car
import random
import time

def main():
    def helper(power):
        power = int(round(power / 10) * 10)
        car.move("forward", power)
        print('power(%%):%d left_speed(cm/s):%.2f right_speed(cm/s):%.2f' % (power, car.speed.left_speed, car.speed.right_speed))
        time.sleep(0.1)
    for power in range(101):
        helper(power)
    for power in range(100, -101, -1):
        helper(power)
    for power in range(-100, 0):
        helper(power)

try:
    main()
finally:
    car.move("stop")
