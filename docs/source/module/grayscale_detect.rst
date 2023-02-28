2.Grayscale Detection
========================

This project will teach us how to read the grayscale module values and determine whether the Pico 4WD detects a line will cliff based on those values.

With the previous section :ref:`cpn_grayscale`, you can know that the value on the **white surface** > **black line** > **cliff**.


**1. Read Grayscale** (``grayscale_2.1_get_value.py``)

#. Copy the above code into Thonny or open the ``grayscale_2.1_get_value.py`` under the path of ``pico_4wd_car-v2.0\examples``.

    .. code-block:: python

        from machine import Pin, ADC
        import time

        gs0 = ADC(Pin(26))
        gs1 = ADC(Pin(27))
        gs2 = ADC(Pin(28))

        def get_value():
            return [gs0.read_u16(), gs1.read_u16(), gs2.read_u16()]

        while True:
            print(get_value())
            time.sleep(0.2)

#. To run the script, click the |thonny_run| button or press ``F5``.

#. After powering up the Pico 4WD car, place the grayscale module in three environments: white, black and hanging in the air (10cm or more) to see how the data in the Shell changes (keeping the USB cable connected to the computer).

    **White surface**
        You will find that the value of the white surface is generally large, for example mine is around 240,000.

    .. image:: img/grayscale_white.png

    **Black line**
        The value on the black line will be smaller, and now I'm at about 2000.

    .. image:: img/grayscale_black.png

    **Overhang (10cm or more)**
        And the value of the overhang will be even smaller, already less than 1000 in my environment.

    .. image:: img/grayscale_cliff.png

The values of these three environments must be recorded and will be used in the next project.

**2. Grayscale and cliff judging** (``grayscale_2.2_threshold.py``)

Next we need to make the car aware of its situation. Then we need to set two thresholds, ``edge_ref`` and ``line_ref``.

Taking my detection environment as an example. 

    * My car reads around 24000 in the white area and around 2000 in the black line, so I set ``line_ref`` to about the middle value of ``10000``.
    * In the cliff area it reads less than 1000, so I set ``edge_ref`` to ``1000``.

The next step is to use ``edge_ref`` and ``line_ref`` to make the Pico 4WD car react differently, as follows.

.. code-block:: python

    from machine import Pin, ADC
    
    gs0 = ADC(Pin(26))
    gs1 = ADC(Pin(27))
    gs2 = ADC(Pin(28))  
    edge_ref = 1000    # edge_reference
    line_ref = 10000 # line_reference      

    def get_value():
        return [gs0.read_u16(), gs1.read_u16(), gs2.read_u16()]

    def is_on_edge():
        gs_list = get_value()
        for value in gs_list:
            if value<=edge_ref:
                return True
        return False

    def get_line_status():
        gs_list = get_value()
        line_status=[]
        for value in gs_list:
            line_status.append(value<line_ref)
        return line_status

    while True:
        if is_on_edge():
            print("Danger!")
        else:
            print(get_line_status())

You will see that if you hang the Pico 4WD car in the air, the Shell will print "Danger! If the grayscale module detects a black line, True will be printed. On white surfaces, False will be printed.