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
            radar_data = [str(i) for i in radar_data]
            radar_data = "".join(radar_data)
            paths = radar_data.split("2")
            length_list = []
            for path in paths:
                length_list.append(len(path))
            if max(length_list) == 0:
                car.move("stop") 
            else:
                i = length_list.index(max(length_list))
                pos = radar_data.index(paths[i])
                pos += (len(paths[i]) - 1) / 2
                delta = len(radar_data) / 3
                if pos < delta:
                    car.move("left", MOTOR_TURNING_POWER)
                elif pos > 2 * delta:

                    car.move("right", MOTOR_TURNING_POWER)
                else:
                    if radar_data[int(len(radar_data)/2-1)] == "0":
#                         car.move("backward", MOTOR_POWER)
                        car.move("stop")
                    else:
                        car.move("forward", MOTOR_TURNING_POWER)

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()
