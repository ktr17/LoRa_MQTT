# -*- coding: utf-8 -*-

import serial
from threading import Thread
from time import sleep, time
from collections import deque

from Config import Config
from Log import Log


class Lora:

    def __init__(self, serialDeviceName, nodeType="Node.py"):
        try:
            Lora.device = serial.Serial(serialDeviceName, 115200)
        except Exception as e:
            raise
        Lora.sendMessages = deque()
        Lora.recvListeners = []
        self.nodeType = nodeType

        self.run()
        return

    """ シリアル通信の受信メッセージを送るメソッドを追加 """
    def addRecvlistener(self, recvEvent):
        Lora.recvListeners.append(recvEvent)
        return


    def run(self):
        Lora.__isStart = False
        Lora.__isLock = False

        # 各種設定
        Lora.send(["1", "a", "2"])
        Lora.send(["b", "4"])  # bw 125
        Lora.send(["c", "{}".format(Config.sf)])  # sf
        Lora.send(["d", "{}".format(Config.channel)])  # channel
        Lora.send(["e", "{}".format(Config.panid)]) # panid
        if self.nodeType == "Node.py":
            Lora.send(["f", "{}".format(Config.child_id)])  # 子機ID
        else:
            Lora.send(["f", "{}".format(Config.parent_id)])  # 親機ID
        Lora.send(["l", "2", "n", "2", "o", "2", "p", "1", "s", "1"])
        Lora.send(["u", "13"])
        Lora.send("z")
        self.__thSend = Thread(
            target=self.__sendThread,
            args=(None, Lora.device, Lora.sendMessages)
        )
        self.__thSend.setDaemon(True)
        self.__thSend.start()

        # Receive thread
        self.__thRecv = Thread(
            target=self.__recvThread,
            args=(None, Lora.device, Lora.recvListeners)
        )
        self.__thRecv.setDaemon(True)
        self.__thRecv.start()

        return


    @classmethod
    def send(self, data):
        """
        送信用スレッドにメッセージを格納する
        外部から呼び出し，引数にメッセージを格納することで，
        スレッドが処理をしてくれる
        """
        if type(data) == list:
            for datum in data:
                Lora.sendMessages.append(datum)
        else:
            Lora.sendMessages.append(data)
        return


    @staticmethod
    def __sendThread(self, device, sendMessages):
        """ 送信待機スレッド """
        while True:
            # 送信待機
            if not len(sendMessages):
                sleep(0.01)
                continue
            # ロック時 初期設定用 10秒以内にモジュールからリアクションがなければ次へ進む
            t = time()
            while(Lora.__isLock):
                if time() - t > 10.0:  # タイムアウト
                    break
                sleep(0.01)

            # 送信待機メッセージキューからデキュー
            msg = sendMessages.popleft()
            if msg == "":
                continue

            # メッセージ送信
            cmd = msg.strip()
            cmd = "{0}\r\n".format(cmd).encode()
            device.write(cmd)
            Log.add(cmd)

            # コマンド間隔 初期設定時
            if Lora.__isStart:
                Lora.__isLock = True
            else:
                sleep(0.1)  # 設定時

            # スタート検知
            if msg == "z":
                Lora.__isStart = True
        return


    # 取得したデータの抽出処理
    @classmethod
    def extraction_data(self, data="", target="srcid"):
        # データがNULLのときは終了
        extractionValue = ""
        if not data:
            Log.add("受信データの破損が疑われます.", "DEBUG")
            return

        if target == "srcid":
            try:
                data = data.split(" ")
                extractionValue = int(data[8][:-1])
            except Exception as e:
                extractionValue = -1

        elif target == "data":
            try:
                data = data.strip()
                extractionValue = data.split("Data(")[1][:-1]
            except Exception as e:
                extractionValue = -1

        return extractionValue


    # このスレッド内ですべての処理をする必要がある
    @staticmethod
    def __recvThread(self, device, recvListeners):
        """
        受信待機スレッド
        通常データを受信した場合は次の起動時刻を送信元に送る
        """
        src_id = -1
        datum = ""
        while True:
            # 受信待機
            if device.inWaiting() <= 0:
                sleep(0.01)
                continue

            # UTF-8に変換できない例外(ES920LR電源投入時発生)
            try:
                line = device.readline().decode("utf-8").strip()
                Log.add(line)
                Lora.__isLock = False
            except UnicodeDecodeError:
                continue

            # ロック解除 初期設定用
            if line == "OK" or line.find("NG") >= 0:
                Lora.__isLock = False

            if line.find("receive data info") >= 0:
                src_id = Lora.extraction_data(data=line, target="srcid")

            # filterにする
            if line.find("RSSI") >= 0:
                datum = Lora.extraction_data(data=line, target="data")

            # メッセージを転送
            for recvEvent in recvListeners:
                recvEvent(line)
            return


def log_lora(serialDevice):
    while True:
        if serialDevice.inWaiting() > 0:
            line = serialDevice.readline()
            line = line.decode("utf-8")
            Log.add(line)

if __name__=="__main__":
    devName = input("DeviceName /dev/??? > ")
    try:
        serialDevice = serial.Serial("/dev/{}".format(devName), 115200)
    except Exception as e:
        Log.add(e)

        thSerialDevice = Thread(target=log_lora, args=(serialDevice,))
        thSerialDevice.setDaemon(True)
        thSerialDevice.start()

   while True:
       preCmd = input("> ")
       cmd = "{}\r\n".format(preCmd).encode()
       serialDevice.write(cmd)
