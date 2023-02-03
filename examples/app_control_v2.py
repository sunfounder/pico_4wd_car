import time
import pico_4wd as car
from ws import WS_Server
from machine import Pin
from math import sqrt

'''*****************************************************************************************
Use the app Sunfounder Controller to control the Pico-4WD-Car

Usage:
    https://docs.sunfounder.com/projects/pico-4wd-car/en/latest/get_started/app_control.html

Pico onboard LED status:
    - always on: working
    - blink: error

*****************************************************************************************'''

VERSION = '1.1.0'
print(f"[ Pico-4WD Car App Control {VERSION}]\n")

''' -------------- Onboard led Config -------------'''
onboard_led = Pin(25, Pin.OUT)

''' ---------------- Custom Config ----------------'''
'''Whether print serial receive '''
RECEIVE_PRINT = False

'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
# WIFI_MODE = "ap"
# SSID = "" # your wifi name, if blank, use the set name "NAME"
# PASSWORD = "12345678" # your password

# STA Mode
WIFI_MODE = "sta"
SSID = "xiaoming_PC"
PASSWORD = "bugaosuni"

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


'''------------ Configure Voice Control Commands -------------'''
voice_commands = {
    # action : [[command , similar commands], [run time(s)]
    "forward": [["forward", "forwhat", "for what"], 3],
    "backward": [["backward"], 3],
    "left": [["left", "turn left"], 0.5],
    "right": [["right", "turn right", "while"], 0.5],
    "stop": [["stop"], 0.5],
}

current_voice_cmd = None
voice_start_time = 0
voice_max_time = 0

'''------------ Global Variables -------------'''
led_status = False

led_rear_brightness = 0.2
led_rear_min_brightness = 0.05
led_rear_max_brightness = 1

led_theme_code = 0
led_theme = {
    "0": [
        [255, 0, 255],  # all colors
        # [80, 30, 0],  # steer color
        # [255, 0, 0],  # brake color
    ],
    "1": [ [0, 255, 0]],
    "2": [ [0, 255, 255]],
    "3": [ [0, 0, 255]],
}
led_theme_sum = len(led_theme)

move_status = 'stop'
is_move_last  = False
brake_light_status= False
brake_light_time = 0

mode = None
throttle_power = 0
steer_power = 0

radar_angle = 0
radar_distance = 0
radar_status = "safety" # "safety" or "danger"

grayscale_line_reference = 0
grayscale_cliff_reference = 0

line_out_time = 0

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


def set_leds_on(leds_index:list, color:list = [255, 255, 255]):
    ''' Set the color of the LED for the selected number

    leds_index: list, select led indexers
    color: RGB color
    '''
    for i in leds_index:
        car.write_light_color_at(i, color)
    car.light_excute()

def set_leds_off(leds_index:list):
    if led_status:
        color = list(led_theme[str(led_theme_code)][0])
        for i in range(3):
            color[i] = int(color[i] * led_rear_brightness)
    else:
        color = [0, 0, 0]
    for i in leds_index:
        car.write_light_color_at(i, color)
    car.light_excute()

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
    global move_status, line_out_time

    if grayscale_line_reference != 0:
        car.GRAYSCALE_LINE_REFERENCE = grayscale_line_reference
    else:
        car.GRAYSCALE_LINE_REFERENCE = GRAYSCALE_LINE_REFERENCE_DEFAULT

    _power = line_track_power
    gs_data = car.get_greyscale_status()
    # print(f"gs_data: {gs_data}")

    if gs_data == [0, 0, 0] or gs_data == [1, 1, 1] or gs_data == [1, 0, 1]:
        if line_out_time == 0:
            line_out_time = time.time()
        if (time.time() - line_out_time > 2):
            car.move('stop')
            move_status = 'stop'
            line_out_time = 0
        return
    else:
        line_out_time = 0

    if gs_data == [0, 1, 0]:
        car.set_motor_power(_power, _power, _power, _power) # forward
        move_status = 'forward'
    elif gs_data == [0, 1, 1]:
        car.set_motor_power(_power, int(_power/5), _power, int(_power/5)) # right
        move_status = 'right'
    elif gs_data == [0, 0, 1]:
        car.set_motor_power(_power, int(-_power/2), _power, int(-_power/2)) # right plus
        move_status = 'right'
    elif gs_data == [1, 1, 0]:
        car.set_motor_power(int(_power/5), _power, int(_power/5), _power) # left
        move_status = 'left'
    elif gs_data == [1, 0, 0]:
        car.set_motor_power(int(-_power/2), _power, int(-_power/2), _power) # left plus
        move_status = 'left'

def obstacle_avoid():
    global radar_status, radar_angle, radar_distance
    global move_status

    car.RADAR_REFERENCE = OBSTACLE_AVOID_REFERENCE
    car.RADAR_STEP_ANGLE = OBSTACLE_AVOID_SCAN_STEP

    #--------- scan -----------
    radar_angle, radar_distance, radar_data = car.radar_scan()
    # If radar data return a int, means scan not finished, and the int is current angle status
    if isinstance(radar_data, int):
        # 0 means distance too close, 1 means distance safety
        if radar_data == 0 and radar_status != "danger":
            # print("Danger!")
            radar_status = "danger"
            car.move("stop")
            move_status = 'stop'
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
            set_leds_on([6, 7], singal_on_color)
            set_leds_off([0, 1])
        else:
            _scan_angle = OBSTACLE_AVOID_SCAN_ANGLE/2
            set_leds_on([0, 1], singal_on_color)
            set_leds_off([6, 7])
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
    set_leds_off([0, 1, 6, 7])


def follow():
    global radar_angle, radar_distance
    global move_status

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
        move_status = 'left'
    elif direction == "right":
        car.move("right", FOLLOW_TURNING_POWER)
        move_status = 'right'
    elif direction == "forward":
        car.move("forward", FOLLOW_FORWARD_POWER)
        move_status = 'forward'
    else:
        car.move("stop")
        move_status = 'stop'


def singal_lights_handler():
    _light_on_nums = None
    _light_off_nums = [0, 1, 6, 7]

    if move_status == 'left':
        _light_on_nums = [6, 7]
        _light_off_nums = [0, 1]
    elif move_status == 'right':
        _light_on_nums = [0, 1]
        _light_off_nums = [6, 7]
    else:
        _light_on_nums = None
        _light_off_nums = [0, 1, 6, 7]

    if _light_on_nums != None:
        set_leds_on(_light_on_nums, singal_on_color)

    if _light_off_nums != None:
        set_leds_off(_light_off_nums)


def brake_lights_handler():
    global is_move_last , brake_light_status, brake_light_time, led_status
    _light_nums = [2, 3, 4, 5]
    if move_status == 'stop' :
        if is_move_last :
            brake_light_status = True
            is_move_last  = False
    else:
        is_move_last  = True

    if brake_light_status == True:
        if brake_light_time == 0:
            brake_light_time = time.time()
        if(time.time() - brake_light_time > 0.5):
            brake_light_status = False
            brake_light_time = 0
        else:
            set_leds_on(_light_nums, [255, 0, 0])
    else:
            set_leds_off(_light_nums)

def bottom_lights_handler():
    global led_status
    if led_status:
        color = list(led_theme[str(led_theme_code)][0])
    else:
        color = [0, 0, 0]
    car.set_light_bottom_color(color)

def on_receive(data):
    global throttle_power, steer_power, move_status, is_move_last , mode
    global grayscale_line_reference, grayscale_cliff_reference
    global led_status, led_theme_code, led_theme_sum, led_rear_brightness
    global current_voice_cmd, voice_start_time, voice_max_time

    if RECEIVE_PRINT:
        print("recv_data: %s"%data)

    ''' data to display'''
    # greyscale
    ws.send_dict['A'] = car.get_grayscale_values()
    # Speed measurement
    ws.send_dict['B'] = car.speed() # uint: cm/s
    # Speed mileage
    ws.send_dict['C'] = car.speed.mileage # unit: meter
    # # radar and distance
    ws.send_dict['D'] = [radar_angle, radar_distance]
    ws.send_dict['J'] = radar_distance

    ''' remote control'''
    # Move - power
    if 'Q' in data.keys() and isinstance(data['Q'], int):
        throttle_power = data['Q']
        if throttle_power > 0:
            move_status = 'forward'
        elif throttle_power < 0:
            move_status = 'backward'
    else:
        throttle_power = 0
    # Move - direction
    if 'K' in data.keys():
        if data['K'] == "left":
            move_status = 'left'
            if throttle_power == 0:
                throttle_power = DEFAULT_POWER
            if steer_power > 0:
                steer_power = 0
            steer_power -= int(throttle_power/2)
            if steer_power < -100:
                steer_power = -100
        elif data['K'] == "right":
            move_status = 'right'
            if throttle_power == 0:
                throttle_power = DEFAULT_POWER
            if steer_power < 0:
                steer_power = 0
            steer_power += int(throttle_power/2)
            if steer_power > 100:
                steer_power = 100
        elif data['K'] == "forward":
            move_status = 'forward'
            steer_power = 0
            if throttle_power == 0:
                throttle_power = DEFAULT_POWER
        elif data['K'] == "backward":
            move_status = 'backward'
            steer_power = 0
            if throttle_power == 0:
                throttle_power = -DEFAULT_POWER
        else:
            steer_power = 0

    # grayscale reference
    if 'A' in data.keys() and isinstance(data['A'], list):
        grayscale_cliff_reference = data['A'][0]
        grayscale_line_reference = data['A'][1]

    # rear LEDs brightness
    if throttle_power < 0:
        led_rear_brightness = (-throttle_power)/100
    else:
        led_rear_brightness = throttle_power/100
    if led_rear_brightness < led_rear_min_brightness:
        led_rear_brightness = led_rear_min_brightness
    elif led_rear_brightness > led_rear_max_brightness:
        led_rear_brightness = led_rear_max_brightness

    # LEDs switch
    if 'E' in data.keys():
        led_status = data['E']

    if led_status:
        # LEDs color theme change
        if 'F' in data.keys() and data['F'] == True:
            led_theme_code = (led_theme_code + 1) % led_theme_sum
            print(f"set led theme color: {led_theme_code}, {led_theme[str(led_theme_code)][0]}")

    # mode select: None / Line Track / Obstacle Avoid / Follow
    if 'N' in data.keys() and data['N'] == True:
        if mode != 'line track':
            mode = 'line track'
            print(f"change mode to: {mode}")
    elif 'O' in data.keys() and data['O'] == True:
        if mode != 'obstacle avoid':
            mode = 'obstacle avoid'
            print(f"change mode to: {mode}")
    elif 'P' in data.keys() and data['P'] == True:
        if mode != 'follow':
            mode = 'follow'
            print(f"change mode to: {mode}")
    else:
        if mode != None:
            mode = None
            print(f"change mode to: {mode}")

    # Voice control
    if 'I' in data.keys():
        voice_text = data['I']
    if voice_text != None or voice_text != '':
        print(f"voice_text: {voice_text}")
        for vcmd in voice_commands:
            if voice_text in voice_commands[vcmd][0]:
                print(f"voice control match: {vcmd}")
                current_voice_cmd = vcmd
                voice_max_time =  voice_commands[vcmd][1]
                break
        else:
            print(f"voice control without match")


def remote_handler():
    global throttle_power, steer_power, move_status
    global radar_angle, radar_distance
    global grayscale_cliff_reference
    global current_voice_cmd, voice_start_time, voice_max_time

    ''' radar and distance '''
    if mode == None:
        car.set_radar_scan_angle(180)
        radar_angle, radar_distance = car.get_radar_distance()


    _joystick_touched = False
    if throttle_power != 0 or steer_power != 0:
        _joystick_touched = True

    ''' move '''
    # print('throttle_power: %s, steer_power: %s'%(throttle_power, steer_power))
    if _joystick_touched:
        my_car_move(throttle_power, steer_power, gradually=True)

    ''' Line Track or Obstacle Avoid '''
    if not _joystick_touched:
        if mode == 'line track':
            radar_angle = 0
            radar_distance = car.get_radar_distance_at(0)
            line_track()
        elif mode == 'obstacle avoid':
            obstacle_avoid()
        elif mode == 'follow':
            follow()
        else:
            car.move('stop', 0)
            move_status = 'stop'

    ''' Voice Control '''
    if not _joystick_touched:
        voice_control_power = 50
        if current_voice_cmd != None and voice_max_time != 0:
            if voice_start_time == 0:
                voice_start_time = time.time()
            if (time.time() - voice_start_time < voice_max_time):
                if current_voice_cmd == "forward":
                    car.move("forward", voice_control_power)
                    move_status = "forward"
                elif current_voice_cmd == "backward":
                    car.move("backward", voice_control_power)
                    move_status = "backward"
                elif current_voice_cmd == "right":
                    car.move("right", voice_control_power)
                    move_status = "right"
                elif current_voice_cmd == "left":
                    car.move("left", voice_control_power)
                    move_status = "left"
                elif current_voice_cmd == "stop":
                    car.move("stop", voice_control_power)
                    move_status = "stop"
            else:
                current_voice_cmd = None
                voice_start_time = 0
                voice_max_time = 0
    else:
        current_voice_cmd = None
        voice_start_time = 0
        voice_max_time = 0


    # print(f'move_status {move_status}')
    # ''' Bottom Lights '''
    bottom_lights_handler()
    # ''' Singal lights '''
    singal_lights_handler()
    # ''' Brake lights '''
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
