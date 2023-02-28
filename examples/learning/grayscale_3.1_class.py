''' 
This file is only for learning, 
please refer to the libs file for actual use.
'''


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