# LMX2595 Test, cr4 wraps the LMX2595 PLL
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r4 import CR4V4R4
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R4(driver)

cr4.set_switch("AB", "single")
cr4.set_switch("CD", "single")

for lo in [10000, 12000, 14000]:
    
    cr4.tune_pll("D", lo)
    input("next")
    cr4.plls["D"].unlock()