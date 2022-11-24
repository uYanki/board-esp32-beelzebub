import os
import struct
import numpy as np
from PIL import Image  # pillow

os.chdir('./gif 60x60/')  # 设置工作目录


def color565(r, g, b):  # 转两字节颜色值
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


with open('img.dat', 'wb') as f:
    for file in os.listdir('./'):
        if file.startswith('img') and file.endswith('.jpg'):
            img = Image.open(file)
            print(img.format, img.size, img.mode)
            for line in np.array(img):  # w*h*3
                for dot in line:
                    f.write(struct.pack("H", color565(*dot))[::-1])
            print(f.tell())
