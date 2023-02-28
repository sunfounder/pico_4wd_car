import machine

for i in range(10,18):
    pin = machine.Pin(i, machine.Pin.OUT)
    pin.high()