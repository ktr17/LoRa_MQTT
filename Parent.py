# -*- coding: utf-8 -*-

import serial
from time import sleep, time

from Config import Config
from Lora import Lora
from Log import Log

def main():
    pass

if __name__ == "__main__":
    args = sys.argv
    serial_device_name = "/dev/ttyUSB0"
    device = Lora(serial_device_name, args[1])
    sleep(5)
    main()
