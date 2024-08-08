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
pll_ids = ["D", "C", "B", "A"]

def reset_all_plls():
    for pll_id in pll_ids:
        cr4.reset_pll(pll_id)

def power_down_all_plls():
    for pll_id in pll_ids:
        cr4.power_off_pll(pll_id)

passed = True
LOs = [10000, 12000, 14000]
for pll_id in pll_ids:
    for LO_freq_mhz in LOs:
        # Check to make sure its not locked currently
        is_locked = driver.read_gpio_pin("PLL_MISO")
        if is_locked:
            print(f"Error: PLL {pll_id} is locked before tuning")
            reset_all_plls()
            power_down_all_plls()
            passed = False

        # Tune the converter
        cr4.power_up_pll(pll_id)
        cr4.tune_pll(pll_id, LO_freq_mhz)

        time.sleep(0.1)
        is_locked = cr4.read_is_locked()

        if not is_locked:
            print(f"Error: PLL {pll_id} could not be locked")
            passed = False
        else:
            print(f"PLL {pll_id} {LO_freq_mhz} mhz locked")

        cr4.reset_pll(pll_id)
        cr4.power_off_pll(pll_id)
    
input("Press enter and watch to see the switch LED's flash")
for i in range(10):
    cr4.set_switch("AB", "dual")
    cr4.set_switch("CD", "dual")
    time.sleep(0.1)
    cr4.set_switch("AB", "single")
    cr4.set_switch("CD", "single")
    time.sleep(0.1)

if passed:
    print("All PLL Locking Tests have passed")
else:
    print("Eror during test, verify test setup or rework the hardware")