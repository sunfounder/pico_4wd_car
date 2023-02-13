# pico_4wd_car_lessons

- motor
    - singal_motor_move.py 单个电机的控制
        - 一个电机使用到了两个 PWM 引脚
            - pin1 = x, pin2 = 0xffff , 正转
            - pin1 = 0xffff, pin2 = x , 反转
            - pin1 = 0xffff, pin2 = 0xffff, 停止
        - power映射到PWM值，和方向值

    - motor_class.py 为了方便控制多个电机，将电机做成一个类
        - 写成类
        - 调用类同时控制1个电机

    - motors_control.py 同时控制4个电机的函数
        - set_motors_power(0, 0, 0, 0)
        - 速度缓慢递增
            set_motor_power_gradually
        - 前进，后退 左 右
            - 简化的移动函数
                - move("forward", power)

- ws2812
    - ws2812_conrol.py 

    - ws2812_class.py 写成类

    - pico_4wd_lights.py

    - car_move_rgb.py 
        让小车移动，并在移动时有灯效显示前进：尾灯中间亮绿色，后退：尾灯中间亮红色，左右转：尾灯两侧亮黄色


- servo
    - servo_control.py 舵机的控制
        - pwm 初始化， 频率对应的角度

    - servo_class.py 做成类
        - 写成类
        - 调用类控制舵机