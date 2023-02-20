from ws2812 import WS2812

LIGHT_PIN = 19
LIGHT_NUM = 24

LIGHT_REAR_RIGHT = [0, 1]
LIGHT_REAR_MIDDLE = [2, 3, 4, 5]
LIGHT_REAR_LEFT = [6, 7]
LIGHT_REAR = [0, 1, 2, 3, 4, 5, 6, 7]

LIGHT_BOTTOM_LEFT = [8, 9, 10, 11, 12, 13, 14, 15]
LIGHT_BOTTOM_RIGHT = [16, 17, 18, 19, 20, 21, 22, 23]

np = WS2812(LIGHT_PIN, LIGHT_NUM)

def set_all_color(color):
    ''' set color to all lights 
        
        color list or hex, 1*3 list, the order is [red, green, blue] 
    '''
    for i in range(24):
        np[i] = color
    np.write()

# def set_color_at(num, color, preset=0):
#     if num > LIGHT_NUM:
#         raise ValueError("num must be less than LIGHT_NUM.")
#     np[num] = color
#     np.write()

def set_color_at(num, color):
    if isinstance(num,list):
        for i in num:
            if i > LIGHT_NUM:
                raise ValueError("num element must be less than LIGHT_NUM.")
            np[i] = color 
    elif  type(num) is int:
        if num > LIGHT_NUM:
            raise ValueError("num must be less than LIGHT_NUM.")
        np[num] = color
    else:
        raise ValueError("num must be list or int.")
    np.write()


def set_bottom_left_color(color):
    for num in LIGHT_BOTTOM_LEFT:
        np[num] = color
    np.write()

def set_bottom_right_color(color):
    for num in LIGHT_BOTTOM_RIGHT:
        np[num] = color
    np.write()

def set_bottom_color(color):
    for num in LIGHT_BOTTOM_LEFT:
        np[num] = color
    for num in LIGHT_BOTTOM_RIGHT:
        np[num] = color
    np.write()

def set_rear_right_color(color):
    for num in LIGHT_REAR_RIGHT:
        np[num] = color
    np.write()    

def set_rear_middle_color(color):
    for num in LIGHT_REAR_MIDDLE:
        np[num] = color
    np.write()

def set_rear_left_color(color):
    for num in LIGHT_REAR_LEFT:
        np[num] = color
    np.write()

def set_rear_color(color):
    for num in LIGHT_REAR:
        np[num] = color
    np.write()

def set_off():
    set_all_color([0, 0, 0])

# call function
if __name__ == "__main__":
    try:
        import time
        set_all_color(0x33aa66)
        time.sleep(0.5)
        set_bottom_left_color(0x6633ff)
        time.sleep(0.5)
        set_bottom_right_color([255,66,100])
        time.sleep(0.5)
        set_bottom_color(0x77ff00)
        time.sleep(0.5)
        set_rear_color(0x88aa00)
        time.sleep(0.5)
        set_rear_right_color(0xaa0000)
        time.sleep(0.5)
        set_rear_middle_color(0x00aa00)
        time.sleep(0.5)
        set_rear_left_color(0x0000aa)
        time.sleep(0.5)
        
        for i in range(8):
            set_off()
            time.sleep(0.01)
            set_color_at(i,0xaa00cc)
            time.sleep(0.3)
            
        set_off()
        time.sleep(0.1)
        set_color_at([1,3,5,7],0xccaa00)
        time.sleep(0.5)
        
        set_off()
        time.sleep(0.1)
        set_color_at([0,2,4,6],0x00ccaa)
        time.sleep(0.5)

    finally:
        set_off()
