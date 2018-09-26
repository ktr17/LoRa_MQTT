# -*- coding: utf-8 -*-

import sys
import serial
from time import sleep, time

from Config import Config
from Lora import Lora
from Log import Log


def main():
    __i = 1
    while True:
        device.send("{0:04d}{1:04d}{2:011d}".format(Config.panid, Config.gwid, __i))
        __i = __i + 1
        sleep(5) # 5秒ごとにデータを送る


if __name__ == "__main__":
    args = sys.argv
    serial_device_name = "/dev/ttyS0"
    device = Lora(serial_device_name, args[1])
    sleep(5)
    main()
