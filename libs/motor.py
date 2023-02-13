'''
    - 为了方便控制多个电机，将单个电机控制做成一个类
        - 写成类
        - 调用类同时控制1个电机
'''

from machine import Pin, PWM
import time

# 重映射值
def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Motor():
    def __init__(self, pin_a, pin_b, dir=1):
        self.pwm1 = PWM(Pin(pin_a, Pin.OUT))
        self.pwm2 = PWM(Pin(pin_b, Pin.OUT))
        self.pwm1.freq(20000)
        self.pwm2.freq(20000)
        self.dir = dir
        self.current_power = 0

    def run(self, power:int):
        self.current_power = power
        if power == 0:
            self.pwm1.duty_u16(0xffff)
            self.pwm2.duty_u16(0xffff)
        else:
            value = mapping(abs(power), 0, 100, 20, 100)
            value = int(value / 100.0 * 0xffff)
            value = 0xffff - value

            if power*self.dir > 0:
                self.pwm1.duty_u16(value)
                self.pwm2.duty_u16(0xffff)
            else:
                self.pwm1.duty_u16(0xffff)
                self.pwm2.duty_u16(value)




def main():
    # init
    left_front  = Motor(17, 16, dir=-1)
    right_front = Motor(15, 14, dir= 1)
    left_rear   = Motor(13, 12, dir=-1)
    right_rear  = Motor(11, 10, dir= 1)
    # forward
    for i in range(100):
        left_front.move(i)
        right_front.move(i)
        left_rear.move(i)
        right_rear.move(i)
        time.sleep(0.05)
    # forward
    for i in range(100):
        left_front.move(-i)
        right_front.move(-i)
        left_rear.move(-i)
        right_rear.move(-i)
        time.sleep(0.05)
    # stop
    left_front.move(0)
    right_front.move(0)
    left_rear.move(0)
    right_rear.move(0)
    time.sleep(0.05)

if __name__ == '__main__':
    main()
