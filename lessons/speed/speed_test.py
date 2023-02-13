from speed import Speed
import motors_helper as car
import time

sp = Speed(8, 9)

def test_speed():
    def helper(power):
        # power changes every 10%
        power = round(power / 10) * 10
        car.move("forward", power)
        print(f'Power(%%):{power}  Speed(cm/s):{sp.speed:.2f} Mileage(m):{sp.mileage:.2f}')
        time.sleep(0.2)

    while True:
        for power in range(100):
            helper(power)

        for power in range(100, -100, -1):
            helper(power)

        for power in range(-100, 0):
            helper(power)


if __name__ == '__main__':
    try:
        test_speed()
    finally:
        car.move("stop")
        time.sleep(0.5)