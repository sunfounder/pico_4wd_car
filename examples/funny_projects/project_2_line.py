from grayscale import Grayscale
import motors as car
import lights
import time

gs = Grayscale(26, 27, 28)
gs.set_line_reference(10000)

MOTOR_POWER = 30

def line_track():
    while True:
        gs_data = gs.get_line_status()
        if gs_data == [0, 1, 0]:
            car.set_motors_power([MOTOR_POWER, MOTOR_POWER, MOTOR_POWER, MOTOR_POWER]) # forward
            lights.set_bottom_color([0, 100, 0])
        elif gs_data == [0, 1, 1]:
            car.set_motors_power([MOTOR_POWER, 0, MOTOR_POWER, 0]) # turn right at a small angle
            lights.set_off()
            lights.set_bottom_left_color([50, 50, 0])
        elif gs_data == [0, 0, 1]:
            car.set_motors_power([MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER]) # turn right at a small angle
            lights.set_off()
            lights.set_bottom_left_color([100, 5, 0])
        elif gs_data == [1, 1, 0]:
            car.set_motors_power([0, MOTOR_POWER, 0, MOTOR_POWER]) # turn left at a small angle
            lights.set_off()
            lights.set_bottom_right_color([50, 50, 0])
        elif gs_data == [1, 0, 0]:
            car.set_motors_power([-MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER]) # turn left at a small angle
            lights.set_off()
            lights.set_bottom_right_color([100, 0, 0])

try:
    line_track()
finally:
    car.move("stop")
    lights.set_off()
    time.sleep(0.05)
