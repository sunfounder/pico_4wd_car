import pico_4wd as car
import time

MOTOR_POWER = 50
car.GRAYSCALE_LINE_REFERENCE = 5000
TIMEOUT = 3000

def main():
    last_data = [0, 0, 0]
    timeout_count = 0
    while True:
        gs_data = car.get_greyscale_status()
#         print(gs_data)
        if gs_data == [0, 0, 0]:
            if last_data == [1, 0, 0]:
                car.set_motor_power(-MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER)
                car.set_light_off()
                car.set_light_bottom_right_color([100, 0, 0])
            elif gs_data == [0, 0, 1]:
                car.set_motor_power(MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER)
                car.set_light_off()
                car.set_light_bottom_left_color([100, 0, 0])
            timeout_count += 1
            if timeout_count > TIMEOUT:
                car.move("stop")
                car.set_light_off()
                timeout_count = 0
        else:
            timeout_count = 0
            if gs_data == [0, 1, 0]:
                car.move("forward", MOTOR_POWER)
                car.set_light_bottom_color([0, 100, 0])
            elif gs_data in [[0, 1, 1], [0, 0, 1]]:
                car.set_motor_power(MOTOR_POWER, 0, MOTOR_POWER, 0)
                car.set_light_off()
                car.set_light_bottom_left_color([50, 50, 0])
            elif gs_data in [[1, 1, 0], [1, 0, 0]]:
                car.set_motor_power(0, MOTOR_POWER, 0, MOTOR_POWER)
                car.set_light_off()
                car.set_light_bottom_right_color([50, 50, 0])
            last_data = gs_data
        time.sleep(0.001)

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()

