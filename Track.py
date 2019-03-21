from bluepy.btle import Scanner, DefaultDelegate
import requests
import time
import json
import numpy as np

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
    mode = x[inds[i]]
    return mode

#Post data. This should be a list of distinct devices
def sendBleData(devices):
    for dev in devices:
        timestamp = time.time()
        bleData = json.dumps({"address":dev.addr, "addType":dev.addrType, "rssi":dev.rssi, "logTime": timestamp})
        response = requests.post(url = SERVER_ADDRESS, data = bleData, headers=HEADERS)

#Filter out devices of concern
def checkMac(devices):
    filteredList = list()
    for dev in devices:
        if dev.addr in MAC_LIST:
            filteredList.add(dev)
    return filteredList;
       
#Get devices in a short span, a 5 second scan 
def burstScan(scanLength, totalScanTime):
    t_end = time.time() + totalScanTime
    deviceMaster = list()
    while time.time() < t_end
        devices = scanner.scan(scanLength) #0.2
        deviceMaster.append(devices)
    return deviceMaster;

def sendBeaconData():
    deviceMasterList = burstScan(SCAN_DURATION, TOTAL_SCAN_TIME)
    filteredDeviceList = checkMac(deviceMasterList)
    #list1 = filter(lambda item: item.addr==MAC_LIST[0], filteredDeviceList)
    beaconList1 = [dev for dev in filteredDeviceList if dev.address==MAC_LIST[0]]
    beaconList2 = [dev for dev in filteredDeviceList if dev.address==MAC_LIST[1]]
    beaconList3 = [dev for dev in filteredDeviceList if dev.address==MAC_LIST[2]]
    #beaconList4 = [dev for dev in filteredDeviceList if dev.address==MAC_LIST[3]]
    #beaconList5 = [dev for dev in filteredDeviceList if dev.address==MAC_LIST[4]]
    
    rssiList1 = [dev.rssi for dev in beaconList1]
    rssiList2 = [dev.rssi for dev in beaconList2]
    rssiList3 = [dev.rssi for dev in beaconList3]
    #rssiList4 = [dev.rssi for dev in beaconList4]
    #rssiList5 = [dev.rssi for dev in beaconList5]
    
    mode1 = getMode(rssiList1)
    mode2 = getMode(rssiList2)
    mode3 = getMode(rssiList3)
    
    bleData1 = beaconList1[0]
    bleData2 = beaconList2[0]
    bleData3 = beaconList3[0]
    
    bleData1.rssi = mode1
    bleData2.rssi = mode2
    bleData3.rssi = mode3
    
    bleList = {bleData1, bleData2, bleData3}
    
    sendBleData(bleList)
    
def execute():
    while True:
        sendBeaconData()
        
execute()
   
#t_end = time.time() +5 
#while time.time() < t_end:
#    devices = scanner.scan(0.20)
    
#    sendBleData(devices)
#    print("END OF SCAN")
