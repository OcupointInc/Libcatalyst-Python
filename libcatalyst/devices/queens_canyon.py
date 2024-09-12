# QC.py
from sensors.digital_attenuators.ADRF5720 import ADRF5720
from drivers.interface import DriverInterface
from enum import Enum

class QCBank(Enum):
    Bypass = 0
    LPF_0p5GHz = 1
    LPF_1GHz = 2
    LPF_2GHz = 3

class QueensCanyon:
    def __init__(self, driver: DriverInterface):
        self.driver = driver

        self.attenuators = ADRF5720(self.driver, "attenuator_cs")

        self.bypass_switch = self._setup_gpio_pin("bypass_switch_gpio", 1)
        self.v1_in = self._setup_gpio_pin("v1_in_gpio", 1)
        self.v2_in = self._setup_gpio_pin("v2_in_gpio", 1)
        self.v1_out = self._setup_gpio_pin("v1_out_gpio", 1)
        self.v2_out = self._setup_gpio_pin("v2_out_gpio", 1)

    def set_attenuation_db(self, attenuation):
        """
        Sets the attenuation in dB.

        Parameters:
        attenuation (float): The attenuation value in dB. This should be a value from 0 to 31.5 in increments of 0.5.
        """
        self.attenuators.set_attenuation_db(attenuation)

    def read_attenuation_db(self):
        """
        Reads the current attenuation in dB.

        Returns:
        float: The current attenuation value in dB. This will be a value from 0 to 31.5 in increments of 0.5.
        """
        return self.attenuators.read_attenuation_db()
    
    def set_bypass_enable(self, enable):
        """
        Enables or disables the bypass switch.

        Parameters:
        enable (bool): If True, the bypass switch is enabled. If False, it is disabled.
        """
        self.driver.write_gpio_pin(self.bypass_switch, enable)

    def set_filter_bank(self, value: QCBank):
        """
        Sets the filter bank to a specific state.

        Parameters:
        value (QCBank): The state to set the filter bank to. This should be a value from QCBank enum.

        Raises:
        ValueError: If the provided value is not a valid QCBank enum value.
        """
        # Bypass Mode
        if value == QCBank.Bypass:
            self.driver.write_gpio_pin(self.v1_in, 1)
            self.driver.write_gpio_pin(self.v2_in, 1)
            self.driver.write_gpio_pin(self.v1_out, 0)
            self.driver.write_gpio_pin(self.v2_out, 1)
        # LPF 0.5 GHz
        elif value == QCBank.LPF_0p5GHz:
            self.driver.write_gpio_pin(self.v1_in, 0)
            self.driver.write_gpio_pin(self.v2_in, 1)
            self.driver.write_gpio_pin(self.v1_out, 1)
            self.driver.write_gpio_pin(self.v2_out, 1)
        # LPF 1 GHz
        elif value == QCBank.LPF_1GHz:
            self.driver.write_gpio_pin(self.v1_in, 1)
            self.driver.write_gpio_pin(self.v2_in, 0)
            self.driver.write_gpio_pin(self.v1_out, 0)
            self.driver.write_gpio_pin(self.v2_out, 0)
        # LPF 2 GHz
        elif value == QCBank.LPF_2GHz:
            self.driver.write_gpio_pin(self.v1_in, 0)
            self.driver.write_gpio_pin(self.v2_in, 0)
            self.driver.write_gpio_pin(self.v1_out, 1)
            self.driver.write_gpio_pin(self.v2_out, 0)
        else:
            raise ValueError("Invalid filter bank value. Must be a valid QCBank enum value.")

    def _setup_gpio_pin(self, config_key, direction):
        self.driver.set_gpio_direction(config_key, direction)
        return config_key

    