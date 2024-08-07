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
    def __init__(self, config_file, freq=1E7, id="ftdi://ftdi:ft232h/1", debug=False):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        # Initialize the FTDI device in MPSSE mode
        self.ftdi = Ftdi()
        self.debug = debug
        self.ftdi.open_mpsse(vendor=0x0403, product=0x6014, direction=0x0, initial=0x0)
        self.gpio = GpioMpsseController()
        self.freq = freq

        direction = 0xFFFF

        # Make any miso pins an input
        for key in self.config:
            if "miso" in key.lower():
                pin = pin_map[self._get_pin(key)]
                mask = ~(1 << pin)
                direction = direction & mask

        self.gpio.configure(id, direction=direction, frequency=freq)

        # Set all of the pins to be high by default except the clock pin (idle low)
        self.current_state = 0xFFFF & ~create_bit_mask("D0")
        self.current_state = 0x0000
        self.gpio.write(self.current_state)

        # Calculate delay for SPI clock
        self.half_period = 0

    def _get_pin(self, pin):
        return self.config[pin]
    
    def read_spi(self, cs, num_bits):
        raise NotImplementedError("This device does not support read SPI functionality.")
    
    def _int_to_bits(self, num, length):
        # Convert integer to binary string, remove the '0b' prefix, and pad with leading zeros
        binary_string = format(num, f'0{length}b')
        # Convert binary string to a list of integers
        bits_list = [int(bit) for bit in binary_string]
        return bits_list
    
    def _int_to_hex_string(self,num, length):
        # Calculate the number of hex digits needed for the specified bit length
        hex_length = (length + 3) // 4  # Each hex digit represents 4 bits
        # Convert integer to hexadecimal string and pad with leading zeros
        return "0x" + format(num, f'0{hex_length}x').upper()

    def write_spi(self, cs, data, num_bits):
        sclk_pin = "D0"
        mosi_pin = "D1"
        cs_pin = self._get_pin(cs)

        sclk_mask = create_bit_mask(sclk_pin)
        mosi_mask = create_bit_mask(mosi_pin)
        cs_mask = create_bit_mask(cs_pin)

        # Ensure SCLK and MOSI are low before starting
        self.current_state &= ~(sclk_mask)
        self.current_state &= ~(mosi_mask)
        self.gpio.write(self.current_state)

        # Activate chip select (CS low)
        self.current_state &= ~cs_mask
        self.gpio.write(self.current_state)

        bits = self._int_to_bits(data, num_bits)

        if self.debug:
            print(self._int_to_hex_string(data, num_bits))

        for bit in bits:
            # Set MOSI
            if bit:
                self.current_state |= mosi_mask
            else:
                self.current_state &= ~mosi_mask
            
            # Write MOSI state (clock is already low)
            self.gpio.write(self.current_state)

            # Clock high
            self.current_state |= sclk_mask
            self.gpio.write(self.current_state)

            # Clock low again (back to idle state)
            self.current_state &= ~sclk_mask
            self.gpio.write(self.current_state)

        # Deactivate chip select (CS high)
        self.current_state |= cs_mask
        self.gpio.write(self.current_state)

        # Reset MOSI and SCLK to low after transmission
        self.current_state &= ~(sclk_mask)
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
        pin_state = self.gpio.read()[0] & mask
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
