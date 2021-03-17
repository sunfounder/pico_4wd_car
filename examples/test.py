import pico_4wd as car
import time

def test_motor():
    speed = 100
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

def test_sonar():
    while True:
        distance = car.sonar.get_distance()
        print('distance:%s'% distance)
        time.sleep(1)

def test_servo():
    while True:
        for angle in range(-90, 90):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.005)
        for angle in range(90, -90, -1):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.005)

def test_light():
    print("red")
    for i in range(24):
        car.set_light_color(i, [255, 0, 0])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color(i, [0, 0, 0])
        time.sleep(0.01)
    print("green")
    for i in range(24):
        car.set_light_color(i, [0, 255, 0])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color(i, [0, 0, 0])
        time.sleep(0.01)
    print("blue")
    for i in range(24):
        car.set_light_color(i, [0, 0, 255])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color(i, [0, 0, 0])
        time.sleep(0.01)
    print("white")
    for i in range(24):
        car.set_light_color(i, [255, 255, 255])
        time.sleep(0.01)
    for i in range(24):
        car.set_light_color(i, [0, 0, 0])
        time.sleep(0.01)

def test_grayscale():
    while True:
        grayValue = car.get_grayscale_values()
        print('left:%d, middle:%d, right:%d' %(grayValue[0], grayValue[1], grayValue[2]))
        time.sleep(1)

def test_speed():
    def helper(power):
        # power changes every 10%
        power = round(power / 10) * 10
        car.move("forward", power)
        print('Power(%%):%d Speed(cm/s):%.2f' % (power, car.speed()))
        time.sleep(0.2)
    while True:
        for power in range(100):
            helper(power)

        for power in range(100, -100, -1):
            helper(power)

        for power in range(-100, 0):
            helper(power)

try:
    # test_motor()
    # test_sonar()
    # test_servo()
    # test_light()
    # test_grayscale()
    test_speed()
finally:
    car.move("stop")
    car.set_light_off()
