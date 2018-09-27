# -*- coding: utf-8 -*-

import  sys
from time import sleep
import paho.mqtt.client as mqtt

from Config import Config
from Log import Log

print("*** 開始 ***\n")


def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))

    client.subscribe(Config.mqttTopic)

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload,'utf-8'))

if __name__ == '__main__':

    client = mqtt.Client(protocol=mqtt.MQTTv311)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(Config.mqttHost, port=Config.mqttPort, keepalive=60)

    client.loop_forever()

print("*** 終了 ***\n")
