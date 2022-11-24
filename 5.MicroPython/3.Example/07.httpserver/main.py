import network
from time import sleep
import socket
import re
from machine import Pin
from neopixel import NeoPixel

rgb = Pin(9, Pin.OUT)
np = NeoPixel(rgb, n=2, bpp=3, timing=1)


def rgbled(state):
    global np
    if state:
        np[0] = (2, 2, 2)
        np[1] = (2, 2, 2)
    else:
        np[0] = (0, 0, 0)
        np[1] = (0, 0, 0)
    np.write()


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


def handle200(content):
    headers = "HTTP/1.1 200 OK\r\n"
    headers += "Connection: close\r\n"
    headers += "Content-Type:text/html;charset=utf-8\r\n"
    headers += "\r\n"
    response = (headers + content).encode("utf-8")  # 响应体
    return response


def handle404(content='404: The requested URL was not found on this server.'):
    # 页面不存在,返回 404
    headers = "HTTP/1.1 404 Not Found\r\n"
    headers += "Connection: close\r\n"
    headers += "Content-Type:text/html;charset=utf-8\r\n"
    headers += "\r\n"
    response = (headers + content).encode("utf-8")


def handleRequest(socket):
    content = socket.recv(1024).decode("utf-8")
    print(content)
    lines = content.splitlines()
    # 处理请求
    url = re.match(r"[^/]+(/[^ ]*)", lines[0]).group(1)  # 提取路由
    print(url)

    response = ''  # 响应体
    filepath = ''
    if url == '/' or url == '/index' or url == '/index/':
        filepath = 'index.html'
    elif url == '/ledstate_on':
        rgbled(True)
        response = handle200('success')
    elif url == '/ledstate_off':
        rgbled(False)
        response = handle200('success')

    if response == '':
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                headers = "HTTP/1.1 200 OK\r\n"
                headers += "Connection: close\r\n"
                headers += "Content-Type:text/html;charset=utf-8\r\n"
                headers += "\r\n"
                response = headers.encode("utf-8") + content  # 注意编码
        except Exception as e:
            handle404()

    socket.send(response)
    socket.close()


def listenPort(port):
    tcpser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpser.bind(("", port))
    tcpser.listen(128)
    while True:
        cli_socket, cli_info = tcpser.accept()
        print(cli_info)
        try:
            handleRequest(cli_socket)
        except Exception as e:
            print('error', e)
    tcpser.close()


if __name__ == "__main__":
    port = 80
    ip = connectWifi('jia1', '58138221')
    print(f'http://{ip}:{port}')
    listenPort(port)
