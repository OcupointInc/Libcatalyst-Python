# sensor_base.py
from abc import ABC, abstractmethod

class SensorBase(ABC):
    def __init__(self, spi_interface):
        self.spi = spi_interface

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_command(self, command):
        pass

    @abstractmethod
    def configure(self):
        pass

    def close(self):
        self.spi.close()