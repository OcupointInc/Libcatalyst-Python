# rf_digital_attenuator.py


class LMX2595():
    def __init__(self, driver, cs):
        self.driver = driver
        self.cs = cs

    def tune_pll(self, freq_mhz):
        
        # self.driver.write_spi(self.cs, spi_word, self.num_bits)
        pass

