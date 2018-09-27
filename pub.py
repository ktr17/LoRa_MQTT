# -*- coding: utf-8 -*-
import  sys
from time import sleep
import paho.mqtt.client as mqtt

from Config import Config


print("*** 開始 ***\n")

client = mqtt.Client(protocol=mqtt.MQTTv311)

client.connect(Config.mqttHost, port=Config.mqttPort, keepalive=60)

for i in range(3):
    client.publish(Config.mqttTopic, "{}: Hello".format(i))
    sleep(0.4)

client.disconnect()

print("*** 終了 ***\n")
