from pico_rdp import Motor, Speed, Servo, Ultrasonic, WS2812, mapping
from machine import Pin, ADC
import time

LIGHT_REAR = 0
LIGHT_BOTTOM_LEFT = 1
LIGHT_BOTTOM_RIGHT = 2

left_front  = Motor(17, 16, dir=1) # motor 1
right_front = Motor(15, 14, dir=-1) # motor 2
left_rear   = Motor(13, 12, dir=1) # motor 3
right_rear  = Motor(11, 10, dir=-1) # motor 4
motors = [left_front, right_front, left_rear, right_rear]

servo = Servo(18)
speed = Speed(8, 9)

np =  WS2812(Pin(19, Pin.OUT), 24)

gs0 = ADC(Pin(26))
gs1 = ADC(Pin(27))
gs2 = ADC(Pin(28))
GRAYSCALE_EDGE_REFERENCE = 20
GRAYSCALE_LINE_REFERENCE = 10000

# Ultrasonic
sonar = Ultrasonic(6, 7)
radar_data = []
RADAR_REFERENCE = 20
RADAR_MAX_ANGLE = 90
RADAR_MIN_ANGLE = -90
RADAR_STEP_ANGLE = 10
radar_step = -RADAR_STEP_ANGLE
radar_angle = 0
radar_scan_angle = 180

def set_light_all_color(color):
    for i in range(24):
        np[i] = color#[color[0], color[1], color[2]]
    np.write()

def set_light_color_at(num, color, preset=0):
    write_light_color_at(num, color, preset=preset)
    np.write()

def set_light_bottom_left_color(color):
    for i in range(8):
        write_light_color_at(i+8*LIGHT_BOTTOM_LEFT, color)
    light_excute()

def set_light_bottom_right_color(color):
    for i in range(8):
        write_light_color_at(i+8*LIGHT_BOTTOM_RIGHT, color)
    light_excute()

def set_light_bottom_color(color):
    for i in range(8):
        write_light_color_at(i+8*LIGHT_BOTTOM_LEFT, color)
    for i in range(8):
        write_light_color_at(i+8*LIGHT_BOTTOM_RIGHT, color)
    light_excute()

def set_light_rear_color(color):
    for i in range(8):
        write_light_color_at(8*LIGHT_REAR, color)
    light_excute()

def write_light_color_at(num, color, preset=0):
    np[num + preset*8] = color#[color[0], color[1], color[2]]

def light_excute():
    np.write()
    
def set_light_off():
    set_light_all_color([0, 0, 0])

def hue2rgb(_h, _s = 1, _b = 1):
    _hi = int((_h/60)%6)
    _f = _h / 60.0 - _hi
    _p = _b * (1 - _s)
    _q = _b * (1 - _f * _s)
    _t = _b * (1 - (1 - _f) * _s)
    
    if _hi == 0:
        _R_val = _b
        _G_val = _t
        _B_val = _p
    if _hi == 1:
        _R_val = _q
        _G_val = _b
        _B_val = _p
    if _hi == 2:
        _R_val = _p
        _G_val = _b
        _B_val = _t
    if _hi == 3:
        _R_val = _p
        _G_val = _q
        _B_val = _b
    if _hi == 4:
        _R_val = _t
        _G_val = _p
        _B_val = _b
    if _hi == 5:
        _R_val = _b
        _G_val = _p
        _B_val = _q
    
    r = int(_R_val*255)
    g = int(_G_val*255)
    b = int(_B_val*255)
    return [r,g,b]

# Grayscale 
def get_grayscale_values():
    return [gs0.read_u16(), gs1.read_u16(), gs2.read_u16()]

def is_greyscale_on_edge():
    ref = GRAYSCALE_EDGE_REFERENCE
    gs_list = get_grayscale_values()
    return gs_list[2] <= ref or gs_list[1] <= ref or gs_list[0] <= ref

def get_greyscale_status():
    ref = GRAYSCALE_LINE_REFERENCE
    return [int(value < ref) for value in get_grayscale_values()]

# Radar
def get_radar_distance_at(angle):
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = sonar.get_distance()
    return distance

def get_radar_distance():
    global radar_angle, radar_step
    radar_angle += radar_step
    if radar_angle >= RADAR_MAX_ANGLE:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -RADAR_STEP_ANGLE
    elif radar_angle <= RADAR_MIN_ANGLE:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = RADAR_STEP_ANGLE
    distance = get_radar_distance_at(radar_angle)
    return [radar_angle, distance]

def set_radar_scan_angle(angle):
    global RADAR_MAX_ANGLE, RADAR_MIN_ANGLE, radar_angle, radar_step, radar_scan_angle
    if radar_scan_angle == angle:
        return
    radar_scan_angle = angle
    RADAR_MAX_ANGLE = int(angle / 2)
    RADAR_MIN_ANGLE = -RADAR_MAX_ANGLE
    if radar_step < 0:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = RADAR_STEP_ANGLE
    else:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -RADAR_STEP_ANGLE
    servo.set_angle(radar_angle)

def get_radar_status(distance):
    if distance > RADAR_REFERENCE:
        return 1
    else:
        return 0

def radar_scan():
    global radar_data
    angle, distance = get_radar_distance()
    status = get_radar_status(distance)

    radar_data.append(status)
    if angle == RADAR_MIN_ANGLE or angle == RADAR_MAX_ANGLE:
        if radar_step < 0:
            # print("reverse")
            radar_data.reverse()
        # print(radar_data)
        tmp = radar_data.copy()
        radar_data = []
        return tmp
    else:
        return status

# slowly increase power of the motor, to avoid hight reverse voltage from motors
def set_motor_power_gradually(*powers):
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

# set power 
def set_motor_power(*powers):
    for i, motor in enumerate(motors):
        motor.power = powers[i]

def stop():
    set_motor_power(0, 0, 0, 0)

def move(dir, power=0):
    if dir == "forward":
        set_motor_power_gradually(power, power, power, power)
    elif dir == "backward":
        set_motor_power_gradually(-power, -power, -power, -power)
    elif dir == "left":
        set_motor_power_gradually(-power, power, -power, power)
    elif dir == "right":
        set_motor_power_gradually(power, -power, power, -power)
    else:
        set_motor_power_gradually(0, 0, 0, 0)

