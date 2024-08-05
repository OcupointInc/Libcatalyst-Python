import time
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from sensors.pll.LMX2595 import LMX2595
from devices.cr4_v4r4 import CR4V4R4

driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R4(driver)
pll_ids = ["D", "C", "B", "A"]

# Reset all of the PLLs
for pll_id in pll_ids:
    cr4.reset_pll(pll_id)


single_convert_freq_mhz = 12000
# Tune to single convert
cr4.tune_pll("D", single_convert_freq_mhz)
cr4.tune_pll("B", single_convert_freq_mhz)
cr4.set_switch("AB", "single")
cr4.set_switch("CD", "single")

input("Tuned single convert to 12GHz.")

single_convert_freq_mhz = 14000
dual_convert_freq_mhz = 12000
# Tune to dual convert
cr4.tune_pll("D", single_convert_freq_mhz)
cr4.tune_pll("B", single_convert_freq_mhz)
cr4.tune_pll("C", dual_convert_freq_mhz)
cr4.tune_pll("A", dual_convert_freq_mhz)
cr4.set_switch("AB", "dual")
cr4.set_switch("CD", "dual")
input("Tuned dual convert to 12GHz and 14GHz")