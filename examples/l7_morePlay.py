import pico_4wd as car

mode = 4

def main():
    while True:
        global mode
        if mode == 1:
            car.avoid(40,30)
        elif mode == 2:
            car.follow(40,30)
        elif mode == 3:
            car.is_on_edge(800)
        elif mode == 4:
            car.track_line(10000,50)

try:
    main()
finally:
    car.move("stop")
