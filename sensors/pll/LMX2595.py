# rf_digital_attenuator.py


class LMX2595():
    def __init__(self, driver, cs):
        self.driver = driver
        self.cs = cs
        self.max_freq = 20000
        self.common_spi = [
        0x4d0000, 0x4c000c, 0x4b0800, 0x4a0000, 0x49003f, 0x480000, 0x470021,
        0x46c350, 0x450000, 0x4403e8, 0x430000, 0x4201f4, 0x410000, 0x401388, 0x3f0000, 
        0x3e0322, 0x3d00a8, 0x3c0000, 0x3b0001,0x3a8001, 0x390020, 0x380000, 0x370000, 
        0x360000, 0x350000, 0x340820, 0x330080, 0x320000, 0x314180, 0x300300, 0x2f0300, 0x2e07fd, 
        0x2dcefc, 0x2c3c22, 0x2b0000, 0x2a0000, 0x290000, 0x280000, 0x2703e8, 0x260000, 0x230004, 
        0x220000, 0x211e21, 0x200393, 0x1f43ec, 0x1e318c, 0x1d318c, 0x1c0488, 0x1b0002, 0x1a0db0, 
        0x190624, 0x18071a, 0x17007c, 0x160001, 0x150401, 0x1327b7, 0x120064, 0x11012c, 0x100080,
        0x0f064f, 0x0e1e70, 0x0d4000, 0x0c5001, 0x0b0018, 0x0a10d8, 0x091604, 0x082000, 0x0740b2, 
        0x06c802, 0x0500c8, 0x040a43, 0x030642, 0x020500, 0x010808, 0x002510, 0x002518
        ]

        self.frequency_dependant_spi = {
            10000:[0x4e006f,0x250204,0x240032,0x14f848],
            12000:[0x4e0003,0x250304, 0x24003c, 0x14e048],
            14000:[0x4e006f,0x250304, 0x240046, 0x14f848]
        }
    

    def tune_pll(self, freq_mhz):
        if freq_mhz > self.max_freq or freq_mhz < 0:
            raise ValueError(f"PLL Frequency must be between 0 and {self.max_freq} dB (inclusive).")
        
        if freq_mhz not in self.frequency_dependant_spi:
            raise ValueError(f"Frequency {freq_mhz} setting not defined.")
        
        #ld_typeSet = 0x3b0000 | (LD_TYPE & 0xFF)
        #ld_dlySet = 0x3c0000 | (LD_DLY & 0xFF)


        index_to_insert_26 = self.common_spi.index(0x260000) + 1
        index_to_insert_14 = self.common_spi.index(0x150401) + 1
       # index_to_insert_36 = self.common_spi.index(0x3d00a8) + 1
        spi_words = (
            [self.frequency_dependant_spi[freq_mhz][0]] +
            self.common_spi[:index_to_insert_26] +
            [self.frequency_dependant_spi[freq_mhz][1], self.frequency_dependant_spi[freq_mhz][2]] +
            self.common_spi[index_to_insert_26:index_to_insert_14] +
            [self.frequency_dependant_spi[freq_mhz][3]] +
            self.common_spi[index_to_insert_14:]
        )

        hex_settings = [f"0x{x:06x}" for x in spi_words]
        print(hex_settings)

        #for spi_word in spi_words:
         #   self.driver.write_spi(self.cs, spi_word, 24) 
        
        
        # self.driver.write_spi(self.cs, spi_word, self.num_bits)
        pass

