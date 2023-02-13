# pico-4wd函数封装说明

## 最底层库 pico_rdp.py
    各种模块的最简单的读值或控制

- class Speed(): 测速模块的类
    - __init__ ： 初始化引脚，定时器，IO中断
    - on_left： 左测速IO中断，计数
    - on_right： 右测速IO中断，计数
    - on_timer： 定时器中断
        - 没200ms中断一次， 根据on_left 和 on_right 的计数算出速度，根据速度累计里程
    - __call__：返回速度值
    - get_speed：返回速度值
    - mileage：返回里程值
    - mileage(value): 重置里程值为value
        - 可以从文件中读取里程值，设定初始的里程

- class Servo():
    - __init__：引脚，初始化PWM
    - set_angle(angle): 更具angle，转换成PWM值输出，从而控制舵机
    - 补充舵机的PWM脉宽与角度的关系

- class Ultrasonic()
    - __init__：初始化引脚
    - _pulse：发送读值的时序
    - get_distance：更具IO返回上拉的时间计算距离,注意时间是发送到返回的距离，实际距离需要 除以 2

- Motor()： 
    