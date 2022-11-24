
import network
from machine import Pin
import urequests
from utime import sleep, localtime
import ujson


def fromNumToStr(n):  # 补零直到两位字符
    result = str(n)
    if len(result) < 2:
        result = "0"+result
    return result


def fromTurpleToTimeStr(tup):
    return (str(tup[0]-30)+"-"+fromNumToStr(tup[1])+"-"+fromNumToStr(tup[2]),
            fromNumToStr(tup[3]+8)+":"+fromNumToStr(tup[4])+":"+fromNumToStr(tup[5]))


# 连接WiFi
station = network.WLAN(network.STA_IF)
while (not station.isconnected()):
    station.active(True)
    try:
        station.connect("HUAWEI-Y6AZGD", "password")  # ssid 和 pwd
        sleep(5.0)
    except OSError:
        print("OSError")
        sleep(2.0)


response = urequests.get(
    "http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp"
)  # 获取时间戳JSON
timeStamp = ujson.loads(response.text)["data"]["t"]
timeStamp = int(timeStamp[:-3])  # 后3位是毫秒, 舍去掉
timeTup = localtime(timeStamp)  # 数字转时间元组
timeNr = fromTurpleToTimeStr(timeTup)  # 时间元组转字符串

print(timeNr)
