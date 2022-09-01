import pico_4wd as car
import time


def test_light():
    print("red")
    for i in range(24):
        car.set_light_color_at(i, [255, 0, 0])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color_at(i, [0, 0, 0])
        time.sleep(0.01)
    print("green")
    for i in range(24):
        car.set_light_color_at(i, [0, 255, 0])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color_at(i, [0, 0, 0])
        time.sleep(0.01)
    print("blue")
    for i in range(24):
        car.set_light_color_at(i, [0, 0, 255])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color_at(i, [0, 0, 0])
        time.sleep(0.01)
    print("white")
    for i in range(24):
        car.set_light_color_at(i, [255, 255, 255])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color_at(i, [0, 0, 0])
        time.sleep(0.01)

try:

    test_light()

finally:
    car.move("stop")
    car.set_light_off()
