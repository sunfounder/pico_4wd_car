import pico_4wd as car
import time

speed = 100
def main():
    car.move("forward", speed)
    time.sleep(1)
    car.move("backward", speed)
    time.sleep(1)
    car.move("left", speed)
    time.sleep(1)
    car.move("right", speed)
    time.sleep(1) 
    car.move("stop")

try:
    main()
finally:
    car.move("stop")
