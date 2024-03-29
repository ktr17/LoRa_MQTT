# -*- coding: utf-8 -*-
from datetime import datetime
from os import mkdir
from os.path import isdir
from threading import Thread

from Config import Config

class Log():
    """ 各種ログ記録用クラス """
    __dirname = "logs"

    def __init__(self):
        self.__checkDirectory()
        return

    """ ログ追記用メソッド """
    @staticmethod
    def add(message, title="INFO"):
        # 1行ログ生成
        time = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        line = "[{0}]\t[{1}]\t{2}\n".format(time, title, message)
        if Config.debug_level == "ALL":
            print(line)
        elif Config.debug_level == "INFO":
            if title == "INFO":
                print(line)
        elif Config.debug_level == "DEBUG":
            if title == "DEBUG":
                print(line)

        # ファイル追記
        path = Log.__dirname + "/" + datetime.now().strftime("Log_%Y%m%d.txt")
        with open(path, "a") as fp:
            fp.write(line)
            fp.close()
        return

    """ ディレクトリ存在確認 & 作成 """
    def __checkDirectory(self):
        if not isdir(Log.__dirname):
            mkdir(Log.__dirname)  # ディレクトリ作成
        return

