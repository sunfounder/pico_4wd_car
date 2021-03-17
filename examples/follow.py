scan_list = []

def scan_step(ref):
    global , current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:  
        current_angle = min_angle
        us_step = STEP
    status = get_status_at(current_angle, ref1=ref)#ref1

    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

def get_status_at(angle, ref1=35, ref2=7):
    dist = get_distance_at(angle)
    if dist > ref1 or dist == -2:
        return 2
    elif dist > ref2:
        return 1
    else:
        return 0

def follow(ref, speed):
    scan_list = scan_step(ref)
    if scan_list != False:
        scan_list = [str(i) for i in scan_list]
        scan_list = "".join(scan_list)
        paths = scan_list.split("2")
        length_list = []
        for path in paths:
            length_list.append(len(path))
        if max(length_list) == 0:
            move("stop") 
        else:
            i = length_list.index(max(length_list))
            pos = scan_list.index(paths[i])
            pos += (len(paths[i]) - 1) / 2
            delta = len(scan_list) / 3
            if pos < delta:
                move("left", speed)
            elif pos > 2 * delta:
                move("right", speed)
            else:
                if scan_list[int(len(scan_list)/2-1)] == "0":
                    move("backward", 100)
                else:
                    move("forward", speed)
