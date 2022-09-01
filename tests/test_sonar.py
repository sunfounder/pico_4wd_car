import pico_4wd as car
import time

def test_sonar():
    while True:
        distance = car.sonar.get_distance()
        print('distance:%s'% distance)
        time.sleep(1)

try:

    test_sonar()

finally:
    car.move("stop")
    car.set_light_off()
