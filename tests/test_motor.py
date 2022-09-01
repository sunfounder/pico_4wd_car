import pico_4wd as car
import time

def test_motor():
    speed = 50
    act_list = [
        "forward",
        "backward",
        "left",
        "right",
        "stop",
    ]
    for act in act_list:
        print(act)
        car.move(act, speed)
        time.sleep(1)


try:
    test_motor()

finally:
    car.move("stop")
    car.set_light_off()

