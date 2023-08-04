import network
import espnow
import time

BROADCAST_MAC = b'\xff\xff\xff\xff\xff\xff'

wlan = network.WLAN(network.STA_IF)
print("receiver MAC:", wlan.config('mac'))
wlan.active(True)
wlan.disconnect()

e = espnow.ESPNow()
e.active(True)
# sender mac
peer = BROADCAST_MAC
# peer = b'\x9c\x9c\x1f\x1aD\xf8'
e.add_peer(peer)


while True:
    # recv msg
    host, msg = e.recv()
    if msg:
        print("Sender MAC>", host, "CMD>", msg)
        # send msg
        e.send(peer, b'I am receiver', True)
