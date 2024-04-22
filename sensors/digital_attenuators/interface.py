from abc import ABC, abstractmethod

class DigitalAttenuatorInterface(ABC):
    @abstractmethod
    def set_attenuation_db(self, attenuation):
        """
        Set the attenuation of the digital attenuator.
        """
        pass

    # Generate the SPI word with swapped bits
    def read_attenuation_db(self):
        """
        Read the attenuation of the digital attenuator.
        """
        pass