import pico_4wd as car
import time

def main():
    while True:
        distance = car.ultrasonic.get_distance()
        print('distance:%0.2f' % distance)
        time.sleep(0.1)

main()