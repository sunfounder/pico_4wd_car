# `pico_4wd`

Module for pico 4wd car

## Methods

### LED Strip

`set_light_all_color(color)`: Set all LED color

- `color`: list of [R, G, B]
- return: None

```python
set_light_all_color([100, 0, 0]) # set all LED color to red
set_light_all_color([0, 100, 0]) # set all LED color to green
set_light_all_color([0, 0, 100]) # set all LED color to blue
```

`set_light_color_at(num, color)`: Set single LED color

- `num`: int for the position of LED, from 0 to 23
- `color`: list of [R, G, B]
- return: None

```python
set_light_color_at(1, [100, 0, 0]) # set the first LED color to red

# set rear LED strip to green
for i in range(0, 8):
    set_light_all_color(i, [0, 100, 0])
# set bottom LED strip to red
for i in range(8, 24):
    set_light_all_color(i, [100, 0, 0])
```

`set_light_bottom_left_color(color)`: Set bottom left LED strip color

- `color`: list of [R, G, B]
- return: None

```python
set_light_bottom_left_color([100, 0, 0]) # set bottom left LED strip color to red
```

`set_light_bottom_right_color(color)`: Set bottom left LED strip color

- `color`: list of [R, G, B]
- return: None

```python
set_light_bottom_right_color([100, 0, 0]) # set bottom left LED strip color to red
```

`set_light_bottom_color(color)`:  Set both bottom LED strips color

- `color`: list of [R, G, B]
- return: None

```python
set_light_bottom_color([100, 0, 0]) # set bottom LED strip color to red
```

`set_light_rear_color(color)`:  Set rear LED strip color

- `color`: list of [R, G, B]
- return: None

```python
set_light_rear_color([100, 0, 0]) # set bottom LED strip color to red
```

`write_light_color_at(num, color)`: Write single LED color to buffer, but not excute

- `num`: int for the position of LED, from 0 to 23
- `color`: list of [R, G, B]
- return: None

```python
write_light_color_at(1, [100, 0, 0]) # set the first LED color to red

# set rear LED strip to green
for i in range(0, 8):
    write_light_color_at(i, [0, 100, 0])
light_excute()
# set bottom LED strip to red
for i in range(8, 24):
    write_light_color_at(i, [100, 0, 0])
light_excute()
```

`light_excute()`: Excute light from buffer

- return: None

```python
write_light_color_at(1, [100, 0, 0]) # set the first LED color to red
light_excute()

# set rear LED strip to green
for i in range(0, 8):
    write_light_color_at(i, [0, 100, 0])
light_excute()
# set bottom LED strip to red
for i in range(8, 24):
    write_light_color_at(i, [100, 0, 0])
light_excute()
```

`set_light_off()`: Turn all LED off

- return: None

```python
# All led blink red
set_light_all_color([100, 0, 0])
set_light_off()
set_light_all_color([100, 0, 0])
set_light_off()
```

`hue2rgb(_h, _s = 1, _b = 1)`: Convert HSB to RGB

- `_h`: hue value 0~360
- `_s`: saturation value 0.0~1.0
- `_b`: brightness value 0.0~1.0
- return: `[r, g, b]`

```python
# All led to red
rgb = hue2rgb(0, 1, 1)
set_light_all_color(rgb)
# All led to green
rgb = hue2rgb(120, 1, 1)
set_light_all_color(rgb)
# All led to blue
rgb = hue2rgb(240, 1, 1)
set_light_all_color(rgb)
```

### Grayscale sensor

`get_grayscale_values()`: Get grayscale values

- return [left, middle, right], each 0~65535

```python
print(get_grayscale_values())
```

def is_greyscale_on_edge():
    ref = GRAYSCALE_EDGE_REFERENCE
    gs_list = get_grayscale_values()
    return gs_list[2] <= ref or gs_list[1] <= ref or gs_list[0] <= ref

def get_greyscale_status():
    ref = GRAYSCALE_LINE_REFERENCE
    return [int(value < ref) for value in get_grayscale_values()]

# Radar
def get_radar_distance_at(angle):
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = sonar.get_distance()
    return distance

def get_radar_distance():
    global radar_angle, radar_step
    radar_angle += radar_step
    if radar_angle >= RADAR_MAX_ANGLE:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -RADAR_STEP_ANGLE
    elif radar_angle <= RADAR_MIN_ANGLE:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = RADAR_STEP_ANGLE
    distance = get_radar_distance_at(radar_angle)
    return [radar_angle, distance]

def set_radar_scan_angle(angle):
    global RADAR_MAX_ANGLE, RADAR_MIN_ANGLE, radar_angle, radar_step, radar_scan_angle
    if radar_scan_angle == angle:
        return
    radar_scan_angle = angle
    RADAR_MAX_ANGLE = int(angle / 2)
    RADAR_MIN_ANGLE = -RADAR_MAX_ANGLE
    if radar_step < 0:
        radar_angle = RADAR_MIN_ANGLE
        radar_step = RADAR_STEP_ANGLE
    else:
        radar_angle = RADAR_MAX_ANGLE
        radar_step = -RADAR_STEP_ANGLE
    servo.set_angle(radar_angle)

def get_radar_status(distance):
    if distance > RADAR_REFERENCE:
        return 1
    else:
        return 0

def radar_scan():
    global radar_data
    angle, distance = get_radar_distance()
    status = get_radar_status(distance)

    radar_data.append(status)
    if angle == RADAR_MIN_ANGLE or angle == RADAR_MAX_ANGLE:
        if radar_step < 0:
            # print("reverse")
            radar_data.reverse()
        # print(radar_data)
        tmp = radar_data.copy()
        radar_data = []
        return tmp
    else:
        return status

# slowly increase power of the motor, to avoid hight reverse voltage from motors
def set_motor_power_gradually(*powers):
    flags = [True, True, True, True]
    while flags[0] or flags[1] or flags[2] or flags[3]:
        for i, motor in enumerate(motors):
            # print(motor.power, powers[i])
            if motor.power > powers[i]:
                motor.power -= 1
            elif motor.power < powers[i]:
                motor.power += 1
            else:
                flags[i] = False
        time.sleep_ms(1)

# set power 
def set_motor_power(*powers):
    for i, motor in enumerate(motors):
        motor.power = powers[i]

def stop():
    set_motor_power(0, 0, 0, 0)

def move(dir, power=0):
    if dir == "forward":
        set_motor_power_gradually(power, power, power, power)
    elif dir == "backward":
        set_motor_power_gradually(-power, -power, -power, -power)
    elif dir == "left":
        set_motor_power_gradually(-power, power, -power, power)
    elif dir == "right":
        set_motor_power_gradually(power, -power, power, -power)
    else:
        set_motor_power_gradually(0, 0, 0, 0)


# Atrtribute
left_front  = Motor(17, 16, dir=-1) # motor 1
right_front = Motor(15, 14, dir=1) # motor 2
left_rear   = Motor(13, 12, dir=-1) # motor 3
right_rear  = Motor(11, 10, dir=1) # motor 4
motors = [left_front, right_front, left_rear, right_rear]

servo = Servo(18)
speed = Speed(8, 9)

np =  WS2812(Pin(19, Pin.OUT), 24)

gs0 = ADC(Pin(26))
gs1 = ADC(Pin(27))
gs2 = ADC(Pin(28))
GRAYSCALE_EDGE_REFERENCE = 20
GRAYSCALE_LINE_REFERENCE = 10000

# Ultrasonic
sonar = Ultrasonic(6, 7)
radar_data = []
RADAR_REFERENCE = 20
RADAR_MAX_ANGLE = 90
RADAR_MIN_ANGLE = -90
RADAR_STEP_ANGLE = 10
radar_step = -RADAR_STEP_ANGLE
radar_angle = 0
radar_scan_angle = 180
