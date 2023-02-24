import motors as car
import lights
import time

def move(action,power=0):
    car.move(action,power)
    if action is "forward":
        lights.set_off()
        lights.set_bottom_color(0x00aa00)
        lights.set_rear_middle_color(0x00aa00)
    elif action is "left":
        lights.set_off()
        lights.set_rear_left_color(0xaaaa00)
        lights.set_bottom_left_color(0xaaaa00)
    elif action is "right":
        lights.set_off()
        lights.set_rear_right_color(0xaaaa00)
        lights.set_bottom_right_color(0xaaaa00)    
    elif action is "backward":
        lights.set_off()
        lights.set_rear_middle_color(0xaa0000)
        lights.set_bottom_color(0xaa0000) 
    else:
        lights.set_off()

if __name__ == "__main__":
    try:
        while True:
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
    finally:
        move("stop")
        lights.set_off()
        time.sleep(0.05)