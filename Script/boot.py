from board import *
import digitalio
import storage
import supervisor
import wifi
import json

config = json.load(open('./config.json'))['config']

noStorageStatus = False
noStoragePin = digitalio.DigitalInOut(GP0)
noStoragePin.switch_to_input(pull=digitalio.Pull.UP)
noStorageStatus = not noStoragePin.value

if(noStorageStatus == False):
    storage.disable_usb_drive()
    storage.remount('/', readonly=False)
    # print("Disabling USB drive")
    supervisor.runtime.autoreload = False
else:
    supervisor.runtime.autoreload = True
    # print("USB drive enabled")

def startWiFi():
    wifi.radio.start_ap(ssid=config['ssid'], password=config['password'])
    HOST = repr(wifi.radio.ipv4_address_ap)
    PORT = 80  
    print(HOST,PORT)
     
startWiFi()