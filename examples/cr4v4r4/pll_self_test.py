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

time.sleep(0.1)
# Make sure all of the lock detect signals are low
is_locked = driver.read_gpio_pin("PLL_MISO")

if is_locked:
    raise ValueError("Should not be locked, just reset all of the PLLS")

LOs = [10000, 12000, 14000]
for pll_id in pll_ids:
    for LO_freq_mhz in LOs:
        cr4.power_up_pll(pll_id)
        cr4.tune_pll(pll_id, LO_freq_mhz)

        time.sleep(0.1)
        is_locked = cr4.read_is_locked()

        if not is_locked:
            print(f"Error: PLL {pll_id} could not be locked")
        else:
            print(f"PLL {pll_id} {LO_freq_mhz} mhz locked")

        cr4.reset_pll(pll_id)
        cr4.power_off_pll(pll_id)
        is_still_locked = cr4.read_is_locked()
        
        time.sleep(0.1)
        if is_still_locked:
            print(f"Not able to turn PLL {pll_id} off")