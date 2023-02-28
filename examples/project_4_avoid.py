import sonar as sonar
import motors as car
import time

def get_dir(data,split_str='0'):

    # get scan status of 0, 1
    data = [str(i) for i in data]
    data = "".join(data)

    # Split 0, leaves the free path
    paths = data.split(split_str)
    max_paths=max(paths)

    # no wide enough path
    if len(max_paths)<4:
        return "left"

    # Calculate the direction of the widest one
    position = data.index(max_paths) # find the widest path position
    position += (len(max_paths)-1)/2 # find the middle of the widest path

    # Divide the scanning area into three pieces and mark the widest one
    if position < len(data) / 3: 
        return "left"
    elif position > 2 * len(data) / 3:
        return "right"
    else:
        return "forward"

def running(direction,power):
    if direction is "left":
        sonar.get_distance_at(20) # face right
        time.sleep(0.2)
        car.move("left", power*2)
        while True:
            distance = sonar.get_distance_at(20) # face right
            status = sonar.get_sonar_status(distance)
            if status is 1: # right position is pass
                break
        car.move("stop")
    elif direction is "right":
        sonar.get_distance_at(-20) # face left
        time.sleep(0.2)
        car.move("right", power*2)
        while True:
            distance = sonar.get_distance_at(-20) # face left
            status = sonar.get_sonar_status(distance)
            if status is 1: # left position is pass
                break
        car.move("stop")
    else:
        # pass
        car.move("forward",power)


try:
    MOTOR_POWER = 30
    SCAN_RANGE_PASS = 60
    SCAN_RANGE_BLOCK = 180
    SCAN_STEP = 10
    status = "pass"
    sonar.set_sonar_scan_config(scan_range=SCAN_RANGE_PASS, step=SCAN_STEP)
    sonar.set_sonar_reference(30)
    while True:
        _, _, sonar_data = sonar.sonar_scan()
        # If sonar data return a int, means scan not finished, and the int is current angle status
        # sonar_data: 0 is block, 1 is pass
        time.sleep(0.04)
        
        if isinstance(sonar_data, int): 
            if sonar_data is 0 and status is "pass":
                status = "block"
                sonar.set_sonar_scan_config(SCAN_RANGE_BLOCK) # change scan range and re-scan
                car.move("stop")
            continue # only list can go on
        direction = get_dir(sonar_data,split_str='0')
        running(direction, MOTOR_POWER)
        status = "pass"
        sonar.set_sonar_scan_config(SCAN_RANGE_PASS)
        
finally:
    car.move("stop")
    time.sleep(0.05)
