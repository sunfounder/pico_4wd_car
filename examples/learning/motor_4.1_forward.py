import machine
import time

pin = []
motor_pin = [17,16,15,14,13,12,11,10]

for i in range(8):
    pin.append(None)
    pin[i] = machine.PWM(machine.Pin(motor_pin[i],machine.Pin.OUT))
    pin[i].freq(20000)

def motor_run(power,pinA,pinB,position):
    power= int(power/100.0*0xFFFF)
    if position>0:
        # clockwise
        pinA.duty_u16(0xFFFF-power)
        pinB.duty_u16(0xFFFF)
    elif position<0:
        # anticlockwise
        pinA.duty_u16(0xFFFF)
        pinB.duty_u16(0xFFFF-power)

try:

    power = 50

    # forward
    motor_run(power,pin[0],pin[1],-1) #left front
    motor_run(power,pin[2],pin[3],1) #right front
    motor_run(power,pin[4],pin[5],-1) #left rear
    motor_run(power,pin[6],pin[7],1) #right rear
    time.sleep(2)

finally:
        # stop
    power = 0
    motor_run(power,pin[0],pin[1],-1) #left front
    motor_run(power,pin[2],pin[3],1) #right front
    motor_run(power,pin[4],pin[5],-1) #left rear
    motor_run(power,pin[6],pin[7],1) #right rear