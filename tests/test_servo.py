import pico_4wd as car
import time


def test_servo():
    for angle in range(0, 90):
        print("angle:%s "%angle)
        car.servo.set_angle(angle)
        time.sleep(0.005)
    for angle in range(90, -90, -1):
        print("angle:%s "%angle)
        car.servo.set_angle(angle)
        time.sleep(0.005)
    for angle in range(-90, 0):
        print("angle:%s "%angle)
        car.servo.set_angle(angle)
        time.sleep(0.005)

try:

    test_servo()

finally:
    car.move("stop")
    car.set_light_off()
