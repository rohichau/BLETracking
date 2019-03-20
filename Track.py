from bluepy.btle import Scanner, DefaultDelegate
import requests
import time
import json

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass;
        '''if isNewDev and dev.addr in MAC_LIST:
            print("Discovered device", dev.addr)
        elif isNewData and dev.addr in MAC_LIST:
            print("Received new data from", dev.addr)'''

MAC_LIST = {"dc:0d:30:48:45:69"}
SERVER_ADDRESS = "http://192.168.43.100:8080/bleapp/postIt"
HEADERS = {'Content-Type':'application/json'}

def sendBleData(devices):
    for dev in devices:
        print(dev.addr)

        if dev.addr in MAC_LIST:
            timestamp = time.time()
            bleData = json.dumps({"address":dev.addr, "addType":dev.addrType, "rssi":dev.rssi, "logTime": timestamp})
            response = requests.post(url = SERVER_ADDRESS, data = bleData, headers=HEADERS)

scanner = Scanner().withDelegate(ScanDelegate())
t_end = time.time() +5 
while time.time() < t_end:
    devices = scanner.scan(0.20)
    sendBleData(devices)
    print("END OF SCAN")
            


       
     
