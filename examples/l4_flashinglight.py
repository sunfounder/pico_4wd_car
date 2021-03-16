import pico_4wd as car
import random
import time

def main():
    while True:
        color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        car.set_light_color(color)
        time.sleep(0.5)
        car.set_light_off()
        time.sleep(0.5)

try:
    main()
finally:
    car.set_light_off()
