import pico_4wd as car

car.RADAR_REFERENCE = 25
car.RADAR_MAX_ANGLE = 45
car.RADAR_MIN_ANGLE = -45
car.RADAR_STEP_ANGLE = 10
MOTOR_FORWARD_POWER = 40
MOTOR_TURNING_POWER = 40


def get_dir(radar_data, split_str="0"):
    # get scan status of 0, 1
    radar_data = [str(i) for i in radar_data]
    radar_data = "".join(radar_data)

    # Split 0, leaves the free path
    paths = radar_data.split(split_str)

    # Calculate where is the widest
    max_paths = max(paths)
    if split_str == "0" and len(max_paths) < 4:
        return "left"
    elif split_str == "1" and len(max_paths) < 2:
        return "stop"

    # Calculate the direction of the widest 
    pos = radar_data.index(max_paths)
    pos += (len(max_paths) - 1) / 2 
    delta = len(radar_data) / 3
    if pos < delta:
        return "left"
    elif pos > 2 * delta:
        return "right"
    else:
        return "forward"


def main():
    while True:
        _, _,radar_data = car.radar_scan()

        # If radar data return a int, means scan not finished, and the int is current angle status
        if isinstance(radar_data, int):
            continue

        direction = get_dir(radar_data, split_str='1')

        if direction == "left":
            car.move("left", MOTOR_TURNING_POWER)
        elif direction == "right":
            car.move("right", MOTOR_TURNING_POWER)
        elif direction == "forward":
            car.move("forward", MOTOR_FORWARD_POWER)
        else:
            car.move("stop") 

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()
