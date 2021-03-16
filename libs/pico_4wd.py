from pico_rdp import Motor, Speed, Servo, Ultrasonic, WS2812
from machine import Pin, ADC
import time

left_front  = Motor(17, 16, dir=-1) # motor 1
right_front = Motor(15, 14, dir=1) # motor 2
left_rear   = Motor(13, 12, dir=-1) # motor 3
right_rear  = Motor(11, 10, dir=1) # motor 4
motors = [left_front, right_front, left_rear, right_rear]

gs0 = ADC(Pin(26))
gs1 = ADC(Pin(27))
gs2 = ADC(Pin(28)) 
servo = Servo(18)
sonar = Ultrasonic(6, 7)
speed = Speed(8, 9)

np =  WS2812(Pin(19, Pin.OUT), 24)

# Ultrasonic
ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = [] 

def set_light_color(color):
    for i in range(24):
        np[i] = color#[color[0], color[1], color[2]]
    np.write()
    
def set_num_color(num, color):
    np[num] = color#[color[0], color[1], color[2]]
    np.write()
    
def set_light_off():
    for i in range(24):
        np[i] = [0, 0, 0]
    np.write()

# Grayscale 
def get_grayscale_list():
    adc_value_list = []
    adc_value_list.append(gs0.read_u16())
    adc_value_list.append(gs1.read_u16())
    adc_value_list.append(gs2.read_u16())
    return adc_value_list

def is_on_edge(ref):
    ref = int(ref)
    gs_list = get_grayscale_list()
    if gs_list[2] <= ref or gs_list[1] <= ref or gs_list[0] <= ref:  
        move("backward", 40)
        time.sleep(0.5)
        move("stop")
    

def get_line_status(ref,fl_list):#170<x<300
    ref = int(ref)
    if fl_list[1] <= ref:
        return 0
    
    elif fl_list[0] <= ref:
        return -1

    elif fl_list[2] <= ref:
        return 1     

def get_distance_at(angle):
    global angle_distance
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = sonar.get_distance()
    angle_distance = [angle, distance]
    return distance

def get_status_at(angle, ref1=35, ref2=7):
    dist = get_distance_at(angle)
    if dist > ref1 or dist == -2:
        return 2
    elif dist > ref2:
        return 1
    else:
        return 0

def get_angle_distance():
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:  
        current_angle = min_angle
        us_step = STEP
    get_distance_at(current_angle)

def scan_step(ref):
    global scan_list, current_angle, us_step
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

def motor_direction_calibration(motor, value):
    # 0: positive direction
    # 1:negative direction
    global cali_dir_value
    motor -= 1
    if value == 1:
        cali_dir_value[motor] = -1*cali_dir_value[motor]

def save_set_power(powers):
    flags = [True, True, True, True]
    while flags[0] or flags[1] or flags[2] or flags[3]:
        for i, motor in enumerate(motors):
            # print(motor.power, powers[i])
            if motor.power > powers[i]:
                motor.power -= 1
            elif motor.power < powers[i]:
                motor.power += 1
            else:
                flags[i] = False
        time.sleep_ms(1)

def set_power(powers):
    for i, motor in enumerate(motors):
        motor.power = powers[i]

def stop():
    set_power([0] * 4)

def move(dir, power=0):
    if dir == "forward":
        save_set_power([power, power, power, power])
    elif dir == "backward":
        save_set_power([-power, -power, -power, -power])
    elif dir == "left":
        save_set_power([-power, power, -power, power])
    elif dir == "right":
        save_set_power([power, -power, power, -power])
    else:
        save_set_power([0, 0, 0, 0])
        
def track_line(ref, speed):
    gs_list = get_grayscale_list()
    if get_line_status(ref,gs_list) == 0:
        move("forward", speed)      
    elif get_line_status(ref,gs_list) == -1:
        move("left", speed)
    elif get_line_status(ref,gs_list) == 1:
        move("right", speed)   
        
def avoid(ref, speed):
    scan_list = scan_step(ref)
    if scan_list:
        tmp = scan_list[3:7]
        if tmp != [2,2,2,2]:
            move("right", speed)
        else:
            move("forward", speed)

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

def test_motor():
    for i in range(101):
        move("forward", i)
        time.sleep(0.01)
    for i in range(100, -101, -1):
        move("forward", i)
        time.sleep(0.01)
    for i in range(-100, 1, 1):
        move("forward", i)
        time.sleep(0.01)

def test_motor_extream():
    print("forward")
    move("forward", 100)
    time.sleep(1)
    print("backward")
    move("backward", 100)
    time.sleep(1)
    print("left")
    move("left", 100)
    time.sleep(1)
    print("right")
    move("right", 100)
    time.sleep(1)
    print("stop")
    move("stop", 100)
    time.sleep(1)

def test_light():
    print("red")
    for i in range(24):
        set_num_color(i, [255, 0, 0])
        time.sleep(0.01)
    for i in range(24):
        set_num_color(i, [0, 0, 0])
        time.sleep(0.01)
    print("green")
    for i in range(24):
        set_num_color(i, [0, 255, 0])
        time.sleep(0.01)
    for i in range(24):
        set_num_color(i, [0, 0, 0])
        time.sleep(0.01)
    print("blue")
    for i in range(24):
        set_num_color(i, [0, 0, 255])
        time.sleep(0.01)
    for i in range(24):
        set_num_color(i, [0, 0, 0])
        time.sleep(0.01)
    print("white")
    for i in range(24):
        set_num_color(i, [255, 255, 255])
        time.sleep(0.01)
    for i in range(24):
        set_num_color(i, [0, 0, 0])
        time.sleep(0.01)

def test_grayscale():
    while True:
        print(get_grayscale_list())
        time.sleep(1)

def test_speed():
    while True:
        print(speed.get_speed())
        time.sleep(1)

def test_ultrasonic():
    while True:
        get_angle_distance()
        print(angle_distance)
        time.sleep(1)
        
if __name__ == "__main__":
    test_speed()
