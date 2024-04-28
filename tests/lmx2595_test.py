import unittest
from unittest.mock import Mock
from sensors.pll.LMX2595 import LMX2595

class TestLmx2595(unittest.TestCase):
    def setUp(self):
        # Create a mock SPI interface and pass it to the HMC1018A initializer
        self.mock_driver = Mock()
        self.attenuator = LMX2595(self.mock_driver, "CS")

    def test_tune_pll(self):
        # Test pll frequencies
        test_cases = [
            (10000, 0b011111),   # 31 - 0 = 31 (binary: 011111)
            (12000, 0b010000),  # 31 - 15 = 16 (binary: 010000)
            (14000, 0b000000)   # 31 - 31 = 0 (binary: 000000)
        ]
        for attenuation, expected_spi_word in test_cases:
            spi_word = self.attenuator.set_attenuation_db(attenuation)
            self.assertEqual(spi_word, expected_spi_word)
            self.mock_driver.write_spi.assert_called_with("CS", expected_spi_word, self.attenuator.num_bits)

if __name__ == '__main__':
    unittest.main()
