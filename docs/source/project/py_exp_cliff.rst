.. _py_cliff:

1. Don’t Push Me
======================



To prevent Pico 4WD car from running off a cliff, let's give it a little sense of self-preservation.

In this project, the car will be dormant, and if you push it over the edge of a cliff, it will be awakened, then back up and shake its head in displeasure.


.. note::

    * The complete script ``project_1_cliff.py`` is in the path ``pico_4wd_car\examples\funny_projects``.

    * In order to allow the car to move on the ground without the USB cable connected, you need to save this script as ``main.py`` to Raspberry Pi Pico, see :ref:`run_script_offline` for a tutorial.


Below are the steps to implement the cliff function, and you can copy them into Thonny to run them.



**1. Import libraries**

#. In this project, we use grayscale module, motor and servo, so we import the related libraries here.

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
                print(gs.get_value())
                time.sleep(0.05)
        finally:
            pass

    * Note that this command ``gs.set_edge_reference(1000)`` is the cliff threshold set according to my current environment, what you actually use may be different.
    
    * Run the script after copying it into Thonny and then hang the car in the air (10cm or more).

        .. image:: img/grayscale_cliff.png
            :width: 500
            :align: center

    * Finallly, fill in a value in ``gs.set_edge_reference()`` according to the result in the Shell.

**2. Back up when detected**

    When the grayscale module detects a cliff, go backward; otherwise, stop in place.

    .. code-block:: python
        :emphasize-lines: 20,21,22,23

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


        def main():
            while True:
        #         print(gs.get_value())
                if gs.is_on_edge():
                    car.move("backward", MOTOR_POWER)
                else:
                    car.move("stop")

        try:
            main()
        finally:
            car.move("stop")
            time.sleep(0.05)


**3. Shaking head while backing up**

    To make the car more cute, let it shake its head while backing up.

    .. code-block:: python
        :emphasize-lines: 16,17,18,19,20,21,22,23,24,25,32

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

        def main():
            while True:
                # print(gs.get_value())
                if gs.is_on_edge():
                    car.move("backward", MOTOR_POWER)
                    shake_head()
                    shake_head()
                else:
                    car.move("stop")

        try:
            main()
        finally:
            car.move("stop")
            time.sleep(0.05)
    
