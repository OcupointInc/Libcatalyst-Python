# ftdi_driver.py
from pyftdi.spi import SpiController
from pyftdi.gpio import GpioController
from .interface import DriverInterface

class FTDISPIDriver(DriverInterface):
    def __init__(self, freq=1E6, id="ftdi://ftdi:ft232h/1"):
        self.spi = SpiController()
        self.gpio = GpioController()
        self.freq = freq
        self.spi.configure(id)
        self.gpio.open_from_url(id)
        self.slave = self.spi.get_port(cs=0, freq=self.freq, mode=0)
        
        # Map the chip selects to the corresponding GPIO pins
        self.cs_pins = {
            'D3': 3,   # CS0 = D3
            'D4': 4,   # CS1 = D4
            'D5': 5,   # CS2 = D5
            'D6': 6,   # CS3 = D6
            'D7': 7,   # CS4 = D7
            'C0': 8,   # CS5 = C0
            'C1': 9,   # CS6 = C1
            'C2': 10,  # CS7 = C2
            'C3': 11,  # CS8 = C3
            'C4': 12,  # CS9 = C4
            'C5': 13,  # CS10 = C5
            'C6': 14,  # CS11 = C6
            'C7': 15   # CS12 = C7
        }
        
        # Configure the additional chip select pins as outputs
        for cs, pin in self.cs_pins.items():
            if cs >= 5:
                self.gpio.set_direction(pin, 0x01)
        
        # Create a dictionary to store the slave objects
        self.slaves = {}
        
        # Initialize the slave objects for each chip select
        for cs, pin in self.cs_pins.items():
            if cs < 5:
                self.slaves[cs] = self.spi.get_port(cs=pin, freq=self.freq, mode=0)
            else:
                self.slaves[cs] = self.spi.get_port(cs=0, freq=self.freq, mode=0)
    
    def _select_slave(self, cs):
        if cs not in self.slaves:
            raise ValueError(f"Invalid chip select: {cs}")
        if cs >= 5:
            self.gpio.write(self.cs_pins[cs], 0)
    
    def _deselect_slave(self, cs):
        if cs not in self.slaves:
            raise ValueError(f"Invalid chip select: {cs}")
        if cs >= 5:
            self.gpio.write(self.cs_pins[cs], 1)
    
    def read_spi(self, cs, num_bits):
        if cs not in self.slaves:
            raise ValueError(f"Invalid chip select: {cs}")
        self._select_slave(cs)
        data = self.slaves[cs].read(num_bits)
        self._deselect_slave(cs)
        return data
    
    def write_spi(self, cs, data, num_bits):
        if cs not in self.slaves:
            raise ValueError(f"Invalid chip select: {cs}")
        self._select_slave(cs)
        self.slaves[cs].write(data)
        self._deselect_slave(cs)
    
    def exchange_spi(self, cs, data, num_bits):
        if cs not in self.slaves:
            raise ValueError(f"Invalid chip select: {cs}")
        self._select_slave(cs)
        result = self.slaves[cs].exchange(data)
        self._deselect_slave(cs)
        return result
    
    def set_gpio_mode(self, pin, value):
        raise NotImplementedError("This device does not support write functionality.")

    def read_gpio_pin(self, pin):
        raise NotImplementedError("This device does not support write functionality.")
    
    def write_gpio_pin(self, pin, value):
        raise NotImplementedError("This device does not support write functionality.")