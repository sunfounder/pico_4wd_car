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

def set_light_all_color(color):
    ''' set color to all lights 
        
        color list or hex, 1*3 list, the order is [red, green, blue] 
    '''
    for i in range(24):
        np[i] = color
    np.write()

def set_light_color_at(num, color, preset=0):
    if num > LIGHT_NUM:
        raise ValueError("num must be less than LIGHT_NUM.")
    np[num] = color
    np.write()

def set_light_bottom_left_color(color):
    for num in LIGHT_BOTTOM_LEFT:
        np[num] = color
    np.write()

def set_light_bottom_right_color(color):
    for num in LIGHT_BOTTOM_RIGHT:
        np[num] = color
    np.write()

def set_light_bottom_color(color):
    for num in LIGHT_BOTTOM_LEFT:
        np[num] = color
    for num in LIGHT_BOTTOM_RIGHT:
        np[num] = color
    np.write()
    
def set_light_rear_color(color):
    for num in LIGHT_REAR:
        np[num] = color
    np.write()


def set_light_off():
    set_light_all_color([0, 0, 0])

