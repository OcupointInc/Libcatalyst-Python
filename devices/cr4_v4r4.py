# QC.py
from sensors.pll.LMX2595 import LMX2595
from sensors.io_expanders.MCP23S17T import MCP23S17T
from drivers.interface import DriverInterface

class CR4V4R4:
    def __init__(self, driver: DriverInterface):
        self.driver = driver
        self.plls = {
            "A": LMX2595(self.driver, "CS_PLL_A"),
            "B": LMX2595(self.driver, "CS_PLL_B"),
            "C": LMX2595(self.driver, "CS_PLL_C"),
            "D": LMX2595(self.driver, "CS_PLL_D"),

        }

        self.io_expander = MCP23S17T(self.driver, "CS_PRF_IO")

    def set_attenuation_db(self, channels, attenuation):
        """
        Sets the attenuation in dB.

        Parameters:
        attenuation (int): The attenuation value in dB. This should be a value from 0 to 31 in increments of 1.
        """
        if len(channels) < 1 or len(channels) > 4:
            raise ValueError("Invalid channels, please enter a list of channels, from 1 to 4")
        
        data = 31 - attenuation
        cs_mask = 0x00
        for channel in channels:
            if channel < 1 or channel > 4:
                raise ValueError("Invalid channel, channels should be 1, 2, 3, or 4")
            cs_mask |= (1 << channel-1)

        # 0x20 is the MOSI pin, and 0x10 is the SCLK pin, writing 6 bits
        self.io_expander.write_spi("A", data, cs_mask, 0x20, 0x10, 6)

    def tune_pll(self, pll_name, frequency_mhz):
        self.plls[pll_name].tune(frequency_mhz)

    def power_off_pll(self, pll_name):
        self.plls[pll_name].power_down()

    def power_up_pll(self, pll_name):
        self.plls[pll_name].power_up()
