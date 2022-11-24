from machine import Pin
from machine import Timer
from time import sleep_ms
import bluetooth

BLE_MSG = ""


class BLE():
    def __init__(self, name):
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.ble.gatts_write(self.rx, bytes(100))  # 默认接收长度为20字节
        self.advertiser()

    def connected(self):
        self.led.value(1)
        self.timer1.deinit()

    def disconnected(self):
        self.timer1.init(period=100, mode=Timer.PERIODIC,
                         callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        global BLE_MSG
        if event == 1:  # _IRQ_CENTRAL_CONNECT 手机链接了此设备
            self.connected()
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT 手机断开此设备
            self.advertiser()
            self.disconnected()
        elif event == 3:  # _IRQ_GATTS_WRITE 手机发送了数据
            buffer = self.ble.gatts_read(self.rx)
            BLE_MSG = buffer.decode('UTF-8').strip()

    def register(self):
        service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        reader_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        sender_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        services = (
            (
                bluetooth.UUID(service_uuid),
                (
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY),
                    (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
                )
            ),
        )

        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(services)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + \
            bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")


def keyhandle(pin):
    print('(key_boot) Hello, I am esp32')
    ble.send('(key_boot) Hello, I am esp32')


if __name__ == "__main__":
    ble = BLE("ESP32BLE")

    but = Pin(0, Pin.IN)
    but.irq(trigger=Pin.IRQ_FALLING, handler=keyhandle)

    while True:
        if BLE_MSG == 'hi':
            print(BLE_MSG)
            BLE_MSG = ""
            ble.send('Hi, I am esp32')
        sleep_ms(100)
