from machine import UART
import time
import json

from machine import Pin
onboard_led_ws = Pin(25, Pin.OUT)

"custom Exception"
class TimeoutError(Exception):
    pass

LOG_FILE = "log.txt"

def log(msg):
    with open(LOG_FILE, "a") as log_f:
        log_f.write(f'\n> {msg}')
        time.sleep(0.01)

class WS_Server():
    WS_TIMEOUT = 3000 # ms
    SEND_INTERVAL = 100 # ms
    
    send_dict = {
        'Name': '',
        'Type': 'PICO-4WD Car',
        'Check': 'SC',
        }

    def __init__(self, name=None, ssid=None, password='', mode=None, port=8765):
        self.name = name
        self.ssid = ssid
        if self.ssid == None or self.ssid == "":
            self.ssid = name
        self.password = password
        self.mode = mode.lower()
        self.port = port
        # self.uart = UART(1, 115200, timeout=100, timeout_char=10)
        self.uart = UART(1, 115200, timeout=10, timeout_char=5)

        self.listen_s = None
        self.client_s = None
        self.ws = None
        self.wlan = None
        self._is_connected = False
        # self.last_send_time = 0

        self.send_dict["Name"] = self.name
        print('reset ESP8266 module ...')
        esp8266_version = self.set("RESET", timeout=2500)
        print(f'ESP8266 module firmware version {esp8266_version}')

    def read(self, block=False):
        buf = ""
        while True: 
            buf = self.uart.readline()
            if buf == None:
                if block:
                    time.sleep_ms(1)
                    continue
                else:
                    return None

            if buf[0] < 0x31 or buf[0] > 0xfe:
                buf = buf[1:]
                log("bufxx: %s" % buf)
                if buf == '':
                    buf = "GARBLED" # Garbled characters
                    return buf
                     
            buf = buf.decode().replace("\r\n", "")
            if buf.startswith("[DEBUG] "):
                buf = buf.replace("[DEBUG]", "[ESP8266]")
            else:
                return buf

    def write(self, value):
        value = "%s\n" % value
        value = value.encode()
        self.uart.write(value)

    def send_data(self):
        data = json.dumps(self.send_dict)
        self._command("WS", data)

    def _command(self, mode, command, value=None):
        command += str(value) if value != None else ""
        command = "%s+%s" % (mode, command)
        self.write(command)

    def set(self, command, value=None, timeout=None):
        flag = 0
        retry_count = 0
        retry_max_count = 3
        t_s = 0

        # retry function
        def retry():
            nonlocal  t_s, retry_count
            self._command("SET", command, value)
            t_s = time.ticks_ms()
            retry_count = retry_count + 1

        # send command
        self._command("SET", command, value)
        # get start time
        t_s = time.ticks_ms()

        while True:
            # onboard LED flash
            if flag == 0:
                onboard_led_ws.on()
                flag = 1
                time.sleep(0.1)
            else:
                onboard_led_ws.off()
                flag = 0
                time.sleep(0.1)

            # Timeout handle
            if timeout != None:
                if(time.ticks_ms() - t_s > timeout):
                    if retry_count < retry_max_count:
                        log(f"TimeoutError. retry {retry_count} ...     ")
                        retry()
                        continue
                    raise TimeoutError('Set timeout %s ms'%timeout)

            # UnicodeError
            try:
                result = self.read(block=False)
            except UnicodeError:
                if retry_count < retry_max_count:
                    log(f"UnicodeError retry {retry_count} ...")
                    retry()
                    continue
                log("UnicodeError")
            
            # result
            if result == None:
                continue
            elif result.startswith("[ERROR]"):
                if retry_count < retry_max_count:
                    log(f"{result} retry {retry_count} ...")
                    retry()
                    continue
                log("result == [ERROR]")
                
            elif result == 'GARBLED':
                if retry_count < retry_max_count:
                    log(f"result GARBLED retry {retry_count} ...")
                    retry()
                    continue
                log("result GARBLED ")

            elif result.startswith("[OK]"):
                result = result[4:]
                result = result.strip(" ")
                break
            else:
                continue

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

    def is_connected(self):
        return self._is_connected
        
    def on_receive(self, data):
        pass

    def loop(self):
        receive = self.read()
        # if receive is not None:
        #     print(f"ws.loop received: {receive}")
            
        if receive == None:
            self.send_data()
            return
        elif receive.startswith("[CONNECTED]"):
            self._is_connected = True
            print("Connected from %s" % receive.split(" ")[1])
            self.send_data()
        elif receive.startswith("[DISCONNECTED]"):
            self._is_connected = False
            print("Disconnected from %s" % receive.split(" ")[1])
        elif receive.startswith("[APPSTOP]"):
            self._is_connected = False
        else:
            try:
                data = json.loads(receive)
                if isinstance(data, str):
                    data = json.loads(data)
                self._is_connected = True
                self.on_receive(data)
                self.send_data()
            except ValueError as e:
                pass
                # print("\033[0;31m[%s\033[0m"%e)
        
        # if (time.ticks_ms() - self.last_send_time > self.SEND_INTERVAL):
        #     self.send_data()
        #     self.last_send_time = time.ticks_ms()

           

