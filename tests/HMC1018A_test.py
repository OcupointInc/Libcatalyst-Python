import unittest
from unittest.mock import Mock
from sensors.digital_attenuators.HMC1018A import HMC1018A

class TestHMC1018A(unittest.TestCase):
    def setUp(self):
        # Create a mock SPI interface and pass it to the HMC1018A initializer
        self.mock_spi_interface = Mock()
        self.attenuator = HMC1018A(self.mock_spi_interface, "attenuator_cs")

    def test_set_attenuation_db_invalid_input(self):
        # Test invalid attenuation values
        invalid_values = [-1, 32, 100]
        for value in invalid_values:
            with self.assertRaises(ValueError):
                self.attenuator.set_attenuation_db(value)

    def test_set_attenuation_db_valid_input(self):
        # Test cases with predefined attenuation values and their expected binary SPI outputs
        test_cases = [
            (0, 0b011111),   # 31 - 0 = 31 (binary: 011111)
            (15, 0b010000),  # 31 - 15 = 16 (binary: 010000)
            (31, 0b000000)   # 31 - 31 = 0 (binary: 000000)
        ]
        for attenuation, expected_spi_word in test_cases:
            spi_word = self.attenuator.set_attenuation_db(attenuation)
            self.assertEqual(spi_word, expected_spi_word)
            self.mock_spi_interface.write_spi.assert_called_with("attenuator_cs", expected_spi_word, self.attenuator.num_bits)

    def test_read_attenuation_db_not_implemented(self):
        # Ensure the read_attenuation_db method raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.attenuator.read_attenuation_db()

if __name__ == '__main__':
    unittest.main()
