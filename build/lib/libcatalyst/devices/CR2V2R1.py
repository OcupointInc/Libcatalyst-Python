# Import necessary modules for various components
from libcatalyst.sensors.pll.LMX2595 import LMX2595
from libcatalyst.drivers.interface import DriverInterface

class CR2V2R1:
    def __init__(self, driver: DriverInterface, clock_frequency_mhz = 100):
        """
        Initialize the CR4V4R5 class with various components.
        
        :param driver: An instance of DriverInterface for communication with hardware
        """
        self.driver = driver
        self.clock_freq_mhz = clock_frequency_mhz
        
        # Initialize PLLs (Phase-Locked Loops) A, B, C, and D
        self.pll = LMX2595(self.driver, "CS")

        self.pll.set_osc_freq_mhz(self.clock_freq_mhz)

    def set_mixing_enable(self, state):
        self.driver.write_gpio_pin(f"SW_BYPASS", state)

    def set_lowpass_filter_enable(self, state):
        self.driver.write_gpio_pin(f"SW_FILTER", state)