'''
    - servo_control.py 舵机的控制
        - pwm 初始化， 频率对应的角度

'''
from machine import Pin, PWM
import time

MAX_PW = 2500
MIN_PW = 500
PERIOD = 0xffff

servo_pin = 18
servo = PWM(Pin(servo_pin, Pin.OUT))
servo.freq(50)

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_angle(angle):
    try:
        angle = int(angle)
    except:
        raise ValueError("Angle value should be int value, not %s"%angle)
    if angle < -90:
        angle = -90
    if angle > 90:
        angle = 90
    High_level_time = mapping(angle, -90, 90, MAX_PW, MIN_PW)
    pwr =  High_level_time / 20000
    value = int(pwr*PERIOD)
    servo.duty_u16(value)


def main():
    for i in range(0, -90, -1):
        set_angle(i)
        time.sleep(0.01)
    for i in range(-90, 90, 1):
        set_angle(i)
        time.sleep(0.01)
    for i in range(90, 0, -1):
        set_angle(i)
        time.sleep(0.01)

if __name__ == '__main__':
    main()