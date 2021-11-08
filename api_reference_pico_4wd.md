# `pico_4wd`

Module for pico 4wd car

## Methods

### LED Strip

`set_light_all_color(color)`: Set all LED color

- `color`: list of [R, G, B], R/G/B range 0~255
- return: None

```python
import pico_4wd as car

car.set_light_all_color([100, 0, 0]) # set all LED color to red
car.set_light_all_color([0, 100, 0]) # set all LED color to green
car.set_light_all_color([0, 0, 100]) # set all LED color to blue
```

`set_light_color_at(num, color, preset=0)`: Set single LED color

- `num`: int for the position of LED, from 0 to 23
- `color`: list of [R, G, B], R/G/B range 0~255
- `preset`: set LIGHT_REAR/LIGHT_BOTTOM_LEFT/LIGHT_BOTTOM_RIGHT
- return: None

```python
import pico_4wd as car

car.set_light_color_at(1, [100, 0, 0]) # set the first LED color to red

# set rear LED strip to green
for i in range(0, 8):
    car.set_light_all_color(i, [0, 100, 0])
# set bottom LED strip to red
for i in range(8, 24):
    car.set_light_all_color(i, [100, 0, 0])
```

`set_light_bottom_left_color(color)`: Set bottom left LED strip color

- `color`: list of [R, G, B], R/G/B range 0~255
- return: None

```python
import pico_4wd as car

car.set_light_bottom_left_color([100, 0, 0]) # set bottom left LED strip color to red
```

`set_light_bottom_right_color(color)`: Set bottom left LED strip color

- `color`: list of [R, G, B], R/G/B range 0~255
- return: None

```python
import pico_4wd as car

car.set_light_bottom_right_color([100, 0, 0]) # set bottom left LED strip color to red
```

`set_light_bottom_color(color)`:  Set both bottom LED strips color

- `color`: list of [R, G, B], R/G/B range 0~255
- return: None

```python
import pico_4wd as car

car.set_light_bottom_color([100, 0, 0]) # set bottom LED strip color to red
```

`set_light_rear_color(color)`:  Set rear LED strip color

- `color`: list of [R, G, B], R/G/B range 0~255
- return: None

```python
import pico_4wd as car

car.set_light_rear_color([100, 0, 0]) # set bottom LED strip color to red
```

`write_light_color_at(num, color, preset=0)`: Write single LED color to buffer, but not excute

- `num`: int for the position of LED, from 0 to 23
- `color`: list of [R, G, B], R/G/B range 0~255
- `preset`: set LIGHT_REAR/LIGHT_BOTTOM_LEFT/LIGHT_BOTTOM_RIGHT
- return: None

```python
import pico_4wd as car

car.write_light_color_at(1, [100, 0, 0]) # set the first LED color to red

# set rear LED strip to green
for i in range(0, 8):
    car.write_light_color_at(i, [0, 100, 0])
car.light_excute()
# set bottom LED strip to red
for i in range(8, 24):
    car.write_light_color_at(i, [100, 0, 0])
car.light_excute()
```

`light_excute()`: Excute light from buffer

- return: None

```python
import pico_4wd as car

car.write_light_color_at(1, [100, 0, 0]) # set the first LED color to red
car.light_excute()

# set rear LED strip to green
for i in range(0, 8):
    car.write_light_color_at(i, [0, 100, 0])
car.light_excute()
# set bottom LED strip to red
for i in range(8, 24):
    car.write_light_color_at(i, [100, 0, 0])
car.light_excute()
```

`set_light_off()`: Turn all LED off

- return: None

```python
import pico_4wd as car
import time

# All led blink red
while True:
    car.set_light_all_color([100, 0, 0])
    car.set_light_off()
    car.set_light_all_color([100, 0, 0])
    car.set_light_off()
    time.sleep(1)
```

`hue2rgb(_h, _s = 1, _b = 1)`: Convert HSB to RGB

- `_h`: hue value 0~360
- `_s`: saturation value 0.0~1.0
- `_b`: brightness value 0.0~1.0
- return: `[r, g, b]`

```python
import pico_4wd as car

# All led to red
rgb = car.hue2rgb(0, 1, 1)
car.set_light_all_color(rgb)
# All led to green
rgb = car.hue2rgb(120, 1, 1)
car.set_light_all_color(rgb)
# All led to blue
rgb = car.hue2rgb(240, 1, 1)
car.set_light_all_color(rgb)
```

### Grayscale sensor

`get_grayscale_values()`: Get grayscale values

- return: [left, middle, right], each 0~65535

```python
import pico_4wd as car
import time

while True:
    print(car.get_grayscale_values())
    time.sleep(1)
```

`is_greyscale_on_edge()`: Check if the car is on edge according to `GRAYSCALE_EDGE_REFERENCE`

- return: True/False

```python
import pico_4wd as car
import time

while True:
    print(car.is_greyscale_on_edge())
    time.sleep(1)
```

`get_greyscale_status()`: Get Grayscale status according to `GRAYSCALE_LINE_REFERENCE`

- return: [status, status, status] status = 1/0 as line/not

```python
import pico_4wd as car
import time

while True:
    print(car.get_greyscale_status())
    time.sleep(1)
```

### Radar

`get_radar_distance_at(angle)`: Turn the servo of radar at the angle and return distance

- `angle`: -90~90
- return: distance unit cm

```python
import pico_4wd as car
import time

while True:
    print("distance: %scm"%car.get_radar_distance_at(0))
    time.sleep(1)
```

`get_radar_distance()`:  Turn the servo of radar by step at every call of this method, and return distance

- return: distance unit cm

```python
import pico_4wd as car
import time

while True:
    angle, distance = car.get_radar_distance()
    print("angle: %s, distance: %scm"%(angle, distance)
    time.sleep(0.5)
```

`set_radar_scan_angle(angle)`: Set radar scan angle, 180 for a full scan, 90 for  only scan ahead

- `angle`: 0~180
- return: None

```python
import pico_4wd as car

car.set_radar_scan_angle(90)
while True:
    angle, distance = car.get_radar_distance()
    print("angle: %s, distance: %scm"%(angle, distance)
    time.sleep(0.5)
```

`get_radar_status(distance)`: Convert distance to status base on `RADAR_REFERENCE`

- `distance`: distance normally get from sonar reads
- return: 0/1 0 in under reference, 1 is over

```python
import pico_4wd as car
import time

while True:
    distance = car.get_radar_distance_at(0)
    print("Radar status at 90: %s" % car.get_radar_status(distance))
    time.sleep(1)
```

`radar_scan()`: radar scan to get a list of status when scan finished or current angle status if not.

- return: list of status or current status, 0 in under reference, 1 is over

```python
import pico_4wd as car
import time

while True:
    status = radar_scan
    if isinstance(status, int):
        print("Scanning, current status: %s" % status)
    else:
        print("Scan finished, status: %s" % status)
    time.sleep(1)
```

`set_motor_power_gradually(*powers)`: slowly increase power of the motor, to avoid hight reverse voltage from motors. but this will slows the motor react, not suit for high reaction application like avoid obstacle and line tracking

- `powers`: powers for left front motor, right front motor, left rear motor, right rear motor
- return: None

```python
import pico_4wd as car
import time

# all motors from 100 to -100, then -100 to 100, but gradually
while True:
    car.set_motor_power_gradually(100, 100, 100, 100)
    time.sleep(1)
    car.set_motor_power_gradually(-100, -100, -100, -100)
    time.sleep(1)
```

# set power 
`set_motor_power(*powers)`: Set all motor powers immediatlly, carefully use this method.

- `powers`: powers for left front motor, right front motor, left rear motor, right rear motor
- return: None

```python
import pico_4wd as car
import time

# all motors from 30 to -30, then -30 to 30, DONOT try from 100 to -100 or -100 to 100.
while True:
    car.set_motor_power(30, 30, 30, 30)
    time.sleep(1)
    car.set_motor_power(-30, -30, -30, -30)
    time.sleep(1)
```

`stop()`: Stop all motors

- return: None

```python
import pico_4wd as car
import time

def main():
    # all motors from 30 to -30, then -30 to 30, DONOT try from 100 to -100 or -100 to 100.
    car.set_motor_power(30, 30, 30, 30)
    time.sleep(3)

# Add stop to finally to stop the car when you code finished or after you terminate it
try:
    main()
finally:
    car.stop()
```

`move(dir, power=0)`: Move the Car with simple strings

- dir: `"forward"`/`"backward"`/`"left"`/`"right"`
- power: 0~100
- return: None

```python
import pico_4wd as car
import time

def main():
    # all motors from 30 to -30, then -30 to 30, DONOT try from 100 to -100 or -100 to 100.
    car.move("forward", 50)
    time.sleep(1)
    car.move("backward", 50)
    time.sleep(1)
    car.move("left", 50)
    time.sleep(1)
    car.move("right", 50)
    time.sleep(1)

# Add stop to finally to stop the car when you code finished or after you terminate it
try:
    main()
finally:
    car.stop()
```

## Atrtribute

- `GRAYSCALE_EDGE_REFERENCE`: Reference for detecting edged
- `GRAYSCALE_LINE_REFERENCE`: Reference for detecting Line
- `RADAR_REFERENCE`: Reference for detecting obstables
- `RADAR_MAX_ANGLE`: Max angle for radar scanning
- `RADAR_MIN_ANGLE`: Min angle for radar scanning
- `RADAR_STEP_ANGLE`: Angle of every step for radar scanning
- `LIGHT_REAR`: Rear light order (0/1/2)
- `LIGHT_BOTTOM_LEFT`: Bottom left light order (0/1/2)
- `LIGHT_BOTTOM_RIGHT`: Bottom right light order (0/1/2)
