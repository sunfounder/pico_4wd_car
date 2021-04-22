Don’t Push Me
================

让我们为Pico-4wd赋予一点“自我保护意识”，让它学会使用自己的grayscale module来避免冲下悬崖。

在这个示例中，小车会处于休眠状态。如果你把它推向悬崖，它会紧急唤醒，后退，并摇头表示不满。请打开 ``donot_push_me.py`` 使用这个示例。

程序流程
--------------

.. image:: img/flowchart_donot_push_me.png


代码
----------------

.. code-block:: python

    import pico_4wd as car
    import time

    car.GRAYSCALE_EDGE_REFERENCE = 500
    MOTOR_POWER = 50

    def shake_head():
        for angle in range(0, 90, 10):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.01)
        for angle in range(90, -90, -10):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.01)
        for angle in range(-90, 0, 10):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.01)

    def main():
        while True:
            if car.is_greyscale_on_edge():
                car.move("backward", MOTOR_POWER)
                car.set_light_all_color([100, 0, 0])
                shake_head()
                shake_head()
            else:
                car.move("stop", MOTOR_POWER)
                car.set_light_off()

    try:
        main()
    finally:
        car.move("stop")
        car.set_light_off()