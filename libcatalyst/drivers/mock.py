import json
from .interface import DriverInterface

class MockDriver(DriverInterface):
    def __init__(self, config_file):
        # Load the configuration json file
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def write_spi(self, cs, data, num_bits):
        print(f"SPI Write {cs}: {data:#2x}")

    def read_spi(self, cs, num_bits):
        data = 31
        print(f"SPI Read {cs}: {data:#2x}")
        return data  # Return a mock value

    def exchange_spi(self, cs_name, write_data, write_bits, read_bits):
        print(f"SPI Exchange: {cs} {num_bits} bits: {data}")
        return 0  # Return a mock value

    def set_gpio_direction(self, pin, value):
        #print(f"Mock: Setting GPIO pin {pin} mode to {'output' if value else 'input'}")
        return

    def read_gpio_pin(self, pin):
        print(f"GPIO Read: {pin}")
        return 0  # Return a mock value

    def write_gpio_pin(self, pin_name, value):
        print(f"GPIO Write: {pin}: {value}")

    def get_pin_name(self, pin):
        return self.config[pin]