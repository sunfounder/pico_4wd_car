import machine

pinA = machine.Pin(17, machine.Pin.OUT)
pinB = machine.Pin(16, machine.Pin.OUT)

pwmA = machine.PWM(pinA) # Create PWM object
pwmB = machine.PWM(pinB) # Create PWM object
pwmA.freq(20000)
pwmB.freq(20000)

# fast
pwmA.duty_u16(0x0000)
pwmB.duty_u16(0xFFFF)