import pico_4wd as car
import random
import time

def main():
    while True:
        car.move("forward",random.randint(0,100))
        time.sleep(1)
        carSpeed = car.speed.get_speed()
        print('distance:%d' % carSpeed)

try:
    main()
finally:
    car.move("stop")
