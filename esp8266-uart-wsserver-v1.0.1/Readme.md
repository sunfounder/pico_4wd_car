# ESP8266 UART Websocket Server Usage

Send command and data over UART in boardrate 115200

## Commands

`SET+SSID<ssid>`: set Wi-Fi SSID

```
SET+SSIDSunFounder
```

`SET+PSK<password>`: set Wi-Fi Password

```
SET+PSKsunfounder
```

`SET+PORT<port>`: set Websocket Port

```
SET+PORT8765
```

`SET+MODE<mode>`: set Wi-Fi Mode, STA = 1, AP = 1

```
SET+MODE1
```

`SET+START`: set Connect, return IP if connected

```
SET+CONNECT
```

## Data

`WS+<data>`: send data over websocket

```
WS+{"value": 25}
```

## Example

Here's an example connecting to Wi-Fi with ssid: SunFounder and password: sunfounder. Then echos what it reads from websocket client. `[tx]` is what you need to send over UART, and `[rx]` is what you get from rx. Under `[rx]`, `[DEBUG]` will only appear in debug mode, and without it, is what you receive for your code.

```
[tx] SET+SSIDMakerStarsHall  // Set ssid to MakerStarsHall
[rx] [DEBUG] RX Receive: SET+SSIDMakerStarsHall
[rx] [DEBUG] Set SSID: SunFounder
[rx] [OK]

[tx] SET+PSKsunfounder   // Set password to sunfounder
[rx] [DEBUG] RX Receive: SET+PSKsunfounder
[rx] [DEBUG] Set password: sunfounder
[rx] [OK]

[tx] SET+MODE1   // Set mode to STA
[rx] [DEBUG] RX Receive: SET+MODE1
[rx] [DEBUG] Set mode: 1
[rx] [OK]

[tx] SET+MODE2   // Set mode to AP
[rx] [DEBUG] RX Receive: SET+MODE1
[rx] [DEBUG] Set mode: 1
[rx] [OK]

[tx] SET+PORT8765   // Set websocket server port to 8765
[rx] [DEBUG] RX Receive: SET+PORT8765
[rx] [DEBUG] Set port: 8765
[rx] [OK]

[tx] SET+START   // Start connecting and start websocket server
[rx] [DEBUG] Connecting  // it will automaticaly try to connect to Wi-Fi as you fill in both ssid and password
[rx] [DEBUG] WiFi connected
[rx] [DEBUG] IP address:
[rx] 192.168.43.145
[rx] [DEBUG] Is server live? 1
[rx] [DEBUG] Websocker on!    // Now Websocket is on!

[rx] [DEBUG] RX Receive: Hello    // Websocket receives a hello.
[tx] WS+Hello    // Send out a Hello back to the Websocket client.
```

```
SET+SSIDbuibuibui
SET+PSKsunfounder
SET+MODE1
SET+PORT8765
SET+START

SET+SSIDaaa
SET+PSKsunfounder
SET+MODE2
SET+PORT8765
SET+START

SET+SSIDMakerStarsHall
SET+PSKsunfounder
SET+MODE1
SET+PORT8765
SET+START
```

## Changelog

- 2021-12-23: tide code, add timeout for serial read