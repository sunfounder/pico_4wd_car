from machine import Pin, PWM
import time

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

            if power*self.dir > 0:
                self.pwm1.duty_u16(0xffff - value)
                self.pwm2.duty_u16(0xffff)
            else:
                self.pwm1.duty_u16(0xffff)
                self.pwm2.duty_u16(0xffff - value)



if __name__ == '__main__':

    # init
    left_front  = Motor(17, 16, dir=-1)
    right_front = Motor(15, 14, dir= 1)
    left_rear   = Motor(13, 12, dir=-1)
    right_rear  = Motor(11, 10, dir= 1)

    try:
        # forward
        power = 80
        left_front.run(power)
        right_front.run(power)
        left_rear.run(power)
        right_rear.run(power)  
        time.sleep(5)

    finally:
        # stop
        power = 0
        left_front.run(power)
        right_front.run(power)
        left_rear.run(power)
        right_rear.run(power) 
        time.sleep(0.2)   



