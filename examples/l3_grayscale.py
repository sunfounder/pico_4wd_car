import pico_4wd as car
import time

grayValue = []
REFERENCE = 10000

def main():
    while True:
        grayValue = car.get_grayscale_list()
        print('reference:%d left:%d middle:%d right:%d' %(REFERENCE, grayValue[0], grayValue[1], grayValue[2]))
        time.sleep(0.1)

main()
