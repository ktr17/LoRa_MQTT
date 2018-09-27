# -*- coding: utf-8 -*-

import sys
import serial
from time import sleep, time

import Log
from Config import Config
from Lora import Lora
from Flags import Flags


flags = Flags()

def checkAck(mes):
    if mes.find("RSSI") >= 0:
        flags.isAck = True

def sendMes():
    __i = 1
    device.send("{0:04d}{1:04d}{2:011d}".format(Config.panid, Config.parent_id, __i))
    while True:
        sleep(2)
        if flags.isAck:
            __i = __i + 1
            device.send("{0:04d}{1:04d}{2:011d}".format(Config.panid, Config.parent_id, __i))
            flags.isAck = False
        else:
            device.send("{0:04d}{1:04d}{2:011d}".format(Config.panid, Config.parent_id, __i))

if __name__ == "__main__":
    args = sys.argv
    serial_device_name = "/dev/ttyS0"
    device = Lora(serial_device_name, args[0])
    sleep(5)
    device.addRecvlistener(checkAck)
    sendMes()

