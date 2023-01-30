import time
import pico_4wd as car
from ws import WS_Server
from machine import Pin
from math import sqrt

''' Use the app Sunfounder Controller to control the Pico-4WD-Car

Usage: 
    https://docs.sunfounder.com/projects/pico-4wd-car/en/latest/get_started/app_control.html

Pico onboard LED status:
    - always on: working
    - blink: error 
'''


print("[ app control ]\n")

''' -------------- Onboard led Config -------------'''
onboard_led = Pin(25, Pin.OUT)

''' ---------------- Custom Config ----------------'''
'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
# WIFI_MODE = "ap"
# SSID = "YOUR_SSID_NAME"
# PASSWORD = "YOUR_PASSWORD_HERE"

# STA Mode
# WIFI_MODE = "sta"
# SSID = "YOUR_SSID_HERE"
# PASSWORD = "YOUR_PASSWORD_HERE"




'''Configure default power''' 
DEFAULT_POWER = 60

'''Configure steer sensitivity''' 
steer_sensitivity = 0.8 # 0 ~ 1

'''Configure grayscale module''' 
GRAYSCALE_LINE_REFERENCE_DEFAULT = 10000
GRAYSCALE_CLIFF_REFERENCE_DEFAULT = 2000
'''Configure radar''' 
# Normal
NORMAL_SCAN_ANGLE = 180
NORMAL_SCAN_STEP = 5

# obstacle_avoid
OBSTACLE_AVOID_SCAN_ANGLE = 50
OBSTACLE_AVOID_SCAN_STEP = 10
OBSTACLE_AVOID_REFERENCE = 20   # distance referenece (m)
OBSTACLE_AVOID_FORWARD_POWER = 30
OBSTACLE_AVOID_TURNING_POWER = 50

# follow
FOLLOW_SCAN_ANGLE = 90
FOLLOW_SCAN_STEP = 10
FOLLOW_REFERENCE = 25 # distance referenece (m)
FOLLOW_FORWARD_POWER = 40
FOLLOW_TURNING_POWER = 40

'''Configure the power of the line_track mode'''
line_track_power = 80

'''Configure singal light'''
# singal_on_color = [50, 50, 0] # yellow:[50, 50, 0]
singal_on_color = [80, 30, 0] # amber:[255, 191, 0]

singal_blink_interval = 500 # ms

'''------------ Global Variables -------------'''
led_status = False
brightness = 0
last_brightness = 0

move_status = 'stop'
last_move_status = False
brake_light_status= False
brake_light_time = 0

left_turn_signal = False
right_turn_signal = False
hazard_lights = False
singal_time_count = 0
singal_on_flag = False

mode = None
throttle_power = 0
steer_power = 0

radar_angle = 0
radar_distance = 0
radar_status = "safety" # "safety" or "danger"

grayscale_line_reference = 0
grayscale_cliff_reference = 0

'''------------ Instantiate WS_Server -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)

'''----------------- Fuctions ---------------------'''
def my_car_move(throttle_power, steer_power, gradually=False):
    power_l = 0
    power_r = 0

    '''single joystick '''
    if steer_power < 0:
        power_l = int((100 + 2*steer_sensitivity*steer_power)/100*throttle_power)
        power_r = int(throttle_power)
    else:
        power_l = int(throttle_power)
        power_r = int((100 - 2*steer_sensitivity*steer_power)/100*throttle_power)

    if gradually:
        car.set_motor_power_gradually(power_l, power_r, power_l, power_r)
    else:
        car.set_motor_power(power_l, power_r, power_l, power_r)

def get_dir(radar_data, split_str="0"):
    # get scan status of 0, 1
    radar_data = [str(i) for i in radar_data]
    radar_data = "".join(radar_data)

    # Split 0, leaves the free path
    paths = radar_data.split(split_str)

    # Calculate where is the widest
    max_paths = max(paths)
    if split_str == "0" and len(max_paths) < 4:
        return "left"
    elif split_str == "1" and len(max_paths) < 2:
        return "stop"

    # Calculate the direction of the widest 
    pos = radar_data.index(max_paths)
    pos += (len(max_paths) - 1) / 2 
    delta = len(radar_data) / 3
    if pos < delta:
        return "left"
    elif pos > 2 * delta:
        return "right"
    else:
        return "forward"

def line_track():
    if grayscale_line_reference != 0:
        car.GRAYSCALE_LINE_REFERENCE = grayscale_line_reference
    else:
        car.GRAYSCALE_LINE_REFERENCE = GRAYSCALE_LINE_REFERENCE_DEFAULT

    _power = line_track_power
    gs_data = car.get_greyscale_status()

    # if gs_data == [0, 1, 0]:
    #     my_car_move(_power, 0)
    # elif gs_data == [0, 1, 1]:
    #     my_car_move(_power, 50)
    # elif gs_data == [0, 0, 1]:
    #     my_car_move(_power, 95)
    # elif gs_data == [1, 1, 0]:
    #     my_car_move(_power, -50)
    # elif gs_data == [1, 0, 0]:
    #     my_car_move(_power, -95)

    if gs_data == [0, 1, 0]:
        car.set_motor_power(_power, _power, _power, _power)
    elif gs_data == [0, 1, 1]:
        car.set_motor_power(_power, int(_power/5), _power, int(_power/5))
    elif gs_data == [0, 0, 1]:
        car.set_motor_power(_power, int(-_power/2), _power, int(-_power/2))
    elif gs_data == [1, 1, 0]:
        car.set_motor_power(int(_power/5), _power, int(_power/5), _power)
    elif gs_data == [1, 0, 0]:
        car.set_motor_power(int(-_power/2), _power, int(-_power/2), _power)

def obstacle_avoid():
    global radar_status, radar_angle, radar_distance 

    car.RADAR_REFERENCE = OBSTACLE_AVOID_REFERENCE
    car.RADAR_STEP_ANGLE = OBSTACLE_AVOID_SCAN_STEP

    #--------- scan -----------
    radar_angle, radar_distance, radar_data = car.radar_scan()
    # If radar data return a int, means scan not finished, and the int is current angle status
    if isinstance(radar_data, int):
        # 0 means distance too close, 1 means distance safety
        if radar_data == 0 and radar_status != "danger":
            print("Danger!")
            radar_status = "danger"
            car.move("stop")
            car.set_radar_scan_angle(180)
        return
    else:
        radar_status = "safety"

    #---- analysis direction -----
    direction = get_dir(radar_data)
    
    #--------- move ------------
    if direction == "left" or direction == "right":
        if direction == "left":
            _scan_angle = -OBSTACLE_AVOID_SCAN_ANGLE/2
        else:
            _scan_angle = OBSTACLE_AVOID_SCAN_ANGLE/2

        distance = car.get_radar_distance_at(-_scan_angle/2)
        # time.sleep(0.5)
        time.sleep(0.1)
        car.move(direction, OBSTACLE_AVOID_TURNING_POWER)
        while True:
            distance = car.get_radar_distance_at(_scan_angle/2)
            status = car.get_radar_status(distance)
            if status == 1:
                break
    ## finally forward
    car.set_radar_scan_angle(OBSTACLE_AVOID_SCAN_ANGLE)
    car.move("forward", OBSTACLE_AVOID_FORWARD_POWER)
        
def follow():
    print("follow")
    global radar_angle, radar_distance 

    car.set_radar_scan_angle(FOLLOW_SCAN_ANGLE)
    car.RADAR_STEP_ANGLE = FOLLOW_SCAN_STEP
    car.RADAR_REFERENCE = FOLLOW_REFERENCE

    #--------- scan -----------
    radar_angle, radar_distance, radar_data = car.radar_scan()

    # If radar data return a int, means scan not finished, and the int is current angle status
    if isinstance(radar_data, int):
        return

    #---- analysis direction -----
    direction = get_dir(radar_data, split_str='1')

    #--------- move ------------
    if direction == "left":
        car.move("left", FOLLOW_TURNING_POWER)

    elif direction == "right":
        car.move("right", FOLLOW_TURNING_POWER)
    elif direction == "forward":
        car.move("forward", FOLLOW_FORWARD_POWER)
    else:
        car.move("stop")

def singal_lights_handler():
    global singal_time_count, singal_on_flag
    _light_nums = [0, 1, 6, 7]

    if hazard_lights:
        _light_on_nums = [0, 1, 6, 7]
    elif left_turn_signal:
        _light_on_nums = [6, 7]
    elif right_turn_signal:
        _light_on_nums = [0, 1]
    else:
        for i in _light_nums:
            car.write_light_color_at(i, [0, 0, 0], preset=car.LIGHT_REAR)
        car.light_excute() 
        return

    if (time.ticks_ms() - singal_time_count > singal_blink_interval):
        singal_time_count = time.ticks_ms()
        singal_on_flag = not singal_on_flag
        if singal_on_flag:
            for i in _light_on_nums:
                car.write_light_color_at(i, singal_on_color, preset=car.LIGHT_REAR)
        else:
            for i in _light_nums:
                car.write_light_color_at(i, [0, 0, 0], preset=car.LIGHT_REAR)                  
        car.light_excute()

def brake_lights_handler():
    global last_move_status, brake_light_status, brake_light_time
    if move_status == 'stop' :
        if last_move_status:
            brake_light_status = True
            last_move_status = False
    else:
        last_move_status = True

    if brake_light_status == True:
        if brake_light_time == 0:
            brake_light_time = time.time()
        if(time.time() - brake_light_time > 0.5):
            brake_light_status = False
            brake_light_time = 0
            for i in range(2, 6, 1):
                car.write_light_color_at(i, [0, 0, 0], preset=car.LIGHT_REAR)
        else:
            for i in range(2, 6, 1):
                car.write_light_color_at(i, [255, 0, 0], preset=car.LIGHT_REAR)

def bottom_lights_handler():
    global led_status, last_brightness
    if led_status:
        if brightness != last_brightness:
            last_brightness = brightness
            car.set_light_bottom_color([brightness, brightness, brightness])
    else:
        if last_brightness != 0:
            last_brightness = 0
            car.set_light_bottom_color([0, 0, 0])  

def on_receive(data):
    global throttle_power, steer_power, move_status, last_move_status, mode 
    global left_turn_signal, right_turn_signal, hazard_lights
    global grayscale_line_reference, grayscale_cliff_reference
    global led_status, brightness

    print("recv_data: %s"%data)

#     ''' data to display'''
#     # greyscale
#     ws.send_dict['A'] = car.get_grayscale_values()
#     # Speed measurement
#     ws.send_dict['B'] = car.speed()
#     # Speed mileage
#     ws.send_dict['C'] = car.speed.mileage / 100 # unit: meter   
#     # # radar and distance
#     ws.send_dict['D'] = [radar_angle, radar_distance]
#     ws.send_dict['J'] = radar_distance
#     
#     ''' remote control'''
#     # Move - power
#     if 'Q' in data.keys() and isinstance(data['Q'], int):
#         throttle_power = data['Q']
#     if 'K' in data.keys():
#         if data['K'] == "left":
#             if throttle_power == 0:
#                 throttle_power = DEFAULT_POWER
#             if steer_power > 0:
#                 steer_power = 0
#             steer_power -= int(throttle_power/2)
#             if steer_power < -100:
#                 steer_power = -100
#         elif data['K'] == "right":
#             if throttle_power == 0:
#                 throttle_power = DEFAULT_POWER
#             if steer_power < 0:
#                 steer_power = 0
#             steer_power += int(throttle_power/2)
#             if steer_power > 100:
#                 steer_power = 100
#         elif data['K'] == "forward":
#             steer_power = 0
#             if throttle_power == 0:
#                 throttle_power = DEFAULT_POWER
#         elif data['K'] == "backward":
#             steer_power = 0
#             if throttle_power == 0:
#                 throttle_power = -DEFAULT_POWER
#         else:
#             steer_power = 0
# 
#     # grayscale reference
#     if 'A' in data.keys() and isinstance(data['A'], list):
#         grayscale_cliff_reference = data['A'][0]
#         grayscale_line_reference = data['A'][1]
# 
#     # singal lights
#     if 'E' in data.keys():
#         left_turn_signal = data['E']
#     if 'F' in data.keys():
#         right_turn_signal = data['F'] 
#     if 'I' in data.keys():
#         hazard_lights = data['I'] 
# 
#     # Bottom LEDs
#     if 'M' in data.keys():
#         led_status = data['M']
#     if led_status and 'L' in data.keys() and isinstance(data['L'], int):
#         brightness = data['L']
# 
#     # mode select: None / Line Track / Obstacle Avoid / Follow
#     if 'N' in data.keys() and data['N'] == True:
#         mode = 'line track'
#     elif 'O' in data.keys() and data['O'] == True:
#         mode = 'obstacle avoid'
#     elif 'P' in data.keys() and data['P'] == True:
#         mode = 'follow'
#     else:
#         mode = None

def remote_handler():
    global throttle_power, steer_power, move_status
    global radar_angle, radar_distance
    global grayscale_cliff_reference
    
    ''' radar and distance '''
    if mode == None:
        car.set_radar_scan_angle(180)
        radar_angle, radar_distance = car.get_radar_distance()    

    ''' move '''
    # print('throttle_power: %s, steer_power: %s'%(throttle_power, steer_power))
    if throttle_power == 0 and steer_power == 0:
        move_status = 'stop'
    else:
        my_car_move(throttle_power, steer_power, gradually=True)
        move_status = 'move'

    ''' Line Track or Obstacle Avoid '''
    if move_status == 'stop':
        if mode == 'line track':
            line_track()
        elif mode == 'obstacle avoid':
            obstacle_avoid()
        elif mode == 'follow':
            follow()
        else:
            car.move('stop', 0)

    ''' Bottom Lights '''
    bottom_lights_handler()
    ''' Singal lights '''
    singal_lights_handler()
    ''' Brake lights '''
    brake_lights_handler()

def main():
    car.servo.set_angle(0)
    car.move('stop', 0)
    ws.on_receive = on_receive
    if ws.start():
        onboard_led.on()
        while True:
            ws.loop()

            try:
                remote_handler()   
            except Exception as e:
                print('remote_handler: %s'%e)            

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        f = open('log.txt', 'w')
        f.write("---------------\n")
        f.write('%s'%e)
        f.close()

    finally:
        car.move("stop")
        car.set_light_off()
        while True:
            time.sleep(0.25)
            onboard_led.off()
            time.sleep(0.25)
            onboard_led.on()
