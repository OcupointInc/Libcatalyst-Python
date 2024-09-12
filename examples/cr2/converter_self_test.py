import time
import sys
import os
from collections import defaultdict

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from sensors.pll.LMX2595 import LMX2595
driver = FTDISPIDriver("configs/CR2_V2_FTDI.json", debug=False)

def is_locked(driver):
    return driver.read_gpio_pin("PLL_MISO")

lmx2595 = LMX2595(driver, "CS")

# High for Mixing, low for bypass
driver.write_gpio_pin("SW_BYPASS", 1)

# High for high pass filter, low for low pass filter
driver.write_gpio_pin("SW_FILTER", 0)