import time
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r5 import CR4V4R5
from devices.keysight_e36311a import Keysight_e36311a
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

for (name, pll) in cr4.plls.items():
    pll.power_down()
    print(f"powered down PLL {name}")
    input("Next")