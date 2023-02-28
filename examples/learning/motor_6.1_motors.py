''' 
This file is only for learning, 
please refer to the libs file for actual use.
'''

from motor import Motor
import time

# init
left_front  = Motor(17, 16, dir=-1)
right_front = Motor(15, 14, dir= 1)
left_rear   = Motor(13, 12, dir=-1)
right_rear  = Motor(11, 10, dir= 1)
motors = [left_front, right_front, left_rear, right_rear]

# run all 4 motors
def set_motors_power(powers:list):
    ''' set motors power
        powers list, 1*4 list powers of each motor, the order is [left_front, right_front, left_rear, right_rear]
    '''
    if len(powers) != 4:
        raise ValueError("powers should be a 1*4 list.")

    for i, motor in enumerate(motors):
        motor.run(powers[i])

def move(action, power=0):
    if action == "forward":
        set_motors_power([power, power, power, power])
    elif action == "backward":
        set_motors_power([-power, -power, -power, -power])
    elif action == "left":
        set_motors_power([-power, power, -power, power])
    elif action == "right":
        set_motors_power([power, -power, power, -power])
    else:
        set_motors_power([0, 0, 0, 0])

# call the car move funtion
if __name__ == "__main__":
    speed = 50
    act_list = [
        "forward",
        "backward",
        "left",
        "right",
        "stop",
    ]
    for act in act_list:
        print(act)
        move(act, speed)
        time.sleep(1)