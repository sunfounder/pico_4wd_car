from machine import Pin, ADC
import pico_4wd as car
import time

vol_adc = ADC(Pin(26))
flag = 0
time_count = 0
try:
    while True:
        # if flag == 0:
        #     flag = 1
        #     car.move('forward', 100)
        # else:
        #     flag = 0
        #     car.move('backward', 100)  
        car.set_motor_power(90, -90, 90, -90)

        with open('battery_test.csv', 'a') as f:
            vol = vol_adc.read_u16() / 65535.0 * 3.3 * 3
            con = '%s\n'%(vol)
            print(con)
            f.write(con)
        time.sleep(1)  
except Exception as e:
    print(e)
finally:
    car.move('stop', 0)
    time.sleep(.2)