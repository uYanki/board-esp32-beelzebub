import mpu6050
import time
import math
from machine import I2C, Pin


class mpu6050dmp:
    # 测试偏差 yaw  pitch  roll用于归零
    def __init__(self, i2c, bias=(- 115, - 5.5, 1.5)):
        self.mpu = mpu6050.MPU6050(i2c)
        self.mpu.dmpInitialize()
        self.mpu.setDMPEnabled(True)
        self.packetSize = self.mpu.dmpGetFIFOPacketSize()
        self.bias = bias

    def Wait4Ypr(self):
        while self.mpu.getIntStatus() < 2:
            time.sleep_ms(10)  # check for DMP data ready interrupt (this should happen frequently)
            # get current FIFO count
        fifoCount = self.mpu.getFIFOCount()

        # check for overflow (this should never happen unless our code is too inefficient)
        if fifoCount == 1024:
            # reset so we can continue cleanly
            self.mpu.resetFIFO()
            print('FIFO overflow!')

        # wait for correct available data length, should be a VERY short wait
        fifoCount = self.mpu.getFIFOCount()
        while fifoCount < self.packetSize:
            fifoCount = self.mpu.getFIFOCount()

        result = self.mpu.getFIFOBytes(self.packetSize)
        q = self.mpu.dmpGetQuaternion(result)
        g = self.mpu.dmpGetGravity(q)
        ypr = self.mpu.dmpGetYawPitchRoll(q, g)
        ypr = (ypr['yaw'] * 180 / math.pi + self.bias[0], ypr['pitch'] * 180 / math.pi + self.bias[1], ypr['roll'] * 180 / math.pi + self.bias[2])
        print('yaw', ypr[0], end=' ')
        print('pitch', ypr[1], end=' ')
        print('roll', ypr[2])
        return ypr
        # track FIFO count here in case there is > 1 packet available
        # (this lets us immediately read more without waiting for an interrupt)
        # fifoCount -= packetSize
