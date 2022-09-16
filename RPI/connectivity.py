import os
import RPi.GPIO as GPIO
import requests
import time

server = os.environ['SERVER_IP']
led = os.environ['LED_PIN']

#set GPIO pin
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT, initial=GPIO.HIGH)

def test_connectivity():
    connectivity = True
    try:
        requests.get(url='http://'+server+':5000/testConnectivity', timeout=2)
    except requests.exceptions.ConnectTimeout:
        connectivity = False
    #print(connectivity)
    return connectivity

while True:
    if test_connectivity():
        GPIO.output(led, False)
        time.sleep(300)
    else:
        GPIO.output(led, True)
        #wifi connection by wps
        os.system("wpa_cli -i wlan0 wps_pbc")
        time.sleep(5)