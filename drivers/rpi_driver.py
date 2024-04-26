import json
import RPi.GPIO as GPIO
import spidev

from .interface import DriverInterface

class RaspberryPiDriver(DriverInterface):
    def __init__(self, id, config_file):
        # Load the configuration json file
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.spi = spidev.SpiDev()  # Create a SPI device instance
        self.id = id
        GPIO.setmode(GPIO.BCM)

    def _get_pin_number(self, name):
        """ Helper method to translate pin names to pin numbers. """
        # Retrieve the pin name string from the configuration
        pin_string = self.config.get(name, -1)  # Return -1 if name is not found
        if pin_string.startswith("GPIO") and pin_string[4:].isdigit():
            # Extract and return the integer part after "GPIO"
            return int(pin_string[4:])

    def write_spi(self, cs_name, data, num_bits):
        cs = self._get_pin_number(cs_name)
        if cs == -1:
            print(f"Error: No pin configured for {cs_name}")
            return
        
        GPIO.setup(cs, GPIO.OUT)
        GPIO.output(cs, GPIO.LOW)  # Select the device
        self.spi.open(0, 0)  # Open SPI bus 0, device 0 (adjust as necessary)
        self.spi.max_speed_hz = 500000  # Set SPI speed
        self.spi.mode = 0  # SPI mode
        self.spi.writebytes([data])  # Send data
        GPIO.output(cs, GPIO.HIGH)  # Deselect the device
        print(f"SPI Write {cs_name} (GPIO {cs}): {data:#2x}")

    def read_spi(self, cs_name, num_bits):
        cs = self._get_pin_number(cs_name)
        if cs == -1:
            print(f"Error: No pin configured for {cs_name}")
            return 0
        
        GPIO.setup(cs, GPIO.OUT)
        GPIO.output(cs, GPIO.LOW)  # Select the device
        response = self.spi.readbytes(1)  # Read one byte
        GPIO.output(cs, GPIO.HIGH)  # Deselect the device
        data = response[0]
        print(f"SPI Read {cs_name} (GPIO {cs}): {data:#2x}")
        return data

    def exchange_spi(self, cs_name, data, num_bits):
        cs = self._get_pin_number(cs_name)
        if cs == -1:
            print(f"Error: No pin configured for {cs_name}")
            return 0
        
        GPIO.setup(cs, GPIO.OUT)
        GPIO.output(cs, GPIO.LOW)
        response = self.spi.xfer2([data])  # Exchange data
        GPIO.output(cs, GPIO.HIGH)
        print(f"SPI Exchange {cs_name} (GPIO {cs}) {num_bits} bits: {data}")
        return response[0]

    def set_gpio_direction(self, pin_name, value):
        pin = self._get_pin_number(pin_name)
        GPIO.setup(pin, GPIO.OUT if value else GPIO.IN)
        print(f"Setting GPIO pin {pin} mode to {'output' if value else 'input'}")

    def read_gpio_pin(self, pin_name):
        pin = self._get_pin_number(pin_name)
        state = GPIO.input(pin)
        print(f"GPIO Read: {pin}: {state}")
        return state

    def write_gpio_pin(self, pin_name, value):
        pin = self._get_pin_number(pin_name)
        GPIO.output(pin, value)
        print(f"GPIO Write: {pin}: {value}")

    def get_pin_name(self, pin_name):
        # Retrieve the pin name string from the configuration
        pin_string = self.config.get("pin_names", {}).get(pin_name, "Unknown")
        if pin_string.startswith("GPIO") and pin_string[4:].isdigit():
            # Extract and return the integer part after "GPIO"
            return int(pin_string[4:])
        #return "Unknown"  # Return "Unknown" if the format is incorrect or the pin is not found
