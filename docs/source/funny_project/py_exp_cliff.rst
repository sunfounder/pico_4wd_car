1. Don’t Push Me
======================

.. image:: img/example_cliff.png

Let us give Pico-4wd a little **self-protection awareness** and let it learn to use its own grayscale module to avoid rushing down the cliff.

In this example, the car will be dormant. If you push it to a cliff, it will be awakened urgently, then back up, and shake its head to express dissatisfaction.


完整代码请看 ``examples`` 目录下的 ``project_1_cliff.py`` 文件。


**How to do?**


1. 在这个项目中，我们用到了 grayscale module ， motor， 和 servo。这意味着我们需要使用 ``grayscale.py``, ``motors.py``, ``motor.py``, ``servo.py`` 这几个库，请将它们从 ``libs`` 文件夹中上传到pico。 然后在项目中import它们

    .. note:: 虽然你可能在 module 篇章中，自己从零构建过这些库。它们自然是能用的，但是个中细节或有出入，建议以 ``libs`` 目录下的文件为准。

    【导入库的图】

    .. note:: 如果你不知道怎么使用thonny IDE，请看 :ref:`XXX`

    .. code-block:: python

        import motors as car
        from servo import Servo
        from grayscale import Grayscale
        import time

        # init grayscale module
        gs = Grayscale(26, 27, 28)
        gs.set_edge_reference(1000)

        # init servo
        servo = Servo(18)
        servo.set_angle(0)   

2. 编写功能：当 grayscale module 检测到悬崖，退后；否则，原地静止。

    .. code-block:: python

        import motors as car
        from servo import Servo
        from grayscale import Grayscale
        import time

        # init grayscale module
        gs = Grayscale(26, 27, 28)
        gs.set_edge_reference(1000)

        # init servo
        servo = Servo(18)
        servo.set_angle(0)

        MOTOR_POWER = 50
        try:
            while True:
                if gs.is_on_edge():
                    car.move("backward", MOTOR_POWER)
                else:
                    car.move("stop")
        finally:
            car.move("stop")
            time.sleep(0.05)   


3. 让小车变得可爱，后退的时候会摇头。

    .. code-block:: python

        import motors as car
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