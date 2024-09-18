import unittest
from unittest.mock import Mock
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from sensors.pll.LMX2595 import LMX2595

class TestLmx2595(unittest.TestCase):
    def setUp(self):
        self.mock_driver = Mock()
        self.pll = LMX2595(self.mock_driver, "CS")

    def test_tune_pll(self):
        test_cases = [
            (10000, [0x700000,0x6F0000,0x6E0000,0x6D0000,0x6C0000,0x6B0000,0x6A0000,0x690021,0x680000,0x670000,0x663F80,0x650011,0x640000,0x630000,0x620200,0x610888,0x600000,0x5F0000,0x5E0000,0x5D0000,0x5C0000,0x5B0000,0x5A0000,0x590000,0x580000,0x570000,0x560000,0x55E700,0x540001,0x530000,0x523200,0x510000,0x506666,0x4F0026,0x4E0003,0x4D0000,0x4C000C,0x4B0800,0x4A0000,0x49003F,0x480001,0x470081,0x46C350,0x450000,0x4403E8,0x430000,0x4201F4,0x410000,0x401388,0x3F0000,0x3E0322,0x3D00A8,0x3C0000,0x3B0001,0x3A9001,0x390020,0x380000,0x370000,0x360000,0x350000,0x340820,0x330080,0x320000,0x314180,0x300300,0x2F0300,0x2E07FD,0x2DC8C0,0x2C0020,0x2B0000,0x2A0000,0x290000,0x280000,0x2703E8,0x260000,0x250104,0x240032,0x230004,0x220000,0x211E21,0x200393,0x1F43EC,0x1E318C,0x1D318C,0x1C0488,0x1B0002,0x1A0DB0,0x190C2B,0x18071A,0x17007C,0x160001,0x150401,0x14E048,0x1327B7,0x120064,0x11012C,0x100080,0x0F064F,0x0E1E70,0x0D4000,0x0C5001,0x0B0018,0x0A10D8,0x091604,0x082000,0x0740B2,0x06C802,0x0500C8,0x040A43,0x030642,0x020500,0x010808,0x00251C]),
            (12000, [0x700000,0x6F0000,0x6E0000,0x6D0000,0x6C0000,0x6B0000,0x6A0000,0x690021,0x680000,0x670000,0x663F80,0x650011,0x640000,0x630000,0x620200,0x610888,0x600000,0x5F0000,0x5E0000,0x5D0000,0x5C0000,0x5B0000,0x5A0000,0x590000,0x580000,0x570000,0x560000,0x55E700,0x540001,0x530000,0x523200,0x510000,0x506666,0x4F0026,0x4E0003,0x4D0000,0x4C000C,0x4B0800,0x4A0000,0x49003F,0x480001,0x470081,0x46C350,0x450000,0x4403E8,0x430000,0x4201F4,0x410000,0x401388,0x3F0000,0x3E0322,0x3D00A8,0x3C0000,0x3B0001,0x3A9001,0x390020,0x380000,0x370000,0x360000,0x350000,0x340820,0x330080,0x320000,0x314180,0x300300,0x2F0300,0x2E07FD,0x2DC8C0,0x2C0020,0x2B0000,0x2A0000,0x290000,0x280000,0x2703E8,0x260000,0x250104,0x24003C,0x230004,0x220000,0x211E21,0x200393,0x1F43EC,0x1E318C,0x1D318C,0x1C0488,0x1B0002,0x1A0DB0,0x190C2B,0x18071A,0x17007C,0x160001,0x150401,0x14E048,0x1327B7,0x120064,0x11012C,0x100080,0x0F064F,0x0E1E70,0x0D4000,0x0C5001,0x0B0018,0x0A10D8,0x091604,0x082000,0x0740B2,0x06C802,0x0500C8,0x040A43,0x030642,0x020500,0x010808,0x00251C]),
            (14000, [0x700000,0x6F0000,0x6E0000,0x6D0000,0x6C0000,0x6B0000,0x6A0000,0x690021,0x680000,0x670000,0x663F80,0x650011,0x640000,0x630000,0x620200,0x610888,0x600000,0x5F0000,0x5E0000,0x5D0000,0x5C0000,0x5B0000,0x5A0000,0x590000,0x580000,0x570000,0x560000,0x55E700,0x540001,0x530000,0x523200,0x510000,0x506666,0x4F0026,0x4E0003,0x4D0000,0x4C000C,0x4B0800,0x4A0000,0x49003F,0x480001,0x470081,0x46C350,0x450000,0x4403E8,0x430000,0x4201F4,0x410000,0x401388,0x3F0000,0x3E0322,0x3D00A8,0x3C0000,0x3B0001,0x3A9001,0x390020,0x380000,0x370000,0x360000,0x350000,0x340820,0x330080,0x320000,0x314180,0x300300,0x2F0300,0x2E07FD,0x2DC8C0,0x2C0020,0x2B0000,0x2A0000,0x290000,0x280000,0x2703E8,0x260000,0x250204,0x240046,0x230004,0x220000,0x211E21,0x200393,0x1F43EC,0x1E318C,0x1D318C,0x1C0488,0x1B0002,0x1A0DB0,0x190C2B,0x18071A,0x17007C,0x160001,0x150401,0x14E048,0x1327B7,0x120064,0x11012C,0x100080,0x0F064F,0x0E1E70,0x0D4000,0x0C5001,0x0B0018,0x0A10D8,0x091604,0x082000,0x0740B2,0x06C802,0x0500C8,0x040A43,0x030642,0x020500,0x010808,0x00251C])
        ]
        for freq_mhz, expected_spi_words in test_cases:
            self.pll.tune(freq_mhz)
            for i, (register, value) in enumerate(self.pll.registers.items()):
                expected = expected_spi_words[i]
                self.assertEqual(
                    value, 
                    expected, 
                    f"Mismatch for frequency {freq_mhz} MHz at register {register}:\n"
                    f"Expected: {hex(expected)}\n"
                    f"Actual: {hex(value)}"
                )

if __name__ == '__main__':
    unittest.main()