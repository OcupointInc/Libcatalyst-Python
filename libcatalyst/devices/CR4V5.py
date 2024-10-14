# Import necessary modules for various components
from libcatalyst.sensors.pll.LMX2595 import LMX2595
from libcatalyst.sensors.io_expanders.MCP23S17T import MCP23S17T
from libcatalyst.sensors.digital_attenuators.HMC1018A import HMC1018A
from libcatalyst.sensors.rf_filters.ADMV8818 import ADMV8818
from libcatalyst.drivers.interface import DriverInterface

class CR4V4R5:
    def __init__(self, driver: DriverInterface):
        """
        Initialize the CR4V4R5 class with various components.
        
        :param driver: An instance of DriverInterface for communication with hardware
        """
        self.driver = driver

        # Set the USB Enable pin high
        self.driver.set_gpio_direction("USB_ENABLE", 1)
        self.driver.write_gpio_pin("USB_ENABLE", 1)
        
        # Initialize PLLs (Phase-Locked Loops) A, B, C, and D
        self.plls = {
            "A": LMX2595(self.driver, "CS_PLL_A"),
            "B": LMX2595(self.driver, "CS_PLL_B"),
            "C": LMX2595(self.driver, "CS_PLL_C"),
            "D": LMX2595(self.driver, "CS_PLL_D"),
        }

        # Set USB_Enable High
        self.driver.set_gpio_direction("USB_ENABLE", 1)
        self.driver.write_gpio_pin("USB_ENABLE", 1)

        # Initialize I/O expander, attenuator, and filter
        self.io_expander = MCP23S17T(self.driver, "CS_PRF_IO")
        self.attenuator = HMC1018A(self.io_expander, "CS_PRF_IO")
        self.filter = ADMV8818(self.io_expander, "CS_PRF_IO")
        
        # Configure I/O expander directions
        self.io_expander.set_bank_direction("A", 0x00)  # Set all pins in bank A as outputs
        self.io_expander.set_bank_direction("B", 0xC3)  # Set specific pins in bank B as inputs/outputs
        
        # Set default clock select to internal
        self.set_clock_select("internal")

    def set_switch(self, name, state):
        """
        Set the state of a switch (AB or CD).
        
        :param name: Name of the switch ("AB" or "CD")
        :param state: State of the switch ("dual" or not)
        """
        if name == "AB" or name == "CD":
            value = 0 if state != "dual" else 1
            self.driver.write_gpio_pin(f"SW_{name}", value)
        else:
            raise ValueError("Switch name needs to be AB or CD")
        
    def set_clock_select(self, val):
        """
        Set the clock select to either internal or external.
        
        :param val: "internal" or "external"
        """
        self.driver.write_gpio_pin("CLK_SEL", True if val == "internal" else False)

    def tune_filters(self, lpf_switch, lpf_band, hpf_switch, hpf_band):
        """
        Tune the low-pass and high-pass filters with given parameters.
        
        :param lpf_switch: Low-pass filter switch setting (integer from 0 to 3)
        :param lpf_band: Low-pass filter band selection (integer from 0 to 15)
        :param hpf_switch: High-pass filter switch setting (integer from 0 to 3)
        :param hpf_band: High-pass filter band selection (integer from 0 to 15)
        """
        # Configure I/O expander for filter tuning
        self.io_expander.spi_bank = "B"
        self.io_expander.cs_mask = 0x30
        self.io_expander.sclk_pin = 0x04
        self.io_expander.mosi_pin = 0x08
        
        # Set the other CS pins high
        self.io_expander.write_bank_state("A", 0x0F)
        
        # Tune the filters using the ADMV8818 filter object
        # lpf_switch and hpf_switch: 0-3, lpf_band and hpf_band: 0-15
        self.filter.tune(lpf_switch, lpf_band, hpf_switch, hpf_band)

    def set_attenuation_db(self, channels, attenuation):
        """
        Sets the attenuation in dB for specified channels.

        :param channels: List of channels (1 to 4) to set attenuation
        :param attenuation: The attenuation value in dB (0 to 31 in increments of 1)
        """
        if len(channels) < 1 or len(channels) > 4:
            raise ValueError("Invalid channels, please enter a list of channels, from 1 to 4")
        
        cs_mask = 0x00
        for channel in channels:
            if channel < 1 or channel > 4:
                raise ValueError("Invalid channel, channels should be 1, 2, 3, or 4")
            cs_mask |= (1 << channel-1)

        # Configure I/O expander for attenuation setting
        self.io_expander.spi_bank = "A"
        self.io_expander.cs_mask = cs_mask
        self.io_expander.sclk_pin = 0x10
        self.io_expander.mosi_pin = 0x20
        # Set the other CS pins high
        self.io_expander.write_bank_state("B", 0x3C)
        # Set the attenuation
        self.attenuator.set_attenuation_db(attenuation)

    def tune_pll(self, pll_name, frequency_mhz):
        """
        Tune a specific PLL to a given frequency in MHz.
        
        :param pll_name: Name of the PLL ("A", "B", "C", or "D")
        :param frequency_mhz: Frequency to tune to in MHz
        """
        self.plls[pll_name].tune(frequency_mhz)

    def power_off_pll(self, pll_name):
        """
        Power off a specific PLL.
        
        :param pll_name: Name of the PLL to power off
        """
        self.plls[pll_name].power_down()

    def power_up_pll(self, pll_name):
        """
        Power up a specific PLL.
        
        :param pll_name: Name of the PLL to power up
        """
        self.plls[pll_name].power_up()

    def pll_reset_enable(self, pll_name, state):
        """
        Enable or disable reset for a specific PLL.
        
        :param pll_name: Name of the PLL
        :param state: Boolean indicating whether to enable (True) or disable (False) reset
        """
        self.plls[pll_name].reset_enable(state)

    def read_is_locked(self):
        """
        Read the lock status of the PLL.
        
        :return: Boolean indicating whether the PLL is locked (True) or not (False)

        The Readback is tied in pairs, between PLLS AB and PLLS CD
        """
        return self.driver.read_gpio_pin("PLL_MISO")