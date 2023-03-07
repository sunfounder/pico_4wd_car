import motors as car
from servo import Servo
from grayscale import Grayscale
import time

# init grayscale module
gs = Grayscale(26, 27, 28)
gs.set_edge_reference(1000)

# init servo
servo = Servo(18)
servo.set_angle(0)

MOTOR_POWER = 50

def shake_head():
    for angle in range(0, 90, 10):
        servo.set_angle(angle)
        time.sleep(0.01)
    for angle in range(90, -90, -10):
        servo.set_angle(angle)
        time.sleep(0.01)
    for angle in range(-90, 0, 10):
        servo.set_angle(angle)
        time.sleep(0.01)

def main():
    while True:
        print(gs.get_value())
        if gs.is_on_edge():
            car.move("backward", MOTOR_POWER)
            shake_head()
        else:
            car.move("stop")

try:
    main()
finally:
    car.move("stop")
    time.sleep(0.05)
    
