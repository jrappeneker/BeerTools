#! /usr/bin/python2.7
from bluepy.btle import Scanner, DefaultDelegate
import time
import datetime
import logging

logging.basicConfig(format='%(message)s',filename='tilt.csv',level=logging.INFO)

TILTS = {
        'a495bb10c5b14b44b5121370f02d74de': 'Red',
        'a495bb20c5b14b44b5121370f02d74de': 'Green',
        'a495bb30c5b14b44b5121370f02d74de': 'Black',
        'a495bb40c5b14b44b5121370f02d74de': 'Purple',
        'a495bb50c5b14b44b5121370f02d74de': 'Orange',
        'a495bb60c5b14b44b5121370f02d74de': 'Blue',
        'a495bb70c5b14b44b5121370f02d74de': 'Yellow',
        'a495bb80c5b14b44b5121370f02d74de': 'Pink',
}

def to_celsius(fahrenheit):
    return round((fahrenheit - 32.0) / 1.8, 2)

# from the bluepy docs
# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            data = dev.getScanData()
            if len(data) >= 2 and len(data[1][2]) == 50 and (data[1][2][8:40]) in TILTS.keys():
                uuid = data[1][2][8:40]
                temp = to_celsius(int(data[1][2][41:44], 16))
                gravity = int(data[1][2][45:48], 16)
                logging.info('{},{:.1f},{}'.format(datetime.datetime.now().isoformat(), temp, gravity))

# from the bluepy docs
# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

# scan loop
while True:
    devices = scanner.scan(3.0)
    time.sleep(60)
