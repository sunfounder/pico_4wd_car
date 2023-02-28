2. Light up
========================

The RGB Board is a component that does not communicate in SPI or I2C, and it needs to handle things at a much lower level.

Pico has a solution for this: |link_pio|.

As well as the two main Cortex-M0+ processing cores, there are two PIO blocks that each have four state machines. These are really stripped-down processing cores that can be used to handle data coming in or out of the microcontroller, and offload some of the processing requirement for implementing communications protocols.

You can't program these cores with MicroPython - you have to use a special language for them - but you can program them from MicroPython.


#. The code to control RGB Board using PIO is shown below. You can copy the above code into Thonny or open the ``rgb_light.py`` under the path of ``pico_4wd_car-v2.0\examples``.

    .. note::

        You can visit |link_pio_micropython| to learn more about the functions involved in the code below.

.. code-block:: python

    import array, time
    from machine import Pin
    import rp2
    from rp2 import PIO, StateMachine, asm_pio
    # Configure the number of WS2812 LEDs.
    LIGHT_NUM = 24
    LIGHT_PIN = 19

    @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, 
    autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        label("bitloop")
        out(x, 1) .side(0) [T3 - 1]
        jmp(not_x, "do_zero") .side(1) [T1 - 1]
        jmp("bitloop") .side(1) [T2 - 1]
        label("do_zero")
        nop() .side(0) [T2 - 1]
    
    # Create the StateMachine with the ws2812 program, outputting on Pin(19).
    sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(LIGHT_PIN))
    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via a color value.
    ar = array.array("I", [0 for _ in range(LIGHT_NUM)])

    for i in range(LIGHT_NUM):
        ar[i] = 0xffaa00
    sm.put(ar,8)   

#. To run the script, click the |thonny_run| button or press ``F5``. When you power up the Pico 4WD car, you will see 3 RGB boards lit up in cyan color.

