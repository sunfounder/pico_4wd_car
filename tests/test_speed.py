import pico_4wd as car
import time


def test_speed():
    def helper(power):
        # power changes every 10%
        power = round(power / 10) * 10
        car.move("forward", power)
        print('Power(%%):%d Speed(cm/s):%.2f' % (power, car.speed()))
        time.sleep(0.2)
    while True:
        for power in range(100):
            helper(power)

        for power in range(100, -100, -1):
            helper(power)

        for power in range(-100, 0):
            helper(power)

try:
    
    test_speed()
    
finally:
    car.move("stop")
    car.set_light_off()
