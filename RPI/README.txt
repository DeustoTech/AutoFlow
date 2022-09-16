ENVIRONMENT VARIABLES
-------------------------
export SERVER_IP="{IP ADDRESS}"
export LED_PIN=12

DEPENDENCIES
------------------
sudo apt-get install python3-pyaudio
# Inference with DL model
pip install requirements_dl.txt
# Inference with ML model
pip install requirements_ml.txt


MICROPHONE DRIVERS
---------------------
ENABLE I2C and SPI on the RPI
sudo apt-get update
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install_arm64.sh
sudo reboot now

------------------------------------------
		SETUP
-----------------------------------------
* To start manually: run ble_scan_rssi.py

crontab -e 
@reboot python3 {PROJECT_PATH}/connectivity.py
@reboot python3 {PROJECT_PATH}/ble_scan_rssi.py
