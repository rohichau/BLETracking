from bluepy.btle import Scanner, DefaultDelegate
import requests
import time
import json
import numpy as np
from collections import defaultdict

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass;
        '''if isNewDev and dev.addr in MAC_LIST:
            print("Discovered device", dev.addr)
        elif isNewData and dev.addr in MAC_LIST:
            print("Received new data from", dev.addr)'''

MAC_LIST = {"dc:0d:30:48:45:69","dc:0d:30:48:45:8E","dc:0d:30:48:45:67"} #other devices can be added here
SERVER_ADDRESS = "http://192.168.43.100:8080/bleapp/postIt"  
SERVER_ADDRESS2 ="http://192.168.1.102:8080/bleapp/postIt" 
HEADERS = {'Content-Type':'application/json'}
SCAN_DURATION = 0.2
TOTAL_SCAN_TIME = 5

scanner = Scanner().withDelegate(ScanDelegate())

def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]

def getMode(x):
    x.sort()
    inds = indices(np.diff(x), lambda x: x > 0)
    i = max (np.diff(inds))
    mode = x[inds[i-1]]
    return mode

#Post data. This should be a list of distinct devices
def sendSingleBleData(dataTuple):
    timestamp = time.time()
    bleData = json.dumps({"address":dataTuple[0],"rssi":dataTuple[1], "logTime":timestamp})
    response = requests.post(url = SERVER_ADDRESS, data = bleData, headers=HEADERS)

#Get devices in a short span, a 5 second scan 
def burstScan(scanLength, totalScanTime):
    print("In burstScan")
    t_end = time.time() + totalScanTime
    filteredDeviceDict = defaultdict(list)
    while time.time() < t_end:
        devices = scanner.scan(scanLength) #0.2

        for dev in devices:
            if dev.addr in MAC_LIST and dev.addr not in filteredDeviceDict:
                filteredDeviceDict[dev.addr] = [dev.rssi]
            elif dev.addr in MAC_LIST and dev.addr in filteredDeviceDict:
                filteredDeviceDict[dev.addr].append(dev.rssi)
    return filteredDeviceDict;

def sendBeaconData():
    print("In sendBeaconData")
    filteredDeviceDict = burstScan(SCAN_DURATION, TOTAL_SCAN_TIME)

    for key in filteredDeviceDict:
        mode = np.average(filteredDeviceDict[key])
        dataTuple = (key,mode)
        sendSingleBleData(dataTuple)
        
def execute():
    print("In Execute")
    while True:
        sendBeaconData()
        
execute()
   

