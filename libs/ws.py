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
    print(f"x: {msg}")
    with open(LOG_FILE, "a") as log_f:
        log_f.write(f'\n> {msg}')
        time.sleep(0.01)

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

        self.send_dict["Name"] = self.name
        # log('reset ESP8266 module ...')
        # while True:
        #     try:
        #         self.set("RESET", timeout=1500  )
        #         break
        #     except TimeoutError:
        #         pass
        #     except UnicodeError:
        #         pass
        #     except Exception as e:
        #         log(e)
        # log('reset ESP8266 module ... Done')

    def read(self, block=False):
        buf = ""
        while True: 
            buf = self.uart.readline()
            log("buf: %s" % buf)
            if buf == None:
                if block:
                    time.sleep_ms(1)
                    continue
                else:
                    return None
            if buf[0] == 0xff or buf[0] == 0xfe:
                buf = buf[1:]
            buf = buf.decode().replace("\r\n", "")
            # log("buf: %s" % buf)
            if buf.startswith("[DEBUG] "):
                buf = buf.replace("[DEBUG]", "[ESP8266]")
                log(buf)
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
        log("Send command: %s" % command)
        command = "%s+%s" % (mode, command)
        self.write(command)

    def set(self, command, value=None, timeout=None):
        self._command("SET", command, value)
        t_s = time.ticks_ms()
        flag = 0
        retry_count = 0
        retry_max_count = 3

        while True:
            if flag == 0:
                onboard_led_ws.on()
                flag = 1
                time.sleep(0.1)
            else:
                onboard_led_ws.off()
                flag = 0
                time.sleep(0.1)

            if timeout != None:
                if(time.ticks_ms() - t_s > timeout):
                    raise TimeoutError('Set timeout %s ms'%timeout)

            try:
                result = self.read(block=False)
            except UnicodeError:
                if retry_count < retry_max_count:
                    log(f"UnicodeError retry {retry_count} ...")
                    self._command("SET", command, value)
                    t_s = time.ticks_ms()
                    retry_count += 1
                    continue

            if result == None:
                continue
            elif result.startswith("[ERROR]"):
                log(f"{result} retry {retry_count} ...")
                self._command("SET", command, value)
                t_s = time.ticks_ms()
                retry_count += 1
                continue
            elif result.startswith("[OK]"):
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
            log(e)
            log("Configuring WiFi Timeout.Please check whether the ESP8266 module is working.")
            return False
        
        try:
            if self.mode == "sta":
                log("Connecting to %s ... "%self.ssid)
            elif self.mode == "ap":
                log("open AP %s ... "%self.ssid)
            ip = self.set("START", timeout=None)
            log("WebServer started on ws://%s:%d" % (ip, self.port))
            return True
        except ValueError as e:
            log(e)
            log("Connect Wifi error. Try another Wifi or AP mode.")
            return False

    def is_connected(self):
        return self._is_connected
        
    def on_receive(self, data):
        pass

    def loop(self):
        receive = self.read()

        if receive == None:
            self.send_data()
            return
        elif receive.startswith("[CONNECTED]"):
            self._is_connected = True
            log("Connected from %s" % receive.split(" ")[1])
            self.send_data()
        elif receive.startswith("[DISCONNECTED]"):
            self._is_connected = False
            log("Disconnected from %s" % receive.split(" ")[1])
        else:
            try:
                data = json.loads(receive)
                if isinstance(data, str):
                    data = json.loads(data)
                self.on_receive(data)
                self.send_data()
            except ValueError as e:
                log("\033[0;31m[%s\033[0m"%e)
           

