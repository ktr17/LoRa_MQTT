# -*- coding: utf-8 -*-

import serial
import sys
from time import sleep
import paho.mqtt.client as mqtt

import Log
from Config import Config
from Lora import Lora
from Loralib import Loralib

flags = Flags()


def checkAck(mes):
    if mes.find("RSSI") >= 0:
        flags.isAck = True


def sendMes(mes):
    device.send("{0:04d}{1:04d}{2}".format(Config.panid, Config.child_id, mes))


def sendbackAck(mes):
    src_id = -1
    if mes.find("receive data info") >= 0:
        src_id = Loralib.extractionData(data=mes, target="srcid")

        device.send("{0:04d}{1:04d}Ack".format(Config.panid, src_id))


def sendMqtt(mes):
    datum = ""

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(Config.mqttHost, port=Config.mqttPort, keepalive=60)

    if mes.find("RSSI") >= 0:
        datum = Loralib.extractionData(data=mes, target="data")

        client.publish(Config.mqttTopic, "{}".format(datum))
        client.disconnect()


# MQTTの接続
def on_connect(client, userdata, flags, respons_code):
    print("status {}".format(respons_code))
    client.subscribe(Config.mqttTopic)


# MQTTで受信
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload, "utf-8"))
    sendMes("{0}:{1}".format(msg.topic, str(msg.payload, "utf-8")))


# MQTTの実行
def subMqtt():
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = sub.on_connect
    client.on_message = sub.on_message

    client.connect(Config.mqttHost, port=Config.mqttPort, keepalive=60)
    client.loop_forever()


def main():
    """
    親スレッドが死なないようにしているだけ
    """
    while True:
        sleep(1)

if __name__ == "__main__":
    args = sys.argv
    serial_device_name = "/dev/ttyUSB0"
    device = Lora(serial_device_name, args[0])
    sleep(5)
    device.addRecvlistener(sendbackAck)
    device.addRecvlistener(sendMqtt)

    main()

