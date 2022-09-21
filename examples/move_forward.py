import pico_4wd as car
import time

try:
    while True:
        car.move("forward", 50)
        time.sleep(1)
finally:
    car.move("stop")