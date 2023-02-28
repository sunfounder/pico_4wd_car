import machine

pinA = machine.Pin(13, machine.Pin.OUT)
pinB = machine.Pin(12, machine.Pin.OUT)

pwmA = machine.PWM(pinA)
pwmB = machine.PWM(pinB)
pwmA.freq(20000)
pwmB.freq(20000)

# slow
pwmA.duty_u16(0xFFFF)
pwmB.duty_u16(0xAAAA)