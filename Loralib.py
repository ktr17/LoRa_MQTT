# -*- coding: utf-8 -*-

class Loralib():
    def extractionData(data="", target="srcid"):
        # データがNULLのときは終了
        extractionValue = ""
        if not data:
            Lora.log.add("受信データの破損が疑われます.", "DEBUG")
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
    
        print(extractionValue)
        return extractionValue
