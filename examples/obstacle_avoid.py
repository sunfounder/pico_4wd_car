import pico_4wd as car

scan_list = []

SAVE_REFERENCE = 15
DANGER_REFERENCE = 8
MOTOR_POWER = 80
MAX_ANGLE = 45
MIN_ANGLE = 45

def get_status_at(angle, distance):
    if distance > SAVE_REFERENCE or distance == -2:
        return 2
    elif distance > DANGER_REFERENCE:
        return 1
    else:
        return 0

def scan_step():
    global scan_list
    angle, distance = car.get_radar_distance()
    status = get_status_at(angle, distance)#ref1

    scan_list.append(status)
    if angle == car.MIN_ANGLE or angle == car.MAX_ANGLE:
        if car.RADAR_STEP < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

def main():
    while True:
        scan_list = scan_step()
        if scan_list:
            tmp = scan_list[3:7]
            print(tmp)
            if tmp != [2,2,2,2]:
                car.move("right", MOTOR_POWER)
                car.set_all_light_color([100, 0, 0])
            else:
                car.move("forward", MOTOR_POWER)
                car.set_all_light_color([0, 100, 0])

try:
    main()
finally:
    car.move("stop")
    car.set_light_off()
