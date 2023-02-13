'''
- 单个电机的控制
    - 一个电机使用到了两个 PWM 引脚
        - pin1 = x, pin2 = 0xffff , 正转
        - pin1 = 0xffff, pin2 = x , 反转
        - pin1 = 0xffff, pin2 = 0xffff, 停止
    - power映射到PWM值,和方向值
'''

from machine import Pin, PWM
import time

pin_a = 15
pin_b = 14
dir = 1 # direction 控制正反方向

pwm1 = PWM(Pin(pin_a, Pin.OUT))
pwm2 = PWM(Pin(pin_b, Pin.OUT))
pwm1.freq(20000)
pwm2.freq(20000)

# 重映射值
def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def move(power:int):
    if power == 0:
        pwm1.duty_u16(0xffff)
        pwm2.duty_u16(0xffff)
    else:
        value = mapping(abs(power), 0, 100, 20, 100)
        value = int(value / 100.0 * 0xffff)
        value = 0xffff - value

        if power*dir > 0:
            pwm1.duty_u16(value)
            pwm2.duty_u16(0xffff)
        else:
            pwm1.duty_u16(0xffff)
            pwm2.duty_u16(value)



def main():
    for i in range(100):
        move(i)
        time.sleep(0.05)
    for i in range(100):
        move(-i)
        time.sleep(0.05)

if __name__ == '__main__':
    try:
        main()
    finally:
        move(0)
        time.sleep(0.05)
