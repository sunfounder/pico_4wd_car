import machine

pinA = machine.Pin(11, machine.Pin.OUT)
pinB = machine.Pin(10, machine.Pin.OUT)

pinA.low()
pinB.high()