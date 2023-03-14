import machine
import time

trig = machine.Pin(6,machine.Pin.OUT)
echo = machine.Pin(7,machine.Pin.IN)

def distance():
    # pulse
    trig.high()
    time.sleep_us(10)
    trig.low()

    # get time
    pulse_width_us = machine.time_pulse_us(echo, machine.Pin.on)
    pulse_width_s= pulse_width_us/ 1000000.0

    # calculate the distance
    distance_m = pulse_width_s * 340 / 2
    distance_cm = (distance_m *100)

    return distance_cm

while True:
    dis = distance()
    print ('Distance: %.2f' % dis)
    time.sleep_ms(300)