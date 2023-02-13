import pico_4wd as car
import time

def test_motor():
    speed = 50
    act_list = [
        "forward",
#         "backward",
#         "left",
#         "right",
#         "stop",
    ]
    for act in act_list:
        print(act)
        car.move(act, speed)
        time.sleep(1)


try:
    while True:
        test_motor()
        time.sleep(2)

finally:
    car.move("stop")
    car.set_light_off()

