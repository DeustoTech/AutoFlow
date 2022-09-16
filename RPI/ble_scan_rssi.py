
import asyncio
from bleak import BleakScanner
#import record # Uncoment this line to use Deep Learing model 
import record_ml as record # Using ML model
import time
import sys

beacon_add = "8C:34:01:F7:9A:04"
rssi_th = -50
device_found = False
ble_scan_freq = 5 #scan every 5 seconds
ble_scan_d = 5


def detection_callback(device, advertisement_data):
    global device_found
    if device.address==beacon_add and device.rssi > rssi_th:
        print('Device found. RSSI = '+str(device.rssi))
        device_found = True
        record.record() 


#------------------------------------------------------        
async def main():
    print('>>>>  BLE scaning  >>>>')
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(ble_scan_d) #scan for 'ble_scan_d seconds'
    print('scaning stopped')
    await scanner.stop()

#------------------------------------------------------
#           MAIN PROGRAM LOOP
#-----------------------------------------------------
try:
    while True:
        if not device_found:    
            time.sleep(ble_scan_freq) #SCAN EVERY 'ble_scan_freq' SECONDS
            asyncio.run(main())   
        else:
            run = True
            record.record()

except (KeyboardInterrupt, SystemExit):
    run = False
    sys.exit()
