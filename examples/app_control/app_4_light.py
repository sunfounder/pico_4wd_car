'''This example adds E and F widgets to control car lights.'''


import time
import motors as car
from ws import WS_Server
from machine import Pin
import lights as lights


'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# AP Mode
WIFI_MODE = "ap"
SSID = "" # your wifi name, if blank, use the set name "NAME"
PASSWORD = "12345678" # your password

'''------------ Global Variables -------------'''
# car move - D-pad & throttle
dpad_touched = False        
move_status = 'stop'
throttle_power = 0
steer_power = 0
steer_sensitivity = 0.8 # 0 ~ 1

# led
led_status = False


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

is_move_last  = False
brake_light_status= False
brake_light_time = 0
brake_light_brightness = 255 # 0 ~ 255
brake_light_brightness_flag = -1 # -1 or 1

'''Configure singal light'''
singal_on_color = [80, 30, 0] # amber:[255, 191, 0]
brake_on_color = [255, 0, 0] 




'''------------ Instantiate -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
onboard_led = Pin(25, Pin.OUT) 


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


'''----------------- on_receive (ws.loop()) ---------------------'''
def on_receive(data):
    global throttle_power, steer_power, move_status, dpad_touched
    global led_status, led_theme_code, led_theme_sum

    ''' if not connected, skip & stop '''
    if not ws.is_connected():
        return

    # Move - power
    if 'Q' in data.keys() and isinstance(data['Q'], int):
        throttle_power = data['Q']
    else:
        throttle_power = 0

    # Move - direction
    if 'K' in data.keys():
        #print(data['K'])
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

    # LEDs switch
    if 'E' in data.keys():
        led_status = data['E']

    if led_status:
        # LEDs color theme change
        if 'F' in data.keys() and data['F'] == True:
            led_theme_code = (led_theme_code + 1) % led_theme_sum
            print(f"set led theme color: {led_theme_code}, {led_theme[str(led_theme_code)][0]}")



def remote_handler():
    global throttle_power, steer_power, move_status, dpad_touched

    if dpad_touched:
        my_car_move(throttle_power, steer_power, gradually=True)


    ''' no operation '''
    if not dpad_touched:
        move_status = "stop"
        car.move('stop')

    # ''' Bottom Lights '''
    bottom_lights_handler()
    # ''' Singal lights '''
    singal_lights_handler()
    # ''' Brake lights '''
    brake_lights_handler()


'''----------------- main ---------------------'''
try:
   ws.on_receive = on_receive
   if ws.start():
        onboard_led.on()
        while True:
            ws.loop()
            remote_handler() 
except Exception as e:
    print(e)
finally:
    onboard_led.off()   
    car.move("stop")
    lights.set_off()    