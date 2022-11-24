import time
import network
from umqttsimple import MQTTClient


def connectWifi(ssid, pwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to wifi...')
        wlan.connect(ssid, pwd)
        i = 1
        while not wlan.isconnected():
            print("connecting...{}".format(i))
            i += 1
            sleep(1)
    print('network config:', wlan.ifconfig())
    return wlan.ifconfig()[0]  # return ip


def sub_cb(topic, msg):  # 回调函数，收到服务器消息后会调用这个函数
    print(topic, msg)


connectWifi('jia1', '58138221')
mqtt = MQTTClient("esp32", "192.168.1.71")
mqtt.set_callback(sub_cb)  # 消息回调函数
mqtt.connect()  # 建立连接
mqtt.subscribe(b"LED")  # 订阅主题
while True:
    mqtt.check_msg()
    time.sleep(1)
