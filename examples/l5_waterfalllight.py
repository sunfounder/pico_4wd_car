import pico_4wd as car
import random
import time

def main():
    while True:
        print("red")
        for i in range(24):
            car.set_num_color(i, [255, 0, 0])
            time.sleep(0.01)
        for i in range(24):
            car.set_num_color(i, [0, 0, 0])
            time.sleep(0.01)
        print("green")
        for i in range(24):
            car.set_num_color(i, [0, 255, 0])
            time.sleep(0.01)
        for i in range(24):
            car.set_num_color(i, [0, 0, 0])
            time.sleep(0.01)
        print("blue")
        for i in range(24):
            car.set_num_color(i, [0, 0, 255])
            time.sleep(0.01)
        for i in range(24):
            car.set_num_color(i, [0, 0, 0])
            time.sleep(0.01)
        print("white")
        for i in range(24):
            car.set_num_color(i, [255, 255, 255])
            time.sleep(0.01)
        for i in range(24):
            car.set_num_color(i, [0, 0, 0])
            time.sleep(0.01)

try:
    main()
finally:
    car.set_light_off()
