from machine import UART
import time
import json


from machine import Pin
led = Pin(25, Pin.OUT)

"custom Exception"
class TimeoutError(Exception):
    pass

class WS_Server():
    WS_TIMEOUT = 3000 # ms

    send_dict = {
        'Name': '',
        'Type': 'PICO-4WD Car',
        # 'Check': 'SunFounder Controller',
        'Check': 'SC',
        }

    def __init__(self, name=None, ssid=None, password='', mode=None, port=8765):
        self.name = name
        self.ssid = ssid
        self.password = password
        self.mode = mode.lower()
        self.port = port
        # self.uart = UART(1, 115200, timeout=100, timeout_char=10)
        self.uart = UART(1, 115200, timeout=10, timeout_char=5)

        self.listen_s = None
        self.client_s = None
        self.ws = None
        self.wlan = None

        self.send_dict["Name"] = self.name
        print('reset ESP8266 module ...')
        self.set("RESET", timeout=self.WS_TIMEOUT)


    def read(self, block=False):
        buf = ""
        # led_stat = False
        while True: 
            # led.value(not led_stat) 
            buf = self.uart.readline()
            if buf == None:
                if block:
                    # time.sleep_ms(10)
                    continue
                else:
                    # led.off()
                    return None
            if buf[0] == 0xff:
                buf = buf[1:]
            buf = buf.decode().replace("\r\n", "")
            # print("buf: %s" % buf)
            if buf.startswith("[DEBUG] "):
                buf = buf.replace("[DEBUG]", "[ESP8266]")
                print(buf)
            else:
                # led.off()
                return buf

    def write(self, value):
        value = "%s\n" % value
        value = value.encode()
        # print("ws write: %s" %value)
        self.uart.write(value)

    def send_data(self):
        data = json.dumps(self.send_dict)
        self._command("WS", data)

    def _command(self, mode, command, value=None):
        command += str(value) if value != None else ""
        # print("Send command: %s" % command)
        command = "%s+%s" % (mode, command)
        self.write(command)


    def set(self, command, value=None, timeout=None):
        self._command("SET", command, value)
        t_s = time.ticks_ms()
        while True:
            if timeout != None:
                if(time.ticks_ms() - t_s > timeout):
                    raise TimeoutError('Set timeout %s ms'%timeout)
            result = self.read(block=False)
            if result == None:
                continue
            # print("Result: %s" % result)
            if result.startswith("[ERROR]"):
                raise ValueError(result)
            if result.startswith("[OK]"):
                result = result[4:]
                result = result.strip(" ")
                break
        return result

    def _get(self, command):
        self._command("GET", command)
        result = self.read()
        return result

    def start(self):
        try:
            if self.mode == "sta":
                self.set("MODE", 1, timeout=self.WS_TIMEOUT)
            elif self.mode == "ap":
                self.set("MODE", 2, timeout=self.WS_TIMEOUT)
            self.set("SSID", self.ssid, timeout=self.WS_TIMEOUT)
            self.set("PSK", self.password, timeout=self.WS_TIMEOUT)
            self.set("PORT", self.port, timeout=self.WS_TIMEOUT)
        except TimeoutError as e:
            print(e)
            print("Configuring WiFi Timeout.Please check whether the ESP8266 module is working.")
            return False
        
        try:
            if self.mode == "sta":
                print("Connecting to %s ... "%self.ssid)
            elif self.mode == "ap":
                print("open AP %s ... "%self.ssid)
            ip = self.set("START", timeout=None)
            print("WebServer started on ws://%s:%d" % (ip, self.port))
            return True
        except ValueError as e:
            print(e)
            print("Connect Wifi error. Try another Wifi or AP mode.")
            return False


    def on_receive(self, data):
        pass

    def loop(self):
        # print("waiting for uart data...")

        st = time.ticks_ms()
        receive = self.read()
        # print('ws_rx_ut: ', time.ticks_ms()-st)

        # print("Received.")
        # print("ws loop, receive: %s" % receive)

        # st = time.ticks_ms()
        if receive == None:
            self.send_data()
            return
        elif receive.startswith("[CONNECTED]"):
            print("Connected from %s" % receive.split(" ")[1])
            self.send_data()
        elif receive.startswith("[DISCONNECTED]"):
            print("Disconnected from %s" % receive.split(" ")[1])
        else:
            try:
                # print("on revceive: %s" % receive)
                data = json.loads(receive)
                if isinstance(data, str):
                    data = json.loads(data)
                self.on_receive(data)
            except ValueError as e:
                print("\033[0;31m[%s\033[0m"%e)
            self.send_data()
        # print('ws_rh_ut: ', time.ticks_ms()-st)

