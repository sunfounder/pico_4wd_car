import time
import pico_4wd as car
from ws import WS_Server
from machine import Pin

print("[ app control ]\n")

''' -------------- Onboard led Config ------------- '''
onboard_led = Pin(25, Pin.OUT)

''' ---------------- Custom Config ---------------- '''
'''Set name'''
NAME = 'my_4wd_car'

'''Configure wifi'''
# STA Mode
# WIFI_MODE = "sta"
# SSID = "YOUR_SSID_HERE"
# PASSWORD = "YOUR_PASSWORD_HERE"


# AP Mode
# WIFI_MODE = "ap"
# SSID = "YOUR_SSID_NAME"
# PASSWORD = "YOUR_PASSWORD_HERE"

'''Configure grayscale module reference value''' 
# car.GRAYSCALE_LINE_REFERENCE = 10000
car.GRAYSCALE_LINE_REFERENCE = 17000

'''Configure radar rotation increment''' 
car.RADAR_STEP_ANGLE = 5

'''Configure the power of the line_track mode'''
line_track_power = 100

'''------------ Global Variables -------------'''
led_status = False
move_status = 'stop'
last_move_status = False
brake_light_status= False
brake_light_time = 0

left_trun_signal = False
right_trun_signal = False
hazard_lights = False
singal_time_count = 0
singal_blink_interval = 500 # ms
singal_on_flag = False
# singal_on_color = [50, 50, 0] # yellow:[50, 50, 0]
singal_on_color = [80, 30, 0] # amber:[255, 191, 0]

mode = None
throttle_power = 0
steer_power = 0

radar_angle = 0
radar_distance = 0


'''------------ Instantiate WS_Server -------------'''
ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)


def line_track():
    global line_t_count

    print('line_track')
    _power = line_track_power
    gs_data = car.get_greyscale_status()
    if gs_data == [0, 1, 0]:
        car.set_motor_power(_power, _power, _power, _power)
        car.set_light_bottom_color([0, 100, 0])
    elif gs_data == [0, 1, 1]:
        car.set_motor_power(_power, 0, _power, 0)
        car.set_light_off()
        car.set_light_bottom_left_color([50, 50, 0])
    elif gs_data == [0, 0, 1]:
        car.set_motor_power(_power, -_power, _power, -_power)
        car.set_light_off()
        car.set_light_bottom_left_color([100, 5, 0])
    elif gs_data == [1, 1, 0]:
        car.set_motor_power(0, _power, 0, _power)
        car.set_light_off()
        car.set_light_bottom_right_color([50, 50, 0])
    elif gs_data == [1, 0, 0]:
        car.set_motor_power(-_power, _power, -_power, _power)
        car.set_light_off()
        car.set_light_bottom_right_color([100, 0, 0])


def obstacle_avoid():
    print('obstacle_avoid')

      
def on_receive(data):
    global throttle_power, steer_power, move_status, last_move_status, mode 
    global led_status, brake_light_status, brake_light_time, brightness
    global left_trun_signal, right_trun_signal, hazard_lights
    ''' data to display'''
    # greyscale
    ws.send_dict['B'] = car.get_grayscale_values()
    # print(ws.send_dict['A'])
            
    # Speed measurement
    ws.send_dict['A'] = car.speed()
    # Speed mileage
    ws.send_dict['N'] = car.speed.mileage

    # # radar and distance
    ws.send_dict['D'] = [radar_angle, radar_distance]
    ws.send_dict['C'] = radar_distance

    ''' remote control'''
    # Move - power
    # if 'Q' in data.keys() and isinstance(data['Q'], int):
    #     throttle_power = data['Q']
    # if 'K' in data.keys() and isinstance(data['K'], int):
    #     steer_power = data['K']  

    if 'Q' in data.keys() and isinstance(data['Q'], int):
        throttle_power = data['Q']
    if 'K' in data.keys():
        steer_power = data['K'][0]

    # if 'K' in data.keys():
    #     steer_power = data['K'][0]  
    #     throttle_power = data['K'][1]  

    print('throttle_power: %s, steer_power: %s'%(throttle_power, steer_power))

    if 'E' in data.keys():
        left_trun_signal = data['E']
    if 'F' in data.keys():
        right_trun_signal = data['F'] 
    if 'G' in data.keys():
        hazard_lights = data['G'] 

    # Line Track or Obstacle Avoid
    if 'I' in data.keys() and data['I'] == True:
        mode = 'line track'
    elif 'J' in data.keys() and data['J'] == True:
        mode = 'obstacle avoid'
    else:
        mode = None

    # RGB LEDs
    if 'M' in data.keys():
        led_status = data['M']

    if led_status and 'L' in data.keys() and isinstance(data['L'], int):
        brightness = data['L']


def singal_lights_handler():
    global singal_time_count, singal_on_flag
    _light_nums = [0, 1, 6, 7]

    if hazard_lights:
        _light_on_nums = [0, 1, 6, 7]
    elif left_trun_signal:
        _light_on_nums = [6, 7]
    elif right_trun_signal:
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
     

def my_car_move(throttle_power, steer_power):
    power_l = 0
    power_r = 0
    if steer_power < 0:
        if throttle_power < 0:
            power_l = throttle_power + steer_power*2
        else:
            power_l = throttle_power - steer_power*2
        power_r = throttle_power
    else:
        power_l = throttle_power 
        if throttle_power < 0:
            power_r = throttle_power + steer_power*2
        else:
            power_r = throttle_power - steer_power*2      
    car.set_motor_power_gradually(power_l, power_r, power_r, power_l)

def remote_handler():
    global led_status, throttle_power, steer_power, move_status, last_move_status, brake_light_status, brake_light_time
    global radar_angle, radar_distance 
    
    ''' radar and distance '''
    # st = time.ticks_ms()
    radar_angle, radar_distance = car.get_radar_distance()
    # print('radar_ut: ', time.ticks_ms()-st)

    ''' Move '''
    # print('throttle_power: %s, steer_power: %s'%(throttle_power, steer_power))
    # st = time.ticks_ms()
    if throttle_power == 0 and steer_power == 0:
        move_status = 'stop'
    else:
        # if steer_power < 0:
        #     car.move('left', -steer_power)
        # elif steer_power > 0:
        #     car.move('right', steer_power)
        # elif throttle_power != 0:
        #     car.move('forward', throttle_power)
        # move_status = 'move'

        my_car_move(throttle_power, steer_power)
        move_status = 'move'
    # print('move_ut: ', time.ticks_ms()-st)

    ''' Line Track or Obstacle Avoid '''
    st = time.ticks_ms()
    if move_status == 'stop':
        if mode == 'line track':
            line_track()
        elif mode == 'obstacle avoid':
            obstacle_avoid()
        else:
            car.move('stop', 0)

    # print('mode_ut: ', time.ticks_ms()-st)

    st = time.ticks_ms()
    # Bottom Lights
    if led_status:
        car.set_light_bottom_color([brightness, brightness, brightness])
    else:
        car.set_light_bottom_color([0, 0, 0])   

    # Singal lights
    singal_lights_handler()
        
    # Brake lights
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
    
    # print('rgb_ut: ', time.ticks_ms()-st)


def main():
    car.servo.set_angle(0)
    ws.on_receive = on_receive
    if ws.start():
        while True:
            st = time.ticks_ms()
            ws.loop()
            # print('ws_ut: ', time.ticks_ms()-st)
            st = time.ticks_ms()
            remote_handler()    
            # print('rh_ut: ', time.ticks_ms()-st)


if __name__ == "__main__":
    try:
        onboard_led.on()
        main()
    finally:
        car.move("stop")
        car.set_light_off()
        onboard_led.off()

