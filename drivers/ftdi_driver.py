# ftdi_driver.py
from ftdi import FtdiSPI
from drivers import DriverInterface

class FTDIDriver(DriverInterface):
    def __init__(self):
        self.ftdi = FtdiSPI()

    def open(self, bus, device):
        self.ftdi.open(bus, device)

    def close(self):
        self.ftdi.close()

    def read(self, length):
        return self.ftdi.read(length)

    def write(self, data):
        self.ftdi.write(data)