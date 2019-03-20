from bluepy.btle import Scanner, DefaultDelegate
import requests
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass;
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

MAC_LIST = {};
SERVER_ADDRESS = "http://192.168.43.100:8080/bleapp/postIt"
HEADERS = "Content-Type":application/json

def sendBleData(devices):
    for dev in devices:
        if dev.addr not in MAC_LIST:
            bleData = {"address":dev.addr, "addType":dev.addrType, "rssi":dev.rssi, "logTime": time.time()}
            response = requests.post(url = SERVER_ADDRESS, data = bleData)

scanner = Scanner().withDelegate(ScanDelegate())

while True:
    devices = scanner.scan(0.2)
    sendBleData(devices)
            


       
     
