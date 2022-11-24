from time import sleep
from machine import Pin, SPI, PWM
from st7789 import ST7789
import st7789
import gt20l

# 背光 （PWM调节亮度）
bl = PWM(Pin(4, Pin.OUT))
bl.freq(1000)
bl.duty_u16(16000)
# bl = Pin(4, Pin.OUT)
# bl.value(1)

# 屏幕
spi1 = SPI(1, baudrate=40000000)  # mosi=Pin(13),sck=Pin(14)
lcd = ST7789(
    spi1,
    dc=Pin(12, Pin.OUT),
    cs=Pin(15, Pin.OUT),
    reset=Pin(2, Pin.OUT),
    height=240, width=135,
)
lcd.init()

#################################################

# 字库
spi2 = SPI(2, baudrate=40000000)  # mosi=Pin(23), miso=Pin(19),sck=Pin(18)
font = gt20l.gt20l(spi2, Pin(5, Pin.OUT))


# 字符显示

def showchar_gt20l(x, y, w, h, points, color):
    # points 字符点阵，w 点阵宽，h 点阵高
    for yoffset in range(0, h/8):
        for xoffset in range(w):
            byte = int(points[yoffset*w+xoffset], 16)  # base=16
            for i in range(8):  # one byte
                if (0x1 << i) & byte:
                    lcd.pixel(x + xoffset, y + i, color)
        y += 8  # one byte size


def showchar_816ascll(x, y, ch, color):
    global lcd, font
    c = font.get_816ascll(ch)
    showchar_gt20l(x, y, 8, 16, c, color)


def showstr_816ascll(x, y, s, color):
    for c in s:
        showchar_816ascll(x, y, c, color)
        x += 8  # 字符宽

# GB2312简体中文编码表
# http://tools.jb51.net/table/gb2312
# https://blog.csdn.net/anyuliuxing/article/details/84326207 (推荐)


def showchar_1516gb2312(x, y, ch, color):
    global lcd, font
    c = font.get_gb2312_font(ch)
    showchar_gt20l(x, y, 16, 16, c, color)


def showstr_1516gb2312(x, y, s, color):
    for c in s:
        showchar_1516gb2312(x, y, [c >> 8, c & 0xff], color)
        x += 15  # 字符宽


str_zh = [0xB9FE, 0xE0B6, 0xA3AC, 0xCED2, 0xB2D9, 0xC4E3, 0xC2E8]  # 哈喽，我操你妈


#################################################

lcd.fill(st7789.RED)
showstr_816ascll(30, 80, "hello wrold", st7789.WHITE)
showstr_1516gb2312(10, 120, str_zh, st7789.WHITE)


#################################################

# gif 图

def show_gif(img, cnt, x, y, w, h, speed=0.1):
    with open(img) as f:
        size = w * h * 2  # 单图字节数
        for i in range(cnt):  # 图片数
            f.seek(size*i)  # 设置起始读取位置
            buffer = f.read(size)
            lcd.set_window(x, y, x+w-1, y+h-1)
            lcd.write(None, buffer)
            sleep(speed)  # 播放速度(值越小速度越快)


for i in range(8):
    show_gif('img.dat', 13, 10, 10, 60, 60)

print("ok")
