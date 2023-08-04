@echo off
reg query "HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\SERIALCOMM"
set /p comno=
echo "[erase flash]"
python -m esptool --chip ESP32 --port COM%comno% erase_flash
echo "[write fireware]"
python -m esptool --chip esp32 --port COM%comno% --baud 921600 write_flash -z 0x1000 esp32_espnow_1.19.1.bin
echo "[fireware info]"
python -m esptool --chip esp32 --port COM%comno% flash_id
echo "[press any key to exit]"
pause
