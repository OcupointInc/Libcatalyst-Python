# ADRF5720.py
from .interface import DigitalAttenuatorInterface

class ADRF5720(DigitalAttenuatorInterface):
    def __init__(self, driver, cs):
        self.max_attenuation = 31.5
        self.num_bits = 8
        self.attenuation_steps = 0.5
        self.driver = driver
        self.cs = cs

    def set_attenuation_db(self, attenuation):
        if attenuation < 0 or attenuation > self.max_attenuation:
            raise ValueError(f"Attenuation must be between 0 and {self.max_attenuation} dB.")
        
        if attenuation % self.attenuation_steps != 0:
            raise ValueError(f"Attenuation must be a multiple of {self.attenuation_steps} dB.")

        # Generate the SPI word with swapped bits
        spi_word = int(attenuation / self.attenuation_steps)

        # Write the SPI word to the digital attenuator
        self.driver.write_spi(self.cs, spi_word, self.num_bits)

        return spi_word
    
    def read_attenuation_db(self):
        # Read the SPI word from the digital attenuator
        spi_word = self.driver.read_spi(self.cs, self.num_bits)

        # Calculate the attenuation from the SPI word
        attenuation = spi_word * self.attenuation_steps
        return attenuation
    
