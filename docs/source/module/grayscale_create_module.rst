3. ``grayscale.py`` Module
=============================

Similarly, in order to keep the code simple and organized when using the grayscale module with other modules, we have encapsulated all its related code into a library.

When you use it, you just need to import this library, and you can call the functions inside directly.

For example, the following two functions can be used to know if a cliff or black line is detected.

.. code-block:: python

    is_on_edge()
    get_line_status()


.. note::

    The final encapsulated library ``grayscale.py`` has been saved in ``pico_4wd_car-v2.0\libs``, which may differ from the ones shown in the course, so please refer to the file under ``libs`` path when using it.

#. Encapsulate the code related to the grayscale module into a library, as follows.


    .. code-block:: python

        from machine import Pin, ADC

        class Grayscale():

            def __init__(self, pin0=26, pin1=27, pin2=28):
                self.gs0 = ADC(Pin(pin0))
                self.gs1 = ADC(Pin(pin1))
                self.gs2 = ADC(Pin(pin2))
                self.edge_ref = 1000    # edge_reference
                self.line_ref = 10000 # line_reference

            def get_value(self):
                return [self.gs0.read_u16(), self.gs1.read_u16(), self.gs2.read_u16()]
                
            def is_on_edge(self):
                gs_list = self.get_value()
                return gs_list[2] <= self.edge_ref or gs_list[1] <= self.edge_ref or gs_list[0] <= self.edge_ref

            def get_line_status(self):
                gs_list = self.get_value()
                return [int(value < self.line_ref) for value in gs_list]

        # init
        gs = Grayscale(26, 27, 28)

        # detect
        while True:
            if gs.is_on_edge():
                print("Danger!")
            else:
                print(gs.get_line_status())

#. We have written cliff and black line thresholds in this module(library), but the thresholds are different for different environments when using it. So 2 other functions were created to make it easy for you to modify the thresholds in the main program.

    .. code-block:: python
        :emphasize-lines: 23,24,26,27,33,34

        from machine import Pin, ADC

        class Grayscale():

            def __init__(self, pin0=26, pin1=27, pin2=28):
                self.gs0 = ADC(Pin(pin0))
                self.gs1 = ADC(Pin(pin1))
                self.gs2 = ADC(Pin(pin2))
                self.edge_ref = 1000    # edge_reference
                self.line_ref = 10000 # line_reference

            def get_value(self):
                return [self.gs0.read_u16(), self.gs1.read_u16(), self.gs2.read_u16()]
                
            def is_on_edge(self):
                gs_list = self.get_value()
                return gs_list[2] <= self.edge_ref or gs_list[1] <= self.edge_ref or gs_list[0] <= self.edge_ref

            def get_line_status(self):
                gs_list = self.get_value()
                return [int(value < self.line_ref) for value in gs_list]

            def set_edge_reference(self, value):
                self.edge_ref = value

            def set_line_reference(self, value):
                self.line_ref = value

        # init
        gs = Grayscale(26, 27, 28)

        # config
        gs.set_edge_reference(800)
        gs.set_line_reference(12000)    

        # detect
        while True:
            if gs.is_on_edge():
                print("Danger!")
            else:
                print(gs.get_line_status())

