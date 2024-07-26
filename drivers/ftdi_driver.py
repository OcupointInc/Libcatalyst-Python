# ftdi_driver.py
from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioMpsseController
from .interface import DriverInterface
import json
import time

# Define the pin mappings
pin_map = {
    'D0': 0, 'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5, 'D6': 6, 'D7': 7,
    'C0': 8, 'C1': 9, 'C2': 10, 'C3': 11, 'C4': 12, 'C5': 13, 'C6': 14, 'C7': 15
}

def create_bit_mask(pin_name):
    # Check if the pin name is valid
    if pin_name not in pin_map:
        raise ValueError(f"Invalid pin name: {pin_name}")
    
    # Create the bit mask
    mask = 1 << pin_map[pin_name]
    
    return mask

class FTDISPIDriver(DriverInterface):
    def __init__(self, config_file, freq=1E6, id="ftdi://ftdi:ft232h/1"):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        # Initialize the FTDI device in MPSSE mode
        self.ftdi = Ftdi()
        self.ftdi.open_mpsse(vendor=0x0403, product=0x6014)
        self.gpio = GpioMpsseController()
        self.freq = freq
        self.gpio.configure(id, direction=0xFFFF, frequency=freq)

        # Set all of the pins to be high by default and store the state
        self.current_state = 0xFFFF
        self.gpio.write(self.current_state)

        # Calculate delay for SPI clock
        self.half_period = 1 / (2 * freq)

    def _get_pin(self, pin):
        return self.config[pin]
    
    def read_spi(self, cs, num_bits):
        raise NotImplementedError("This device does not support read SPI functionality.")
    
    def write_spi(self, cs, data, num_bits):
        sclk_pin = self._get_pin("SCLK")
        mosi_pin = self._get_pin("MOSI")
        cs_pin = self._get_pin(cs)

        sclk_mask = create_bit_mask(sclk_pin)
        mosi_mask = create_bit_mask(mosi_pin)
        cs_mask = create_bit_mask(cs_pin)

        # Activate chip select (CS low)
        self.current_state &= ~cs_mask
        self.gpio.write(self.current_state)

        for byte in data:
            for i in range(8):  # Assuming 8 bits per byte
                # Set MOSI
                if byte & (0x80 >> i):
                    self.current_state |= mosi_mask
                else:
                    self.current_state &= ~mosi_mask
                
                # Clock low
                self.current_state &= ~sclk_mask
                self.gpio.write(self.current_state)
                time.sleep(self.half_period)

                # Clock high
                self.current_state |= sclk_mask
                self.gpio.write(self.current_state)
                time.sleep(self.half_period)

        # Deactivate chip select (CS high)
        self.current_state |= cs_mask
        self.gpio.write(self.current_state)
    
    def exchange_spi(self, cs, data, num_bits):
        raise NotImplementedError("This device does not support exchange SPI functionality.")

    def set_gpio_direction(self, pin, value):
        mask = create_bit_mask(self._get_pin(pin))
        if value:
            new_direction = self.gpio.direction | mask
        else:
            new_direction = self.gpio.direction & ~mask
        self.gpio.set_direction(mask, new_direction)

    def read_gpio_pin(self, pin):
        mask = create_bit_mask(self._get_pin(pin))
        pin_state = self.gpio.read() & mask
        return bool(pin_state)
    
    def write_gpio_pin(self, pin, value):
        mask = create_bit_mask(self._get_pin(pin))
        if value:
            self.current_state |= mask
        else:
            self.current_state &= ~mask
        self.gpio.write(self.current_state)

    def close(self):
        self.gpio.close()
        self.ftdi.close()