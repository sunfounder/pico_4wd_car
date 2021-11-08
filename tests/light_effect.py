import pico_4wd as car
import time

def rainbow():
    colors = [car.hue2rgb(hue) for hue in range(0, 360, 15)]
    print(colors)

    for i in range(24):
        car.write_light_color_at(i, colors[i-12])
    car.light_excute()
#     offset = -24
# 
#     while True:
#         for i in range(24):
#             car.write_light_color_at(i, colors[i+offset])
#         car.light_excute()
#         offset += 1
#         if offset == 0:
#             offset = -24
#         time.sleep(0.03)

def rear_light():
    YELLOW = [50, 10, 0]
    RED = [50, 0, 0]
    OFFSET = 8
    car.write_light_color_at(0 + OFFSET, YELLOW)
    car.write_light_color_at(1 + OFFSET, YELLOW)
    car.write_light_color_at(2 + OFFSET, RED)
    car.write_light_color_at(3 + OFFSET, RED)
    car.write_light_color_at(4 + OFFSET, RED)
    car.write_light_color_at(5 + OFFSET, RED)
    car.write_light_color_at(6 + OFFSET, YELLOW)
    car.write_light_color_at(7 + OFFSET, YELLOW)
    car.light_excute()

def turn_left_light():
    YELLOW = [50, 10, 0]
    OFFSET = 8
    car.write_light_color_at(0 + OFFSET, YELLOW)
    car.write_light_color_at(1 + OFFSET, YELLOW)
    car.light_excute()

def turn_right_light():
    YELLOW = [50, 10, 0]
    OFFSET = 8
    car.write_light_color_at(6 + OFFSET, YELLOW)
    car.write_light_color_at(7 + OFFSET, YELLOW)
    car.light_excute()

def bottom_light_effect():
    BLUE = [0, 0, 255]
    RED = [255, 0, 0]
    BOTTOM_LEFT_OFFSET = 0
    BOTTOM_RIGHT_OFFSET = 16
    for i in range(8):
        car.write_light_color_at(i+BOTTOM_LEFT_OFFSET, BLUE)
    for i in range(8):
        car.write_light_color_at(i+BOTTOM_RIGHT_OFFSET, RED)
    car.light_excute()

def rear_light_effect():
    brightness = 100
    colors = [[int(c * brightness / 255) for c in car.hue2rgb(hue)] for hue in range(0, 360, 45)]
    print(colors)

    for i in range(8):
        car.write_light_color_at(i+8, colors[i])
    for i in range(8):
        car.write_light_color_at(i+0, [255, 255, 255])
    for i in range(8):
        car.write_light_color_at(i+16, [255, 255, 255])
    car.light_excute()

def rear_light():
    BLUE = [0, 0, 100]
    RED = [100, 0, 0]
    OFFSET = 8
    car.write_light_color_at(0 + OFFSET, RED)
    car.write_light_color_at(1 + OFFSET, BLUE)
    car.write_light_color_at(3 + OFFSET, RED)
    car.write_light_color_at(4 + OFFSET, BLUE)
    car.write_light_color_at(6 + OFFSET, RED)
    car.write_light_color_at(7 + OFFSET, BLUE)
    for i in range(8):
        car.write_light_color_at(i+0, [255, 255, 255])
    for i in range(8):
        car.write_light_color_at(i+16, [255, 255, 255])
    
    car.light_excute()
