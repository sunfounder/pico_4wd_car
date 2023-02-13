'''
    - servo_class.py 做成类
        - 写成类
        - 调用类控制舵机
'''
from machine import Pin, PWM
import time

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Servo():
    MAX_PW = 2500
    MIN_PW = 500
    PERIOD = 0xffff   

    def __init__(self, pin):
        self.servo = PWM(Pin(pin, Pin.OUT))
        self.servo.freq(50)

    def set_angle(self, angle):
        try:
            angle = int(angle)
        except:
            raise ValueError("Angle value should be int value, not %s"%angle)
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        High_level_time = mapping(angle, -90, 90, self.MAX_PW, self.MIN_PW)
        pwr =  High_level_time / 20000
        value = int(pwr*self.PERIOD)
        self.servo.duty_u16(value)


def main():
    servo = Servo(18)
    for i in range(0, -90, -1):
        servo.set_angle(i)
        time.sleep(0.01)
    for i in range(-90, 90, 1):
        servo.set_angle(i)
        time.sleep(0.01)
    for i in range(90, 0, -1):
        servo.set_angle(i)
        time.sleep(0.01)

if __name__ == '__main__':
    main()