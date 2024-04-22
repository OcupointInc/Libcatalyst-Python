# QC.py
from sensors.digital_attenuators.ADRF5720 import ADRF5720
from drivers.interface import DriverInterface
from dataclasses import dataclass, field

@dataclass
class ChannelConfig:
    attenuator_cs: str
    attenuator_ps_gpio: str
    bypass_switch_gpio: str
    v1_in_gpio: str
    v2_in_gpio: str
    v1_out_gpio: str
    v2_out_gpio: str

from enum import Enum


class QCBank(Enum):
    Bypass = 0
    LPF_0p5GHz = 1
    LPF_1GHz = 2
    LPF_2GHz = 3

class QC:
    def __init__(self, driver: DriverInterface):
        self.driver = driver

        self.attenuators = ADRF5720(self.driver, "attenuator_cs")

        self.bypass_switch = self.setup_gpio_pin("bypass_switch_gpio", 1)
        self.v1_in = self.setup_gpio_pin("v1_in_gpio", 1)
        self.v2_in = self.setup_gpio_pin("v2_in_gpio", 1)
        self.v1_out = self.setup_gpio_pin("v1_out_gpio", 1)
        self.v2_out = self.setup_gpio_pin("v2_out_gpio", 1)

    def set_attenuation_db(self, attenuation):
        self.attenuators.set_attenuation_db(attenuation)

    def read_attenuation_db(self):
        return self.attenuators.read_attenuation_db()
    
    def set_bypass_enable(self, enable):
        self.driver.write_gpio_pin(self.bypass_switch, enable)

    def set_filter_bank(self, value: QCBank):
        # Bypass Mode
        if value == 0:
            self.driver.write_gpio_pin(self.v1_in, 1)
            self.driver.write_gpio_pin(self.v2_in, 1)
            self.driver.write_gpio_pin(self.v1_out, 0)
            self.driver.write_gpio_pin(self.v2_out, 1)
        # LPF 0.5 GHz
        elif value == 1:
            self.driver.write_gpio_pin(self.v1_in, 0)
            self.driver.write_gpio_pin(self.v2_in, 1)
            self.driver.write_gpio_pin(self.v1_out, 1)
            self.driver.write_gpio_pin(self.v2_out, 1)
        # LPF 1 GHz
        elif value == 2:
            self.driver.write_gpio_pin(self.v1_in, 1)
            self.driver.write_gpio_pin(self.v2_in, 0)
            self.driver.write_gpio_pin(self.v1_out, 0)
            self.driver.write_gpio_pin(self.v2_out, 0)
            pass
        # LPF 2 GHz
        elif value == 3:
            self.driver.write_gpio_pin(self.v1_in, 0)
            self.driver.write_gpio_pin(self.v2_in, 0)
            self.driver.write_gpio_pin(self.v1_out, 1)
            self.driver.write_gpio_pin(self.v2_out, 0)
            pass
        else:
            raise ValueError("Invalid filter bank value. Must be 0, 1, 2, or 3.")

    def setup_gpio_pin(self, config_key, direction):
        self.driver.set_gpio_direction(config_key, direction)
        return config_key

    