from machine import UART
import time
import json

from machine import Pin
led = Pin(25, Pin.OUT)

class WS_Server():

    send_dict = {
        'Name': '',
        'Type': 'PICO-4WD Car',
        'Check': 'SunFounder Controller',
        }

    def __init__(self, name=None, ssid=None, password='', mode=None, port=8765):
        self.name = name
        self.ssid = ssid
        self.password = password
        self.mode = mode.lower()
        self.port = port
        self.uart = UART(1, 115200, timeout=10000, timeout_char=1000)
        self.listen_s = None
        self.client_s = None
        self.ws = None
        self.wlan = None

        self.send_dict["Name"] = self.name

        self.set("RESET")

    def read(self):
        buf = ""
        while 1: 
            buf = self.uart.readline()
            if buf == None:
                time.sleep_ms(10)
                continue
            if buf[0] == 0xff:
                buf = buf[1:]
            buf = buf.decode().replace("\r\n", "")
            # print("buf: %s" % buf)
            if buf.startswith("[DEBUG] "):
                buf = buf.replace("[DEBUG]", "[ESP8266]")
                print(buf)
            else:
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

    def set(self, command, value=None):
        self._command("SET", command, value)
        while True:
            result = self.read()
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
        led.high()
        if self.mode == "ap":
            self.set("SSID", self.name)
            led.low()
            self.set("PSK", self.password)
            self.set("MODE", 2)
        elif self.mode == "sta":
            self.set("SSID", self.ssid)
            led.low()
            self.set("PSK", self.password)
            self.set("MODE", 1)
        
        self.set("PORT", self.port)
        print("Connecting")
        try:
            ip = self.set("START")
            print("WebServer started on ws://%s:%d" % (ip, self.port))
        except ValueError as e:
            print(e)
            print("Connect Wifi error. Try another Wifi or AP mode.")

    def on_receive(self, data):
        pass

    def loop(self):
        # print("waiting for uart data...")
        receive = self.read()
        # print("Received.")
        # print("ws loop, receive: %s" % receive)
        if receive == None:
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
                print(e)
            self.send_data()
