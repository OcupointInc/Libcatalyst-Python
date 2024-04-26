import json
import RPi.GPIO as GPIO
import time

from .interface import DriverInterface

class RaspberryPiDriver(DriverInterface):
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        GPIO.setmode(GPIO.BCM)

    def _get_pin_number(self, name):
        pin_string = self.config.get(name, -1)
        if pin_string.startswith("GPIO") and pin_string[4:].isdigit():
            return int(pin_string[4:])

    def write_spi(self, cs_name, data, num_bits):
        MOSI = self._get_pin_number("MOSI")
        SCLK = self._get_pin_number("SCLK")
        CS = self._get_pin_number(cs_name)
        if CS == -1:
            print(f"Error: No pin configured for {cs_name}")
            return

        GPIO.setup(MOSI, GPIO.OUT)
        GPIO.setup(SCLK, GPIO.OUT)
        GPIO.setup(CS, GPIO.OUT)

        GPIO.output(CS, GPIO.HIGH)
        GPIO.output(SCLK, GPIO.LOW)

        GPIO.output(CS, GPIO.LOW)  # Activate the CS line to start the transaction
        for i in range(num_bits):
            bit_pos = num_bits - 1 - i
            GPIO.output(MOSI, (data >> bit_pos) & 0x1)
            GPIO.output(SCLK, GPIO.HIGH)
            GPIO.output(SCLK, GPIO.LOW)
        GPIO.output(CS, GPIO.HIGH)  # Deactivate CS to end the transaction

        hex_width = (num_bits + 3) // 4  # Calculate the necessary width of the hexadecimal output
        data_format = f"0{hex_width}x"  # Format string for hexadecimal width
        print(f"SPI Write {cs_name} (GPIO{CS}): 0x{format(data, data_format)}")  # Print using the dynamic format


    def read_spi(self, cs_name, num_bits):
        # This method can be similarly implemented using GPIO for bit-banging read
        # SPI reads are usually not implemented this way, as they require capturing data from MISO during clock edges
        pass

    def exchange_spi(self, cs_name, data, num_bits):
        # Implement if you need bi-directional communication, similar to write_spi but also reading from MISO
        pass

    def set_gpio_direction(self, pin_name, value):
        pin = self._get_pin_number(pin_name)
        GPIO.setup(pin, GPIO.OUT if value else GPIO.IN)
        print(f"Setting GPIO pin {pin} mode to {'output' if value else 'input'}")

    def read_gpio_pin(self, pin_name):
        pin = self._get_pin_number(pin_name)
        GPIO.setup(pin, GPIO.IN)
        state = GPIO.input(pin)
        print(f"GPIO Read: {pin}: {state}")
        return state

    def write_gpio_pin(self, pin_name, value):
        pin = self._get_pin_number(pin_name)
        GPIO.output(pin, value)
        print(f"GPIO Write: {pin}: {value}")