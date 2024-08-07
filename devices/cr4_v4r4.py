# QC.py
from sensors.pll.LMX2595 import LMX2595
from sensors.io_expanders.MCP23S17T import MCP23S17T
from sensors.digital_attenuators.HMC1018A import HMC1018A
from sensors.rf_filters.ADMV8818 import ADMV8818
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
        self.attenuator = HMC1018A(self.io_expander, "CS_PRF_IO")
        self.filter = ADMV8818(self.io_expander, "CS_PRF_IO")
        self.io_expander.set_bank_direction("A", 0x00)
        self.io_expander.set_bank_direction("B", 0xC3)

    def set_switch(self, name, state):
        #if state != "single" or state != "dual":
        #    raise ValueError("State needs to be single or dual")
        
        if name == "AB" or name == "CD":
            value = 0

            if state == "dual":
                value = 1

            self.driver.write_gpio_pin(f"SW_{name}", value)
        else:
            raise ValueError("Switch name needs to be AB or CD")
        

    def tune_filters(self, lpf1, lpf2, hpf1, hpf2):
        self.io_expander.spi_bank = "B"
        self.io_expander.cs_mask = 0x30
        self.io_expander.sclk_pin = 0x04
        self.io_expander.mosi_pin = 0x08
        # Set the other CS pins high
        self.io_expander.write_bank_state("A", 0x0F)
        self.filter.tune(lpf1, lpf2, hpf1, hpf2)

    def set_attenuation_db(self, channels, attenuation):
        """
        Sets the attenuation in dB.

        Parameters:
        attenuation (int): The attenuation value in dB. This should be a value from 0 to 31 in increments of 1.
        """
        if len(channels) < 1 or len(channels) > 4:
            raise ValueError("Invalid channels, please enter a list of channels, from 1 to 4")
        
        cs_mask = 0x00
        for channel in channels:
            if channel < 1 or channel > 4:
                raise ValueError("Invalid channel, channels should be 1, 2, 3, or 4")
            cs_mask |= (1 << channel-1)

        self.io_expander.spi_bank = "A"
        self.io_expander.cs_mask = cs_mask
        self.io_expander.sclk_pin = 0x10
        self.io_expander.mosi_pin = 0x20
        # Set the other CS pins high
        self.io_expander.write_bank_state("B", 0x3C)
        self.attenuator.set_attenuation_db(attenuation)

    def tune_pll(self, pll_name, frequency_mhz):
        self.plls[pll_name].tune(frequency_mhz)

    def power_off_pll(self, pll_name):
        self.plls[pll_name].power_down()

    def power_up_pll(self, pll_name):
        self.plls[pll_name].power_up()

    def reset_pll(self, pll_name):
        self.plls[pll_name].reset()

    def read_is_locked(self):
        return self.driver.read_gpio_pin("PLL_MISO")
