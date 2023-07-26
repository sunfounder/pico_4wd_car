
import socket
import uos
import network
import uwebsocket
import time
import json
import hashlib
import binascii

"custom Exception"
class TimeoutError(Exception):
    pass

LOG_FILE = "log.txt"

def log(msg):
    with open(LOG_FILE, "a") as log_f:
        log_f.write(f'\n> {msg}')
        time.sleep(0.01)

class WS_Server():

    PING_PONG_TIMEOUT = 3000 # ms
    send_dict = {
        'Name': '',
        'Type': 'PICO-4WD Car',
        'Check': 'SC',
        }

    def __init__(self, name=None, ssid=None, password='', mode=None, port=8765):
        self.port = port
        self.listen_s = None
        self.client_s = None
        self.ws = None
        self.wlan = None
        self.name = name
        self.ssid = ssid
        self.password = password
        self.mode = mode
        self.send_dict['Name'] = name
        self._is_started = False
        self.ping_pong_timeout_start = 0
    
    def server_handshake(self, sock):
        clr = sock.makefile("rwb", 0)
        l = clr.readline()

        webkey = None

        while 1:
            l = clr.readline()
            if not l:
                raise OSError("EOF in headers")
            if l == b"\r\n":
                break
            h, v = [x.strip() for x in l.split(b":", 1)]
            if h == b'Sec-WebSocket-Key':
                webkey = v

        if not webkey:
            raise OSError("Not a websocket request")

        respkey = webkey + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        respkey = hashlib.sha1(respkey).digest()
        respkey = binascii.b2a_base64(respkey)[:-1]

        resp = b"""\
HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: %s\r
\r
""" % respkey

        sock.send(resp)

        
    def setup_conn(self, accept_handler):
        self.listen_s = socket.socket()
        self.listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ai = socket.getaddrinfo("0.0.0.0", self.port)
        addr = ai[0][4]

        self.listen_s.bind(addr)
        self.listen_s.listen(5)
        if accept_handler:
            self.listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print("WebServer started on ws://%s:%d" % (iface.ifconfig()[0], self.port))
        return self.listen_s

    def accept_conn(self, listen_sock):
        cl, remote_addr = listen_sock.accept()
        print("\nWebSocket connection from:", remote_addr)
        self.client_s = cl
        self.server_handshake(cl)
        self.ws = uwebsocket.websocket(cl, True)
        self.ws.write(json.dumps(self.send_dict))
        print("have sended!")
        cl.setblocking(False)

    def read(self):
        if self.ws == None:
            return None
        recv = self.ws.read()
        if recv != None and recv != b"":
            recv = recv.decode()
            # print("accept_conn: %s" % recv)
            return recv
        else:
            return None

#     def read(self):
#         if self.ws == None:
#             return None
#         print('read 1')
#         buffer = ''
#         while True:
#             recv = self.ws.read(1)
#             if recv != None and recv != b"":
#                 recv = recv.decode()
#                 buffer += recv
#                 if recv == '}':
#                     break;
#             else:
#                 break
#         print('read 2')
#         return buffer

    def is_started(self):
        return self._is_started
        
    def write(self, value):
        value = value.encode()
        self.ws.write(value)

    def send_data(self):
        data = json.dumps(self.send_dict)
        self.write(data)

    def stop(self):
        if self.client_s:
            self.client_s.close()
        if self.listen_s:
            self.listen_s.close()
        self.wlan.active(False)

    def start(self):
        if self.mode == "ap":
            self.wlan = network.WLAN(network.AP_IF)
            self.wlan.config(essid=self.name, password=self.password)
            self.wlan.active(True)  # turning on the hotspot
        elif self.mode == "sta":
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.connect(self.ssid, self.password)
            for _ in range(5):
                if self.wlan.isconnected():
                    print('network config:', self.wlan.ifconfig())
                    break
                time.sleep(1)
            if not self.wlan.isconnected():
                print("wifi connected fail ")
        self.setup_conn(self.accept_conn)
        self.ping_pong_timeout_start = time.ticks_ms()
        return True

    def on_receive(self, data):
        pass

    def loop(self):
        if time.ticks_ms() - self.ping_pong_timeout_start > self.PING_PONG_TIMEOUT:
            self._is_started = False
        receive = self.read()
        # print("Received.")
        # print("ws loop, receive: %s" % receive)
        if receive == None or len(receive) == 0:
            pass
        elif receive == 'ping':
            self.write('pong')
            self.ping_pong_timeout_start = time.ticks_ms()
            self._is_started = False
        else:
            try:
                # print("on revceive: %s" % receive)
                data = json.loads(receive)
                if isinstance(data, str):
                    data = json.loads(data)
                self.on_receive(data)
                self.ping_pong_timeout_start = time.ticks_ms()
                self._is_started = True
            except ValueError as e:
                print(e)
            self.send_data()
            
        time.sleep_ms(10)
