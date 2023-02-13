from grayscale import Grayscale
import time

gs = Grayscale(26, 27, 28)

GRAYSCALE_EDGE_REFERENCE = 2000
GRAYSCALE_LINE_REFERENCE = 10000

def main():
    gs.set_edge_reference(GRAYSCALE_EDGE_REFERENCE)
    gs.set_line_reference(GRAYSCALE_LINE_REFERENCE)

    while True:
        value_list = gs.get_value()
        line_status = gs.get_line_status()
        is_edge = gs.is_on_edge()
        print(f"value:{value_list}, line_status:{line_status}, is_edge:{is_edge}")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
