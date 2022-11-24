from socket import *
import network
from time import sleep

print("start")
# create station interface
wlan = network.WLAN(network.STA_IF)
# activate the interface
wlan.active(True)
# scan for access points
print(wlan.scan())
# check if the station is connected to an AP
if not wlan.isconnected():
    # connect to an AP
    wlan.connect("jia1", "58138221")
    while not wlan.isconnected():
        sleep(1)
    # get the interface's MAC address
    print(wlan.config('mac'))
    # get the interface's IP/netmask/gw/DNS addresses (IP/子网掩码/网关/DNS)
    print(wlan.ifconfig())

if wlan.isconnected():
    # udp socket
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    dest_addr = ('192.168.1.71', 6001)  # pc ip & port
    # send
    send_data = "hello world\r\n"
    udp_socket.sendto(send_data.encode('utf-8'), dest_addr)
    # recv
    print("wait for data to arrive")
    data = udp_socket.recv(10)
    if data:
        udp_socket.sendto(data, dest_addr)
        print(str(data, 'utf8'), end='')
    udp_socket.close()

print("OK")
