2. Line Track
===================

.. image:: img/example_line.png

Let Pico-4wd walk on its exclusive avenue! Tape a line on a light-colored ground (or table) with black insulating tape. Run this script and you will see Pico-4wd track the line to forward.



完整代码请看 ``examples`` 目录下的 ``project_2_line_track.py`` 文件。


**How to do?**


1. 在浅色的桌面或者地面用黑色电工胶带贴出一条线。

【方便的话配个图】

.. warning::
    When pasting this line, there should be no sharp turns so that the car does not drive off the path.


2. 在这个项目中，我们用到了 grayscale module ， motor， 和 rgb board 。这意味着我们需要使用 ``grayscale.py``, ``motors.py``, ``motor.py``, ``light.py``, ``lights.py`` 这几个库，请将它们从 ``libs`` 文件夹中上传到pico。 然后在项目中import它们


    .. .. note:: 虽然你可能在 module 篇章中，自己从零构建过这些库。它们自然是能用的，但是个中细节或有出入，建议以 ``libs`` 目录下的文件为准。

    .. 【导入库的图】

    .. .. note:: 如果你不知道怎么使用thonny IDE，请看 :ref:`XXX`

    .. code-block:: python

        from grayscale import Grayscale
        import motors as car
        import lights

        gs = Grayscale(26, 27, 28)
        gs.set_line_reference(10000)

        MOTOR_POWER = 30

3. 设置 grayscale module 的测线阈值（如有疑惑请参考 :ref:`py_grayscale` ）. 然后，根据 grayscale module 的检测结果，让小车往不同的方向行驶。

    .. code-block:: python

        from grayscale import Grayscale
        import motors as car
        import lights

        gs = Grayscale(26, 27, 28)
        gs.set_line_reference(10000)

        MOTOR_POWER = 30

        def line_track():
            while True:
                gs_data = gs.get_line_status()
                if gs_data == [0, 1, 0]:
                    car.set_motors_power([MOTOR_POWER, MOTOR_POWER, MOTOR_POWER, MOTOR_POWER])
                elif gs_data == [0, 1, 1]:
                    car.set_motors_power([MOTOR_POWER, 0, MOTOR_POWER, 0])
                elif gs_data == [0, 0, 1]:
                    car.set_motors_power([MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER])
                elif gs_data == [1, 1, 0]:
                    car.set_motors_power([0, MOTOR_POWER, 0, MOTOR_POWER])
                elif gs_data == [1, 0, 0]:
                    car.set_motors_power([-MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER])

        try:
            line_track()
        finally:
            car.move("stop")

4. 最后在行驶时加点灯光特效，让它看起来更有趣一些。

    .. code-block:: python

        from grayscale import Grayscale
        import motors as car
        import lights

        gs = Grayscale(26, 27, 28)
        gs.set_line_reference(10000)

        MOTOR_POWER = 30

        def line_track():
            while True:
                gs_data = gs.get_line_status()
                if gs_data == [0, 1, 0]:
                    car.set_motors_power([MOTOR_POWER, MOTOR_POWER, MOTOR_POWER, MOTOR_POWER])
                    lights.set_bottom_color([0, 100, 0])
                elif gs_data == [0, 1, 1]:
                    car.set_motors_power([MOTOR_POWER, 0, MOTOR_POWER, 0])
                    lights.set_off()
                    lights.set_bottom_left_color([50, 50, 0])
                elif gs_data == [0, 0, 1]:
                    car.set_motors_power([MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER])
                    lights.set_off()
                    lights.set_bottom_left_color([100, 5, 0])
                elif gs_data == [1, 1, 0]:
                    car.set_motors_power([0, MOTOR_POWER, 0, MOTOR_POWER])
                    lights.set_off()
                    lights.set_bottom_right_color([50, 50, 0])
                elif gs_data == [1, 0, 0]:
                    car.set_motors_power([-MOTOR_POWER, MOTOR_POWER, -MOTOR_POWER, MOTOR_POWER])
                    lights.set_off()
                    lights.set_bottom_right_color([100, 0, 0])

        try:
            line_track()
        finally:
            car.move("stop")
            lights.set_off()

