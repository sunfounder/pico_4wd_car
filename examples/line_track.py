import pico_4wd as car

MOTOR_POWER = 60
REFERENCE = 10000

def main():
    while True:
        if car.get_greyscale_status(REFERENCE) == 0:
            car.move("forward", MOTOR_POWER)      
        elif car.get_greyscale_status(REFERENCE) == -1:
            car.move("left", MOTOR_POWER)
        elif car.get_greyscale_status(REFERENCE) == 1:
            car.move("right", MOTOR_POWER)   


try:
    main()
finally:
    car.move("stop")
    car.set_light_off()

