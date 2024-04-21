# spidev_driver.py
import spidev
from drivers import DriverInterface

class SPIDevDriver(DriverInterface):
    def __init__(self):
        self.spi = spidev.SpiDev()

    def open(self, bus, device):
        self.spi.open(bus, device)

    def close(self):
        self.spi.close()

    def read(self, length):
        return self.spi.readbytes(length)

    def write(self, data):
        self.spi.writebytes(data)