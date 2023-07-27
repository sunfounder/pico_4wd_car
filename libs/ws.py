import os

if os.uname().machine == "Raspberry Pi Pico W with RP2040":
    from ws_pico_w import *
else:
    from ws_esp01 import *