from machine import Pin, ADC

class Grayscale():
    GRAYSCALE_EDGE_REFERENCE = 20
    GRAYSCALE_LINE_REFERENCE = 10000

    def __init__(self, pin0, pin1, pin2):
        self.gs0 = ADC(Pin(26))
        self.gs1 = ADC(Pin(27))
        self.gs2 = ADC(Pin(28))
        self.edge_ref = 20    # edge_reference
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
