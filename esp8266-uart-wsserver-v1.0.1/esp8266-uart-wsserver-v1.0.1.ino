#include <WebSocketsServer.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

// for production, uncomment this line
// #define DEBUG

#define SERIAL_TIMEOUT 100 // 100ms

// Mode
#define NONE 0
#define STA 1
#define AP 2

// internal Variables
String ssid = "";
String password = "";
int port = 0;
int mode = NONE;

bool isConnected = false;
String ip = "";
String rxBuf = "";
uint8_t client_num = 0;

WebSocketsServer webSocket = WebSocketsServer(8765);

bool wifiClient();
bool wifiAP();
bool connectWiFi();
String serialRead();
void handleSet(String cmd);
void handleGet(String cmd);
String intToString(uint8_t * value, size_t length);
void onWebSocketEvent(uint8_t cn, WStype_t type, uint8_t * payload, size_t length);

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(SERIAL_TIMEOUT);
  #ifdef DEBUG
  Serial.println("[DEBUG] Start!");
  #endif
  Serial.println("\r\n[OK]");
}

void loop() {
  rxBuf = serialRead();
  if (rxBuf.length() > 0) {
    #ifdef DEBUG
    Serial.print("[DEBUG] RX Receive: ");Serial.println(rxBuf);
    #endif
    delay(10);
    if (rxBuf.substring(0, 4) == "SET+"){
      handleSet(rxBuf.substring(4));
    } else if (rxBuf.substring(0, 3) == "WS+"){
      String out = rxBuf.substring(3);
      #ifdef DEBUG
      Serial.print("[DEBUG] Read from Serial: ");Serial.println(out);
      #endif
      webSocket.sendTXT(client_num, out);
    }
  }
  if (isConnected){
    webSocket.loop();
  }
  delay(10);
}

bool wifiClient(){
  // Connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  // Wait some time to connect to wifi
  int count = 0;
  #ifdef DEBUG
  Serial.print("[DEBUG] Connecting.");
  #endif
  while (WiFi.status() != WL_CONNECTED) {
    #ifdef DEBUG
    Serial.print(".");
    #endif
    delay(500);
    count ++;
    if (count > 30){
      #ifdef DEBUG
      Serial.println("");
      #endif
      return false;
    }
  }
  #ifdef DEBUG
  Serial.println("");
  #endif
  ip = WiFi.localIP().toString();
  return true;
}

bool wifiAP(){
  WiFi.softAP(ssid, password);
  ip = WiFi.softAPIP().toString();
  return true;
}

bool connectWiFi(){
  bool ret;

  #ifdef DEBUG
  Serial.print("[DEBUG] Mode:");
  #endif
  if (mode == AP){
    #ifdef DEBUG
    Serial.println("AP");
    #endif
    ret = wifiAP();
  } else if (mode == STA) {
    #ifdef DEBUG
    Serial.println("STA");
    #endif
    ret = wifiClient();
  }

  if (!ret){
    return false;
  }

  #ifdef DEBUG
  Serial.print("[DEBUG] IP address: ");Serial.println(ip);
  #endif

  isConnected = true;
  webSocket = WebSocketsServer(port);
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
  #ifdef DEBUG
  Serial.println("[DEBUG] Websocket on!");
  #endif
  return true;
}

String serialRead() {
  String buf = "";
  char inChar;
  int temp;
  unsigned long timeoutStart = millis();
  while (Serial.available() && millis() - timeoutStart < SERIAL_TIMEOUT) {
    temp = Serial.read();
    inChar = (char)temp;
    if (inChar == '\n') {
      break;
    } else if((int)inChar != 255){
      buf += inChar;
    }
  }
  return buf;
}

void handleSet(String cmd){
  if (cmd.substring(0, 4) == "SSID"){
    ssid = cmd.substring(4);
    #ifdef DEBUG
    Serial.print("[DEBUG] Set SSID: ");Serial.println(ssid);
    #endif
    Serial.println("[OK]");
  } else if (cmd.substring(0, 3) == "PSK"){
    password = cmd.substring(3);
    #ifdef DEBUG
    Serial.print("[DEBUG] Set password: ");Serial.println(password);
    #endif
    Serial.println("[OK]");
  } else if (cmd.substring(0, 4) == "PORT"){
    port = cmd.substring(4).toInt();
    #ifdef DEBUG
    Serial.print("[DEBUG] Set port: ");Serial.println(port);
    #endif
    Serial.println("[OK]");
  } else if (cmd.substring(0, 4) == "MODE"){
    mode = cmd.substring(4).toInt();
    #ifdef DEBUG
    Serial.print("[DEBUG] Set mode: ");
    if (mode == AP){
      Serial.println("AP");
    } else if (mode == STA) {
      Serial.println("STA");
    }
    #endif
    Serial.println("[OK]");
  } else if (cmd.substring(0, 5) == "RESET"){
    #ifdef DEBUG
    Serial.println("[DEBUG] Reset");
    #endif
    delay(10);
    ESP.reset();
  } else if (cmd.substring(0, 5) == "START"){
    if (ssid.length() == 0) {
      Serial.println("[ERROR] Please set ssid");
    } else if (password.length() == 0) {
      Serial.println("[ERROR] Please set password");
    } else if (mode == NONE) {
      Serial.println("[ERROR] Please set mode");
    } else if (port == 0) {
      Serial.println("[ERROR] Please set port");
    } else{
      bool result = connectWiFi();
      if (!result) {
        Serial.println("[ERROR] TIMEOUT");
      } else {
        Serial.print("[OK] ");Serial.println(ip);
      }
    }
  }
}

void handleGet(String cmd){
  if (cmd.substring(0, 4) == "IP"){
    Serial.println(ip);
  } else if (cmd.substring(0, 6) == "STATUS") {
    Serial.println(WiFi.status() != WL_CONNECTED);
  }
}

String intToString(uint8_t * value, size_t length) {
  // #ifdef DEBUG
  // Serial.println("[DEBUG] intToString");
  // #endif
  String buf;
  for (int i=0; i<length; i++){
    buf += (char)value[i];
  }
  return buf;
}

void onWebSocketEvent(uint8_t cn, WStype_t type, uint8_t * payload, size_t length) {
  String out;
  client_num = cn;
  #ifdef DEBUG
  Serial.println("[DEBUG] onWebSocketEvent");
  #endif
  switch(type) {
    // Client has disconnected
    case WStype_DISCONNECTED:{
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] Disconnected!");
      #endif
      IPAddress remoteIp = webSocket.remoteIP(client_num);
      Serial.print("[DISCONNECTED] ");Serial.println(remoteIp.toString());
      break;
    }
    // New client has connected
    case WStype_CONNECTED:{
      IPAddress remoteIp = webSocket.remoteIP(client_num);
      #ifdef DEBUG
      Serial.print("[DEBUG] [WS] Connection from ");
      Serial.println(remoteIp.toString());
      #endif
      Serial.print("[CONNECTED] ");Serial.println(remoteIp.toString());
      // out = serialReadBlock();
      // webSocket.sendTXT(client_num, out);
      break;
    }
    case WStype_TEXT:{
      // #ifdef DEBUG
      // Serial.printf("[DEBUG] [%u] Received text: ", client_num);
      // #endif
      out = intToString(payload, length);
      #ifdef DEBUG
      Serial.print("[DEBUG] [WS] Received text: ");Serial.println(out);
      #endif
      Serial.println(out);
      // out = serialReadBlock();
      // #ifdef DEBUG
      // Serial.print("[DEBUG] Read from Serial: ");Serial.println(out);
      // #endif
      // webSocket.sendTXT(client_num, out);
      break;
    }
    // For everything else: do nothing
    case WStype_BIN: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_BIN");
      #endif
      break;
    }
    case WStype_ERROR: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_ERROR");
      #endif
      break;
    }
    case WStype_FRAGMENT_TEXT_START: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_FRAGMENT_TEXT_START");
      #endif
      break;
    }
    case WStype_FRAGMENT_BIN_START: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_FRAGMENT_BIN_START");
      #endif
      break;
    }
    case WStype_FRAGMENT: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_FRAGMENT");
      #endif
      break;
    }
    case WStype_FRAGMENT_FIN: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_FRAGMENT_FIN");
      #endif
      break;
    }
    case WStype_PING: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_PING");
      #endif
      break;
    }
    case WStype_PONG: {
      #ifdef DEBUG
      Serial.println("[DEBUG] [WS] WStype_PONG");
      #endif
      break;
    }
    default: {
      #ifdef DEBUG
      Serial.print("[DEBUG] [WS] Event Type: [");Serial.print(type);Serial.println("]");
      #endif
      break;
    }
  }
}
