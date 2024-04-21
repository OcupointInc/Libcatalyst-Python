from abc import ABC, abstractmethod

# SPI Interface
class SPIInterface(ABC):
    @abstractmethod
    def write(self, data, num_bits):
        pass

    @abstractmethod
    def read(self, num_bits):
        pass

# GPIO Interface
class GPIOInterface(ABC):
    @abstractmethod
    def set_pin(self, pin, value):
        pass

    @abstractmethod
    def read_pin(self, pin):
        pass