import pico_4wd as car

car.RADAR_SAVE_REFERENCE = 20
car.RADAR_DANGER_REFERENCE = 10
car.RADAR_MAX_ANGLE = 45
car.RADAR_MIN_ANGLE = -45
car.RADAR_STEP_ANGLE = 10
MOTOR_FORWARD_POWER = 20
MOTOR_TURNING_POWER = 80

def main():
    while True:
        radar_data = car.radar_scan()
        if radar_data:
            # print("radar_data: %s" % radar_data)
            tmp = radar_data[3:7]
            if tmp != [2,2,2,2]:
                car.move("right", MOTOR_TURNING_POWER)
                car.set_light_all_color([100, 0, 0])
            else:
                car.move("forward", MOTOR_FORWARD_POWER)
                car.set_light_all_color([0, 100, 0])

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()

