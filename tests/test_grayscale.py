import pico_4wd as car
import time


def test_grayscale():
    while True:
        grayValue = car.get_grayscale_values()
        print('left:%d, middle:%d, right:%d' %(grayValue[0], grayValue[1], grayValue[2]))
        time.sleep(1)


try:

    test_grayscale()

finally:
    car.move("stop")
    car.set_light_off()
                                                      