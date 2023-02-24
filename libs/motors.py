from motor import Motor
import time

left_front  = Motor(17, 16, dir=-1)
right_front = Motor(15, 14, dir= 1)
left_rear   = Motor(13, 12, dir=-1)
right_rear  = Motor(11, 10, dir= 1)
motors = [left_front, right_front, left_rear, right_rear]

def set_motors_power(powers:list):
    ''' set motors power 
        powers list, 1*4 list powers of each motor, the order is [left_front, right_front, left_rear, right_rear]
    '''
    if len(powers) != 4:
        raise ValueError("powers should be a 1*4 list.")

    for i, motor in enumerate(motors):
        motor.run(powers[i])

def set_motors_power_gradually(powers:list):
    '''
        slowly increase power of the motor, to avoid hight reverse voltage from motors
    '''
    if len(powers) != 4:
        raise ValueError("powers should be a 1*4 list.")

    flags = [True, True, True, True]
    while flags[0] or flags[1] or flags[2] or flags[3]:
        for i, motor in enumerate(motors):
            if motor.current_power > powers[i]:
                motor.run(motor.current_power - 1)
            elif motor.current_power < powers[i]:
                motor.run(motor.current_power + 1)
            else:
                flags[i] = False
        time.sleep_ms(1)

def stop():
    set_motors_power([0, 0, 0, 0])


def move(action, power=0):
    if action == "forward":
        set_motors_power_gradually([power, power, power, power])
    elif action == "backward":
        set_motors_power_gradually([-power, -power, -power, -power])
    elif action == "left":
        set_motors_power_gradually([-power, power, -power, power])
    elif action == "right":
        set_motors_power_gradually([power, -power, power, -power])
    else:
        # set_motors_power_gradually([0, 0, 0, 0])
        set_motors_power([0, 0, 0, 0])


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
