@REM esptool.exe -help

esptool.exe --chip esp8266 --before no_reset_no_sync erase_flash

esptool.exe --chip esp8266 --before no_reset_no_sync write_flash 0 "esp8266-uart-wsserver-v1.0.2.bin"


pause

