5. Light with Movement
=============================

我们可以让小车在转弯的时候亮起黄灯，在后退时亮出红灯，前进时亮出绿灯。
即便在避障或者跟随的时候，也添加这样的灯效。

实现这样的效果无需在源代码中进行复杂的改动，只需添加一个嵌套的库。

完整代码请看 ``examples`` 目录下的 ``project_5_light.py`` 文件。

**How to do?**

1. 在一个新文件中import ``motors.py`` 和 ``lights.py`` . 并且创建一个 ``move(action,power=0)`` 函数，它的函数名和参数和 ``motors.py`` 中的一致。在这个函数中，调用原来的 ``move`` 函数，并添加点亮rgb board的代码。

    .. code-block:: python

        import motors as car
        import lights
        import time

        def move(action,power=0):
            car.move(action,power)
            if action is "forward":
                lights.set_off()
                lights.set_bottom_color(0x00aa00)
                lights.set_rear_middle_color(0x00aa00)
            elif action is "left":
                lights.set_off()
                lights.set_rear_left_color(0xaaaa00)
                lights.set_bottom_left_color(0xaaaa00)
            elif action is "right":
                lights.set_off()
                lights.set_rear_right_color(0xaaaa00)
                lights.set_bottom_right_color(0xaaaa00)    
            elif action is "backward":
                lights.set_off()
                lights.set_rear_middle_color(0xaa0000)
                lights.set_bottom_color(0xaa0000) 
            else:
                lights.set_off()

2. 将这个新文件（我们在 ``examples`` 路径下创建了这个文件，名为 ``project_5_light.py``）上传到pico。

    【插个图呗】

3. 在 ``project_1_cliff.py`` ， ``project_3_follow.py`` ， ``project_4_avoid.py`` 中任意项目中，修改导入的头文件。

    .. code-block:: python
        :emphasize-lines: 1,2

        import project_5_light as car
        # import motors as car
        from servo import Servo
        from grayscale import Grayscale
        import time

        # init grayscale module
        gs = Grayscale(26, 27, 28)
        gs.set_edge_reference(1000)

        # init servo
        servo = Servo(18)
        servo.set_angle(0)

        def shake_head():
            for angle in range(0, 90, 10):
                servo.set_angle(angle)
                time.sleep(0.01)
            for angle in range(90, -90, -10):
                servo.set_angle(angle)
                time.sleep(0.01)
            for angle in range(-90, 0, 10):
                servo.set_angle(angle)
                time.sleep(0.01)

        MOTOR_POWER = 50
        try:
            while True:
                if gs.is_on_edge():
                    car.move("backward", MOTOR_POWER)
                    shake_head()
                    shake_head()
                else:
                    car.move("stop")
        finally:
            car.move("stop")
            time.sleep(0.05)

4. 运行代码。现在你能看到，在保留原来示例的基础上，每次移动都附带了灯光特效。