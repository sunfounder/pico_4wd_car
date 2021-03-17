import pico_4wd as car
import time

moves = [
    "forward",
    "backward",
    "left",
    "right",
    "stop",
]

power = 100
def main():
    for move in moves:
        print(move)
        car.move(move, power)
        time.sleep(1)

try:
    main()
finally:
    car.move("stop")
