from machine import Pin, SPI, PWM
import st7789
from uQR import QRCode


# 背光 （PWM调节亮度）
bl = PWM(Pin(4, Pin.OUT))
bl.freq(1000)
bl.duty_u16(16000)


# 屏幕
spi1 = SPI(1, baudrate=40000000)  # mosi=Pin(13),sck=Pin(14)
lcd = st7789.ST7789(
    spi1, 135, 240,
    cs=Pin(15, Pin.OUT),
    reset=Pin(2, Pin.OUT),
    dc=Pin(12, Pin.OUT)
)
lcd.init()
lcd.fill(st7789.RED)


# 二维码

def showQRCode(data, x, y, scale_rate=4):

    # scale_rate 放大倍数

    qr = QRCode(border=2)
    qr.add_data(data)
    matrix = qr.get_matrix()

    row_len = len(matrix)
    col_len = len(matrix[0])

    # 色块 （size=scale_rate*scale_rate）
    buffer_black = bytearray(scale_rate * scale_rate * 2)  # 每个点pixel有2个字节表示颜色
    buffer_white = bytearray(scale_rate * scale_rate * 2)  # 每个点pixel有2个字节表示颜色
    color_black = st7789.BLACK  # 背景色
    color_black_byte1 = color_black & 0xff00 >> 8
    color_black_byte2 = color_black & 0xff
    color_white = st7789.WHITE  # 前景色
    color_white_byte1 = color_white & 0xff00 >> 8
    color_white_byte2 = color_white & 0xff

    for i in range(0, scale_rate * scale_rate * 2, 2):
        buffer_black[i] = color_black_byte1
        buffer_black[i + 1] = color_black_byte2
        buffer_white[i] = color_white_byte1
        buffer_white[i + 1] = color_white_byte2

    for row in range(row_len):
        for col in range(col_len):
            lcd.set_window(x+row*scale_rate, y+col*scale_rate, x+(row+1)
                           * scale_rate-1, y+(col+1)*scale_rate-1)
            lcd.write(None, buffer_white if matrix[row][col] else buffer_black)


showQRCode("我日你爹", 10, 10, 4)
