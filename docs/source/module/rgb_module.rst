.. _py_ws2812_class:

3. ``ws2812.py`` Module
===================================
In order to be able to make the RGB Board light up different colors and display different effects in a complex project, we need to encapsulate the previous project into a (module)library.

.. note::

    The encapsulated library ``ws2812.py`` has been saved in ``pico_4wd_car-v2.0\libs``, which may differ from the ones shown in the course, so please refer to the file under ``libs`` path when using it.


**Hex Format**

    Next, let's look at the simple encapsulated code.

    .. code-block:: python


        from machine import Pin
        from rp2 import PIO, StateMachine, asm_pio
        import array
        import time

        @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
        def ws2812():
            T1 = 2
            T2 = 5
            T3 = 3
            label("bitloop")
            out(x, 1).side(0)[T3 - 1]
            jmp(not_x, "do_zero").side(1)[T1 - 1]
            jmp("bitloop").side(1)[T2 - 1]
            label("do_zero")
            nop().side(0)[T2 - 1]

        class WS2812():
            
            def __init__(self, pin, num):
                # Configure the number of WS2812 LEDs.
                self.led_nums = num
                self.pin = pin
                self.sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(self.pin))
                # Start the StateMachine, it will wait for data on its FIFO.
                self.sm.active(1)
                
                self.buf = array.array("I", [0 for _ in range(self.led_nums)])

            def write(self):
                self.sm.put(self.buf, 8)   

            def __getitem__(self, i):
                return self.buf[i]

            def __setitem__(self, i, value):
                self.buf[i] = value


        # Display a pattern on the LEDs via a color value.
        LIGHT_PIN = 19
        LIGHT_NUM = 24
        np = WS2812(LIGHT_PIN, LIGHT_NUM)

        for i in range(LIGHT_NUM):
            np[i] = 0x00aaff
        np.write()

    Now you can copy this code into Thonny and then click the |thonny_run| button or press ``F5`` to run it. When you power up the Pico 4WD car, you will see 3 RGB boards lit up in magenta color.


**RGB Format**

    Additionally to hexadecimal, people often prefer RGB color representations. 
    Therefore, we perform a little optimization, converting colors from HEX to RGB.

    Focus on the highlighted functions to see how the hexadecimal format is converted to RGB format.


    .. code-block:: python
        :emphasize-lines: 33,42,54,57

        from machine import Pin
        from rp2 import PIO, StateMachine, asm_pio
        import array
        import time

        @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
        def ws2812():
            T1 = 2
            T2 = 5
            T3 = 3
            label("bitloop")
            out(x, 1).side(0)[T3 - 1]
            jmp(not_x, "do_zero").side(1)[T1 - 1]
            jmp("bitloop").side(1)[T2 - 1]
            label("do_zero")
            nop().side(0)[T2 - 1]

        class WS2812():
            
            def __init__(self, pin, num):
                # Configure the number of WS2812 LEDs.
                self.led_nums = num
                self.pin = pin
                self.sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(self.pin))
                # Start the StateMachine, it will wait for data on its FIFO.
                self.sm.active(1)
                
                self.buf = array.array("I", [0 for _ in range(self.led_nums)])

            def write(self):
                self.sm.put(self.buf, 8)   

            def list_to_hex(self, color):
                if isinstance(color, list) and len(color) == 3:
                    return (color[0] << 8) + (color[1] << 16) + (color[2])
                elif isinstance(color, int):
                    value = (color & 0xFF0000)>>8 | (color & 0x00FF00)<<8 | (color & 0x0000FF)
                    return value
                else:
                    raise ValueError("Color must be 24-bit RGB hex or list of 3 8-bit RGB, not %s"%color)

            def hex_to_list(self, color):
                if isinstance(color, list) and len(color) == 3:
                    return color
                elif isinstance(color, int):
                    r = color >> 8 & 0xFF
                    g = color >> 16 & 0xFF
                    b = color >> 0 & 0xFF
                    return [r, g, b]
                else:
                    raise ValueError("Color must be 24-bit RGB hex or list of 3 8-bit RGB, not %s"%color)

            def __getitem__(self, i):
                return self.hex_to_list(self.buf[i])

            def __setitem__(self, i, value):
                self.buf[i] = self.list_to_hex(value)

        # Display a pattern on the LEDs via an array of LED RGB values.
        LIGHT_PIN = 19
        LIGHT_NUM = 24
        np = WS2812(LIGHT_PIN, LIGHT_NUM)
        
        for i in range(LIGHT_NUM):
            np[i] = [0,255,110]
        np.write()
        time.sleep(1)
        
        for i in range(LIGHT_NUM):
            np[i] = 0xFF00AA
        np.write()

    As you can see at the bottom of the code, we use both RGB and hexadecimal colors, ``[0,255,110]`` and ``0xFF00AA``. You can choose one according to your preference.

    You can also copy it into Thonny and run it to see what effect it has.
