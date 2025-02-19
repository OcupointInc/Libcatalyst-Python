from unittest.mock import Mock
import pytest
from sensors.digital_attenuators.ADRF5720 import ADRF5720

class TestADRF5720:
    def setup_method(self):
        # Create a mock SPI interface and inject it into the ADRF5720 instance
        self.driver = Mock()
        self.attenuator = ADRF5720(self.driver, "attenuator_cs")

    def test_set_attenuation_db_invalid_range(self):
        # Test attenuation values that are out of the acceptable range
        with pytest.raises(ValueError):
            self.attenuator.set_attenuation_db(-0.5)
        with pytest.raises(ValueError):
            self.attenuator.set_attenuation_db(32)

    def test_set_attenuation_db_invalid_step(self):
        # Test attenuation values that are not multiples of the step size
        invalid_values = [0.3, 31.2]
        for value in invalid_values:
            with pytest.raises(ValueError):
                self.attenuator.set_attenuation_db(value)

    def test_set_attenuation_db_valid(self):
        # Test valid attenuation settings and ensure correct SPI word calculation
        test_cases = [
            (0, 0),       # Minimum attenuation
            (15.5, 31),   # Mid-range attenuation
            (31.5, 63)    # Maximum attenuation
        ]
        for attenuation, expected_spi_word in test_cases:
            spi_word = self.attenuator.set_attenuation_db(attenuation)
            assert spi_word == expected_spi_word
            self.driver.write_spi.assert_called_with("attenuator_cs", expected_spi_word, self.attenuator.num_bits)

    def test_read_attenuation_db(self):
        # Mocking the read method to simulate reading an SPI word from hardware
        self.driver.read_spi.return_value = 31  # Mid-range SPI word
        attenuation = self.attenuator.read_attenuation_db()
        expected_attenuation = 31 * self.attenuator.attenuation_steps
        assert attenuation == expected_attenuation
        