import pico_4wd as car
import time


try:
    car.move('forward', 100)
    t_s = time.ticks_ms()
    t_count = 0
    while True:
        t_temp = time.ticks_ms()
        t_count = t_temp - t_s
        t_s = t_temp
        print("time: %s, speed: %s cm/s, mileage: %s m"%(t_count, car.speed(), car.speed.mileage))
        time.sleep(.2)
finally:
    car.move('stop', 0)
    time.sleep(.02)
