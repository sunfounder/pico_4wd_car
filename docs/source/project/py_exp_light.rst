.. _py_light:

5. Light with Movement
=============================

We can make the car light up yellow when turning, red when going backwards and green when going forward.

Also such lighting effects can be added to other projects such as :ref:`py_cliff`, :ref:`py_follow` and :ref:`py_avoid`.
It's easy to add, just import this light effect script to other projects as a library, no need to make complicated changes in the source code.

**1. Realize interesting light effects** (``project_5_light.py``)

    The following is the light effect code for the movement of the car.

    * When the car moves forward, the bottom RGB board and the middle 4 LEDs on the tail are lit in green, and backward is red.
    * When turning left or right, the bottom RGB board and the left or right two LEDs on the tail are lit in yellow.

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

        if __name__ == "__main__":
            try:
                while True:
                    speed = 50
                    act_list = [
                        "forward",
                        "backward",
                        "left",
                        "right",
                        "stop",
                    ]
                    for act in act_list:
                        print(act)
                        move(act, speed)
                        time.sleep(1)
            finally:
                move("stop")
                lights.set_off()
                time.sleep(0.05)


**2. Upload to Raspberry Pico**

    In order to apply the above lighting effect to other projects, you need to save it to the Raspberry Pi Pico by following these steps.

    #. Copy the above code into Thonny or open the ``project_5_light.py`` under the path of ``pico_4wd_car-v2.0\examples\funny_projects``.
    #. Then click **File** -> **Save As**.

        .. image:: img/save_as.png

    #. Select **Raspberry Pi Pico** in the pop-up window that appears.

        .. image:: img/save_to_pico.png

    #. Set the file name to ``project_5_light.py``. Of course you can also use another name (except ``main.py`` and ``boot.py``), fill it in and then click **OK** to confirm.

**3. Import in other Projects**

    If you want to use this light effect in any of the :ref:`py_cliff`, :ref:`py_follow` and :ref:`py_avoid` projects, all you need to do is import the library you just saved and comment out the original ``motors`` library.

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

        ...
