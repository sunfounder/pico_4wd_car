import machine

for i in range(10,18):
    pin = machine.PWM(machine.Pin(i, machine.Pin.OUT))
    pin.freq(20000)
    pin.duty_u16(0xFFFF)