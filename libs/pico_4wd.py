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
MAX_ANGLE = ANGLE_RANGE/2
MIN_ANGLE = -ANGLE_RANGE/2
STEP = 18
RADAR_STEP = STEP
current_angle = 0
scan_list = [] 

def set_all_light_color(color):
    for i in range(24):
        np[i] = color#[color[0], color[1], color[2]]
    np.write()
    
def set_light_color(num, color):
    np[num] = color#[color[0], color[1], color[2]]
    np.write()
    
def set_light_off():
    set_all_light_color([0, 0, 0])

# Grayscale 
def get_grayscale_values():
    return [gs0.read_u16(), gs1.read_u16(), gs2.read_u16()]

def is_on_edge(ref):
    ref = int(ref)
    gs_list = get_grayscale_values()
    if gs_list[2] <= ref or gs_list[1] <= ref or gs_list[0] <= ref:  
        move("backward", 40)
        time.sleep(0.5)
        move("stop")

def get_greyscale_status(ref):
    ref = int(ref)
    return [int(value > ref) for value in get_grayscale_values()]

def get_distance_at(angle):
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = sonar.get_distance()
    return distance

def get_radar_distance():
    global current_angle, RADAR_STEP
    current_angle += RADAR_STEP
    if current_angle >= MAX_ANGLE:
        current_angle = MAX_ANGLE
        RADAR_STEP = -STEP
    elif current_angle <= MIN_ANGLE:  
        current_angle = MIN_ANGLE
        RADAR_STEP = STEP
    distance = get_distance_at(current_angle)
    return [current_angle, distance]

# slowly increase power of the motor, to avoid hight reverse voltage from motors
def save_set_motor_power(powers):
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
def set_motor_power(powers):
    for i, motor in enumerate(motors):
        motor.power = powers[i]

def stop():
    set_motor_power([0] * 4)

def move(dir, power=0):
    if dir == "forward":
        save_set_motor_power([power, power, power, power])
    elif dir == "backward":
        save_set_motor_power([-power, -power, -power, -power])
    elif dir == "left":
        save_set_motor_power([-power, power, -power, power])
    elif dir == "right":
        save_set_motor_power([power, -power, power, -power])
    else:
        save_set_motor_power([0, 0, 0, 0])

if __name__ == "__main__":
    test_speed()


