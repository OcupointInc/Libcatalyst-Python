# rf_digital_attenuator.py
from .interface import DigitalAttenuatorInterface

class HMC1018A(DigitalAttenuatorInterface):
    def __init__(self, spi_interface):
        self.max_attenuation = 31
        self.num_bits = 6
        self.attenuation_steps = 1
        self.spi_interface = spi_interface

    def set_attenuation(self, attenuation):
        if attenuation < 0 or attenuation > self.max_attenuation:
            raise ValueError(f"Attenuation must be between 0 and {self.max_attenuation} dB.")
        
        if attenuation % self.attenuation_steps != 0:
            raise ValueError(f"Attenuation must be a multiple of {self.attenuation_steps} dB.")

        # Generate the SPI word with swapped bits
        spi_word = self.max_attenuation - attenuation

        # Write the SPI word to the digital attenuator
        self.spi_interface.write(spi_word, self.num_bits)

        return spi_word
    
    def read_attenuation(self):
        raise NotImplementedError("This device does not support readback functionality.")
    
