import pico_4wd as car

car.RADAR_DANGER_REFERENCE = 20
car.RADAR_MAX_ANGLE = 45
car.RADAR_MIN_ANGLE = -45
car.RADAR_STEP_ANGLE = 10
MOTOR_FORWARD_POWER = 20
MOTOR_TURNING_POWER = 90

def main():
    while True:
        radar_data = car.radar_scan()
        if radar_data:
            # get scan status of 0, 1, 2
            radar_data = [str(i) for i in radar_data]
            radar_data = "".join(radar_data)
            # Split 0, leaves the free path
            paths = radar_data.split("0")
            length_list = []
            # Calculate where is the widest
            for path in paths:
                length_list.append(len(path))
            if max(length_list) == 0:
                car.move("stop") 
            else:
                # Calculate the direction of the widest 
                i = length_list.index(max(length_list))
                pos = radar_data.index(paths[i])
                pos += (len(paths[i]) - 1) / 2
                delta = len(radar_data) / 3
                if pos < delta:
                    car.move("left", MOTOR_TURNING_POWER)
                elif pos > 2 * delta:

                    car.move("right", MOTOR_TURNING_POWER)
                else:
                    # if the middle is free
                    if int(radar_data[int(len(radar_data)/2-1)]) > 0:
                        car.move("forward", MOTOR_FORWARD_POWER)
try:
    main()
finally:
    car.move("stop")
    car.set_light_off()
