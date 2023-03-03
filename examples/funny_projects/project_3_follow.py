import sonar as sonar
import motors as car
import time


def get_dir(data,split_str='0'):

    # get scan status of 0, 1
    data = [str(i) for i in data]
    data = "".join(data)

    # Split 1, leaves the object path
    paths = data.split(split_str)
    max_paths=max(paths)

    # no object
    if len(max_paths)<3:
        return "stop"

    # Calculate the direction of the biggest one
    position = data.index(max_paths) # find the biggest object position
    position += (len(max_paths)-1)/2 # find the middle of the biggest object

    # Divide the scanning area into three pieces and mark the right one
    if position < len(data) / 3: 
        return "left"
    elif position > 2 * len(data) / 3:
        return "right"
    else:
        return "forward"

def running(direction,power):
    if direction == "left":
        car.move("left", power)
    elif direction == "right":
        car.move("right", power)
    elif direction == "forward":
        car.move("forward", power)
    else:
        car.move("stop")


try:
    MOTOR_POWER = 20
    sonar.set_sonar_reference(20)
    sonar.set_sonar_scan_config(scan_range=90, step=10)
    while True:
        _,_,sonar_data = sonar.sonar_scan()
        # If sonar data return a int, means scan not finished, and the int is current angle status
        # sonar_data: 0 is block, 1 is pass
        time.sleep(0.04)
        
        if isinstance(sonar_data,int):
            continue # only list can go on

        direction = get_dir(sonar_data,split_str='1')
        running(direction,MOTOR_POWER)

finally:
    car.move("stop")
    time.sleep(0.05)
