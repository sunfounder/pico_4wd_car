import pico_4wd as car
import time

car.GRAYSCALE_EDGE_REFERENCE = 500
MOTOR_POWER = 50

def main():
    while True:
        if car.is_greyscale_on_edge():
            car.move("backward", MOTOR_POWER)
            time.sleep(1)
            car.move("left", MOTOR_POWER)
            time.sleep(1)
            car.set_light_all_color([100, 0, 0])
        else:
            car.move("forward", MOTOR_POWER)
            car.set_light_all_color([0, 100, 0])

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()
