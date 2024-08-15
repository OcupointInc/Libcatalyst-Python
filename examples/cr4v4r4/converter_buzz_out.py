import time
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r4 import CR4V4R4

driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R4(driver)

pins = [
    "CS_PLL_D",
    "CS_PLL_B",
    "CS_PLL_C",
    "CS_PLL_A",
    "MOSI",
    "SCLK"
]

# Turn all of them low
for pin in pins:
    cr4.driver.write_gpio_pin(pin, 0)
    

for pin in pins:

    cr4.driver.write_gpio_pin(pin, 1)
    input(f'{pin} pulled high')
    cr4.driver.write_gpio_pin(pin, 0)