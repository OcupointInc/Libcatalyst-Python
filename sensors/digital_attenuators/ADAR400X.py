# ADRF5720.py
from .interface import DigitalAttenuatorInterface

class ADAR400X(DigitalAttenuatorInterface):
    def __init__(self, driver, cs, hardware_address):
        self.max_attenuation = 31
        self.num_bits = 16
        self.attenuation_steps = 1
        self.driver = driver
        self.cs = cs
        self.hardware_address = hardware_address

        self.setup()


    def setup(self):
        self._soft_reset()
        self._soft_reset()
        self._set_direct_control()

    def _set_direct_control(self):
        addr = 0x011
        data = 0x00
        spi_word = (addr << 8) | data
        self.driver.write_spi(self.cs, spi_word, self.num_bits)

    def _soft_reset(self):
        addr = 0x000
        data = 0xBD
        spi_word = (addr << 8) | data

        self.driver.write_spi(self.cs, spi_word, self.num_bits)

    def set_attenuation_db(self, channel, data):
        if channel < 0 or channel > 3:
            raise ValueError(f"Channel must be between 0 and 3.")
        
        if data < 0 or data > self.max_attenuation:
            raise ValueError(f"Attenuation must be between 0 and {self.max_attenuation} dB.")
        
        if data % self.attenuation_steps != 0:
            raise ValueError(f"Attenuation must be a multiple of {self.attenuation_steps} dB.")

        # Generate the SPI word with swapped bits
        addr = 0x101 + channel * 2

        spi_word = (addr << 8) | data

        return spi_word
    
    def read_attenuation_db(self):
        # Read the SPI word from the digital attenuator
        spi_word = self.driver.read_spi(self.cs, self.num_bits)

        # Calculate the attenuation from the SPI word
        attenuation = spi_word * self.attenuation_steps
        return attenuation
    
    def set_time_delay(self, channel, data):
        """
        Set the time delay of the digital attenuator.
        """
        if channel < 0 or channel > 3:
            raise ValueError(f"Channel must be between 0 and 3.")
        
        if data < 0 or data > 255:
            raise ValueError(f"Time delay must be between 0 and 255.")
        
        # Get the register 0x100, 0x102, 0x104, 0x106
        addr = 0x100 + channel * 2

        spi_word = (addr << 8) | data
        
        # Write the SPI word to the digital attenuator
        self.driver.write_spi(self.cs, spi_word, self.num_bits)
        
        return spi_word
    
