'''*****************************************************************************************
Use the app Sunfounder Controller to control the Pico-4WD-Car

https://github.com/sunfounder/pico_4wd_car/tree/v2.0

Pico onboard LED status:
    - off: not working
    - always on: working
    - blink: error

*****************************************************************************************'''
import time
import sys
import motors as car
import sonar as sonar
import lights as lights
from speed import Speed
from grayscale import Grayscale
from ws import WS_Server
from machine import Pin

VERSION = '1.3.0'
print(f"[ Pico-4WD Car App Control {VERSION}]\n")

'''
 "w" mode will clear the previous log first, if you need to keep it,
 please use the "a" mode
'''
LOG_FILE = "log.txt"

# "a" mode
# with open(LOG_FILE, "a") as log_f:
#     Separation_Line = "\n" + "-"*30 + "\n"
#     log_f.write(Separation_Line)

# "w" mode
with open(LOG_FILE, "w") as log_f:
    log_f.write("")

''' -------------- Onboard led Config -------------'''
onboard_led = Pin(25, Pin.OUT)

''' ---------------- Custom Config ----------------'''
'''Whether print serial receive '''
RECEIVE_PRINT = False

'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
WIFI_MODE = "ap"
SSID = "" # your wifi name, if blank, use the set name "NAME"
PASSWORD = "12345678" # your password

# STA Mode
# WIFI_MODE = "sta"
# SSID = "YOUR SSID"
# PASSWORD = "YOUR PASSWORD"

'''Configure steer sensitivity'''
steer_sensitivity = 0.8 # 0 ~ 1

'''Configure grayscale module'''
GRAYSCALE_LINE_REFERENCE_DEFAULT = 10000
GRAYSCALE_CLIFF_REFERENCE_DEFAULT = 2000

'''Configure sonar'''
# Normal
NORMAL_SCAN_ANGLE = 180
NORMAL_SCAN_STEP = 5

# obstacle_avoid
OBSTACLE_AVOID_SCAN_ANGLE = 60
OBSTACLE_AVOID_SCAN_STEP = 10
OBSTACLE_AVOID_REFERENCE = 25   # distance referenece (cm)
OBSTACLE_AVOID_FORWARD_POWER = 30
OBSTACLE_AVOID_TURNING_POWER = 50

# follow
FOLLOW_SCAN_ANGLE = 90
FOLLOW_SCAN_STEP = 5
FOLLOW_REFERENCE = 20 # distance referenece (m)
FOLLOW_FORWARD_POWER = 20
FOLLOW_TURNING_POWER = 15

# voice control power
VOICE_CONTROL_POWER = 50

'''Configure the power of the line_track mode'''
LINE_TRACK_POWER = 80

'''Configure singal light'''
singal_on_color = [80, 30, 0] # amber:[255, 191, 0]
brake_on_color = [255, 0, 0] 

'''------------ Configure Voice Control Commands -------------'''
voice_commands = {
    # action : [[command , similar commands], [run time(s)]
    "forward": [["forward", "forwhat", "for what"], 3],
    "backward": [["backward"], 3],
    "left": [["left", "turn left"], 1],
    "right": [["right", "turn right", "while", "white"], 1],
    "stop": [["stop"], 1],
}

current_voice_cmd = None
voice_start_time = 0
voice_max_time = 0

'''------------ Global Variables -------------'''
led_status = False

lights_brightness = 0.2
led_rear_min_brightness = 0.08
led_rear_max_brightness = 1

led_theme_code = 0
led_theme = {
    "0": [0, 0, 255], # blue
    "1": [255, 0, 255], # purple
    "2": [200, 0, 0], # red 
    "3": [128, 20, 0], # orange 
    "4": [128, 128, 0], # yellow 
    "5": [0, 128, 0], # green
}
led_theme_sum = len(led_theme)

dpad_touched = False
move_status = 'stop'
is_move_last  = False
brake_light_status= False
brake_light_time = 0
brake_light_brightness = 255 # 0 ~ 255
brake_light_brightness_flag = -1 # -1 or 1

anti_fall_enabled = False
on_edge = False

mode = None
throttle_power = 0
steer_power = 0

sonar_on = True
sonar_angle = 0
sonar_distance = 0
avoid_proc = "scan" # obstacle process, "scan", "getdir", "stop", "forward", "left", "right"
avoid_has_obstacle = False

line_out_time = 0

'''------------ Instantiate -------------'''
try:
    speed = Speed(8, 9)
    grayscale = Grayscale(26, 27, 28)
    ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
except Exception as e:
    onboard_led.off()
    sys.print_exception(e)
    with open(LOG_FILE, "a") as log_f:
        log_f.write('\n> ')
        sys.print_exception(e, log_f)
    sys.exit(1) # if ws init failed, exit

'''----------------- motors fuctions ---------------------'''
def my_car_move(throttle_power, steer_power, gradually=False):
    power_l = 0
    power_r = 0

    if steer_power < 0:
        power_l = int((100 + 2*steer_sensitivity*steer_power)/100*throttle_power)
        power_r = int(throttle_power)
    else:
        power_l = int(throttle_power)
        power_r = int((100 - 2*steer_sensitivity*steer_power)/100*throttle_power)

    if gradually:
        car.set_motors_power_gradually([power_l, power_r, power_l, power_r])
    else:
        car.set_motors_power([power_l, power_r, power_l, power_r])

'''------- get_dir (sonar sacn data to direction) ---------------------'''
def get_dir(sonar_data, split_str="0"):
    # get scan status of 0, 1
    sonar_data = [str(i) for i in sonar_data]
    sonar_data = "".join(sonar_data)

    # Split 0, leaves the free path
    paths = sonar_data.split(split_str)

    # Calculate where is the widest
    max_paths = max(paths)
    if split_str == "0" and len(max_paths) < 4:
        return "left"
    elif split_str == "1" and len(max_paths) < 2:
        return "stop"

    # Calculate the direction of the widest
    pos = sonar_data.index(max_paths)
    pos += (len(max_paths) - 1) / 2
    delta = len(sonar_data) / 3
    if pos < delta:
        return "left"
    elif pos > 2 * delta:
        return "right"
    else:
        return "forward"

'''----------------- line_track ---------------------'''
def line_track():
    global move_status, line_out_time
    _power = LINE_TRACK_POWER
    gs_data = grayscale.get_line_status()
    # print(f"gs_data: {gs_data}, {grayscale.line_ref}")

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
        car.set_motors_power([_power, _power, _power, _power]) # forward
        move_status = 'forward'
    elif gs_data == [0, 1, 1]:
        car.set_motors_power([_power, int(_power/5), _power, int(_power/5)]) # right
        move_status = 'right'
    elif gs_data == [0, 0, 1]:
        car.set_motors_power([_power, int(-_power/2), _power, int(-_power/2)]) # right plus
        move_status = 'right'
    elif gs_data == [1, 1, 0]:
        car.set_motors_power([int(_power/5), _power, int(_power/5), _power]) # left
        move_status = 'left'
    elif gs_data == [1, 0, 0]:
        car.set_motors_power([int(-_power/2), _power, int(-_power/2), _power]) # left plus
        move_status = 'left'

'''----------------- obstacle_avoid ---------------------'''
def obstacle_avoid():
    global sonar_angle, sonar_distance, avoid_proc, avoid_has_obstacle
    global move_status

    # scan
    if avoid_proc == 'scan':
        if not avoid_has_obstacle:
            sonar.set_sonar_scan_config(OBSTACLE_AVOID_SCAN_ANGLE, OBSTACLE_AVOID_SCAN_STEP)
            move_status = 'forward'
            car.move('forward', OBSTACLE_AVOID_FORWARD_POWER)
        else:
            sonar.set_sonar_scan_config(180, OBSTACLE_AVOID_SCAN_STEP)
            move_status = 'stop'
            car.move('stop')
        sonar_angle, sonar_distance, sonar_data = sonar.sonar_scan()
        if isinstance(sonar_data, int):
            # 0 means distance too close, 1 means distance safety
            if sonar_data == 0:
                avoid_has_obstacle = True
                return
            else:
                return
        else:
            avoid_proc = 'getdir'

    # getdir
    if avoid_proc == 'getdir':
        avoid_proc = get_dir(sonar_data)

    # move: stop, forward
    if avoid_proc == 'stop':
        avoid_has_obstacle = True
        move_status = 'stop'
        car.move('stop')
        avoid_proc = 'scan'
    elif avoid_proc == 'forward':
        avoid_has_obstacle = False
        move_status = 'forward'
        car.move('forward', OBSTACLE_AVOID_FORWARD_POWER)
        avoid_proc = 'scan'
    elif avoid_proc == 'left' or avoid_proc == 'right':
        avoid_has_obstacle = True
        if avoid_proc == 'left':
            move_status = 'left'
            car.move('left', OBSTACLE_AVOID_TURNING_POWER)
            sonar_angle = 20 # servo turn right 20 
        else:
            move_status = 'right'
            car.move('right', OBSTACLE_AVOID_TURNING_POWER)
            sonar_angle = -20 # servo turn left 20 
        sonar.servo.set_angle(sonar_angle)
        time.sleep(0.2)
        avoid_proc = 'turn'

    # turn: left, right
    if avoid_proc == 'turn':
        sonar_distance = sonar.get_distance_at(sonar_angle)
        status = sonar.get_sonar_status(sonar_distance)
        if status == 1:
            avoid_has_obstacle = False
            avoid_proc = 'scan'
            move_status = 'forward'
            car.move("forward", OBSTACLE_AVOID_FORWARD_POWER)
            sonar.servo.set_angle(0)

'''----------------- follow ---------------------'''
def follow():
    global sonar_angle, sonar_distance
    global move_status

    sonar.set_sonar_scan_config(FOLLOW_SCAN_ANGLE, FOLLOW_SCAN_STEP)
    sonar.set_sonar_reference(FOLLOW_REFERENCE)

    #--------- scan -----------
    sonar_angle, sonar_distance, sonar_data = sonar.sonar_scan()
    # time.sleep(0.02)

    # If sonar data return a int, means scan not finished, and the int is current angle status
    if isinstance(sonar_data, int):
        return

    #---- analysis direction -----
    direction = get_dir(sonar_data, split_str='1')

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

'''----------------- singal_lights_handler ---------------------'''
def singal_lights_handler():
    if move_status == 'left':
        lights.set_rear_left_color(singal_on_color)
        lights.set_rear_right_color(0x000000)
    elif move_status == 'right':
        lights.set_rear_left_color(0x000000)
        lights.set_rear_right_color(singal_on_color)
    else:
        lights.set_rear_left_color(0x000000)
        lights.set_rear_right_color(0x000000)

def brake_lights_handler():
    global is_move_last , brake_light_status, brake_light_time, led_status, brake_light_brightness
    global brake_light_brightness, brake_light_brightness_flag

    if move_status == 'stop':
        if brake_light_brightness_flag == 1:
            brake_light_brightness += 5
            if brake_light_brightness > 255:
                brake_light_brightness = 255
                brake_light_brightness_flag = -1
        elif brake_light_brightness_flag == -1:
            brake_light_brightness -= 5
            if brake_light_brightness < 0:
                brake_light_brightness = 0
                brake_light_brightness_flag = 1          
        brake_on_color = [brake_light_brightness, 0, 0]
        lights.set_rear_color(brake_on_color)
    else:
        if is_move_last:
            lights.set_rear_middle_color(0x000000)
        else:
            lights.set_rear_color(0x000000)
        is_move_last = True
        brake_light_brightness = 255

def bottom_lights_handler():
    global led_status
    if led_status:
        color = list(led_theme[str(led_theme_code)])
    else:
        color = [0, 0, 0]
    lights.set_bottom_color(color)

'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):
    global throttle_power, steer_power, move_status, is_move_last , mode, dpad_touched
    global led_status, led_theme_code, led_theme_sum, lights_brightness
    global current_voice_cmd, voice_start_time, voice_max_time
    global sonar_on
    global anti_fall_enabled

    if RECEIVE_PRINT:
        print("recv_data: %s"%data)

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        sonar.servo.set_angle(0)
        car.move('stop', 0)
        return

    ''' data to display'''
    # greyscale
    ws.send_dict['A'] = grayscale.get_value()
    # Speed measurement
    ws.send_dict['B'] = round(speed.get_speed(), 2) # uint: cm/s
    # Speed mileage
    ws.send_dict['C'] = speed.get_mileage() # unit: meter
    # # sonar and distance
    ws.send_dict['D'] = [sonar_angle, sonar_distance]
    ws.send_dict['J'] = sonar_distance

    ''' remote control'''
    # Move - power
    if 'Q' in data.keys() and isinstance(data['Q'], int):
        throttle_power = data['Q']
    else:
        throttle_power = 0

    # Move - direction
    if 'K' in data.keys():
        if data['K'] == "left":
            dpad_touched = True
            move_status = 'left'
            if steer_power > 0:
                steer_power = 0
            steer_power -= int(throttle_power/2)
            if steer_power < -100:
                steer_power = -100
        elif data['K'] == "right":
            dpad_touched = True
            move_status = 'right'
            if steer_power < 0:
                steer_power = 0
            steer_power += int(throttle_power/2)
            if steer_power > 100:
                steer_power = 100
        elif data['K'] == "forward":
            dpad_touched = True
            move_status = 'forward'
            steer_power = 0
        elif data['K'] == "backward":
            dpad_touched = True
            move_status = 'backward'
            steer_power = 0
            throttle_power = -throttle_power
        else:
            dpad_touched = False
            move_status = 'stop'
            steer_power = 0

    if throttle_power == 0:
        move_status = 'stop'

    # grayscale reference
    if 'A' in data.keys() and isinstance(data['A'], list):
        grayscale.set_edge_reference(data['A'][0])
        grayscale.set_line_reference(data['A'][1])
    else:
        grayscale.set_edge_reference(GRAYSCALE_CLIFF_REFERENCE_DEFAULT)
        grayscale.set_line_reference(GRAYSCALE_LINE_REFERENCE_DEFAULT)

    # rear LEDs brightness
    if throttle_power < 0:
        lights_brightness = (-throttle_power)/100
    else:
        lights_brightness = throttle_power/100
    if lights_brightness < led_rear_min_brightness:
        lights_brightness = led_rear_min_brightness
    elif lights_brightness > led_rear_max_brightness:
        lights_brightness = led_rear_max_brightness

    # LEDs switch
    if 'E' in data.keys():
        led_status = data['E']

    if led_status:
        # LEDs color theme change
        if 'F' in data.keys() and data['F'] == True:
            led_theme_code = (led_theme_code + 1) % led_theme_sum
            print(f"set led theme color: {led_theme_code}, {led_theme[str(led_theme_code)][0]}")

    # enable sonar_sacn in normal mode
    # if 'G' in data.keys() and data['M'] == True:
    #     sonar_on = True
    # else:
    #     sonar_on = False

    # mode select: None / Anti fall / Line Track / Obstacle Avoid / Follow
    if 'M' in data.keys() and data['M'] == True:
        if mode != 'anti fall':
            mode = 'anti fall'
            print(f"change mode to: {mode}")        
    elif 'N' in data.keys() and data['N'] == True:
        if mode != 'line track':
            mode = 'line track'
            print(f"change mode to: {mode}")
    elif 'O' in data.keys() and data['O'] == True:
        if mode != 'obstacle avoid':
            mode = 'obstacle avoid'
            sonar.set_sonar_reference(OBSTACLE_AVOID_REFERENCE)
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
    voice_text = None
    if 'I' in data.keys() and  data['I'] != '':
        ws.send_dict['I'] = 1
        voice_text = data['I']
    else:
        ws.send_dict['I'] = 0
        
    if voice_text != None:
        print(f"voice_text: {voice_text}")
        for vcmd in voice_commands:
            if voice_text in voice_commands[vcmd][0]:
                print(f"voice control match: {vcmd}")
                current_voice_cmd = vcmd
                voice_max_time =  voice_commands[vcmd][1]
                break
        else:
            print(f"voice control without match")

'''----------------- remote_handler ---------------------'''
def remote_handler():
    global mode, throttle_power, steer_power, move_status, dpad_touched
    global sonar_angle, sonar_distance
    global current_voice_cmd, voice_start_time, voice_max_time
    global lights_brightness
    global on_edge

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        sonar.servo.set_angle(0)
        car.move('stop', 0)
        mode = None
        return
    
    ''' sonar and distance '''
    if mode == None or mode == 'anti fall':
        if sonar_on:
            sonar.set_sonar_scan_config(NORMAL_SCAN_ANGLE, NORMAL_SCAN_STEP)
            sonar_angle, sonar_distance, _ = sonar.sonar_scan()
        else:
            sonar_angle = 0
            sonar_distance = sonar.get_distance_at(sonar_angle)

    ''' move && anti-fall '''
    if mode == "anti fall":
        if grayscale.is_on_edge():
            if dpad_touched and move_status == "backward":
                my_car_move(throttle_power, steer_power, gradually=True)
            else:
                move_status = "stop"
                car.move("stop")
        else:
            if dpad_touched:
                my_car_move(throttle_power, steer_power, gradually=True)
            else:
                move_status = "stop"
                car.move("stop")                
    elif dpad_touched:
        my_car_move(throttle_power, steer_power, gradually=True)

    ''' mode: Line Track or Obstacle Avoid or Follow '''
    if not dpad_touched and mode != 'anti fall':
        if mode == 'line track':
            sonar_angle = 0
            sonar_distance = sonar.get_distance_at(0)
            line_track()
        elif mode == 'obstacle avoid':
            obstacle_avoid()
        elif mode == 'follow':
            follow()

    ''' Voice Control '''
    if current_voice_cmd != None and not dpad_touched and (mode == None or mode == 'anti fall'):
        if mode == 'anti fall':
            if grayscale.is_on_edge() and current_voice_cmd != "backward":
                car.move("stop")
                move_status = "stop"
                current_voice_cmd = "stop"

        if voice_max_time != 0:
            if voice_start_time == 0:
                voice_start_time = time.time()
            if ((time.time() - voice_start_time) < voice_max_time):
                # lights_brightness
                lights_brightness = VOICE_CONTROL_POWER/100
                #
                if current_voice_cmd == "forward":
                    car.move("forward", VOICE_CONTROL_POWER)
                    move_status = "forward"
                elif current_voice_cmd == "backward":
                    car.move("backward", VOICE_CONTROL_POWER)
                    move_status = "backward"
                elif current_voice_cmd == "right":
                    car.move("right", VOICE_CONTROL_POWER)
                    move_status = "right"
                elif current_voice_cmd == "left":
                    car.move("left", VOICE_CONTROL_POWER)
                    move_status = "left"
                elif current_voice_cmd == "stop":
                    car.move("stop")
                    move_status = "stop"
            else:
                current_voice_cmd = None
                voice_start_time = 0
                voice_max_time = 0
    else:
        current_voice_cmd = None
        voice_start_time = 0
        voice_max_time = 0

    ''' no operation '''
    if not dpad_touched and mode == None and current_voice_cmd == None:
        move_status = "stop"
        car.move('stop')

    # ''' Bottom Lights '''
    bottom_lights_handler()
    # ''' Singal lights '''
    singal_lights_handler()
    # ''' Brake lights '''
    brake_lights_handler()

'''----------------- main ---------------------'''
def main():
    sonar.servo.set_angle(0)
    car.move('stop')
    ws.on_receive = on_receive
    if ws.start():
        onboard_led.on()
        while True:
            ws.loop()
            remote_handler()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.print_exception(e)
        with open(LOG_FILE, "a") as log_f:
            log_f.write('\n> ')
            sys.print_exception(e, log_f)
    finally:
        car.move("stop")
        lights.set_off()
        ws.set("RESET", timeout=2500)
        while True: # pico onboard led blinking indicates error
            time.sleep(0.25)
            onboard_led.off()
            time.sleep(0.25)
            onboard_led.on()

