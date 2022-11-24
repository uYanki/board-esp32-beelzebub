from mpu6050dmp import mpu6050dmp
from machine import SoftI2C, I2C, Pin

i2c = SoftI2C(scl=Pin(2), sda=Pin(3), freq=400000)
print(i2c.scan())
try:
    # get expected DMP packet size for later comparison
    mpu = mpu6050dmp(i2c, bias=(- 112, -5.5, 1.4))
    while True:
        mpu.Wait4Ypr()  # 等待四元数
except Exception as e:
    print(e)
