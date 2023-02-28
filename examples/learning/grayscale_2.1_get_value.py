from machine import Pin, ADC
import time

gs0 = ADC(Pin(26))
gs1 = ADC(Pin(27))
gs2 = ADC(Pin(28))

def get_value():
    return [gs0.read_u16(), gs1.read_u16(), gs2.read_u16()]

while True:
    print(get_value())
    time.sleep(0.2)