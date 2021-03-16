import pico_4wd as car
import time

grayValue = []

def main():
    while True:
        grayValue = car.get_grayscale_list()
        print('Grayscale value: %d %d %d' %(grayValue[0], grayValue[1], grayValue[2]))
        time.sleep(1)

main()