import network
import espnow
import time

BROADCAST_MAC = b'\xff\xff\xff\xff\xff\xff'

wlan = network.WLAN(network.STA_IF)
print("sender Mac:", wlan.config('mac'))
wlan.active(True)
wlan.disconnect()

e = espnow.ESPNow()
e.active(True)
# receiver mac list
peerList = [BROADCAST_MAC]  # [b'$\xd7\xebi\xaa\x08', ...]
for peer in peerList:
    e.add_peer(peer)

while True:
    # send
    cmd = "hello, i am sender"
    for peer in peerList:
        e.send(peer, cmd, True)
    print("TX>", cmd)

    # recv
    _, msg = e.recv()
    while not msg:
        _, msg = e.recv()
    print("RX>", msg)

    time.sleep(2)
