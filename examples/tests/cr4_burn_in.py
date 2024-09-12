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
psu = Keysight_e36311a("configs/CR4_V4_FTDI.json")
cr4 = CR4V4R5(driver)
psu.output_disable(1)
psu.output_disable(2)
time.sleep(2)


def tune():
    single_convert_freq_mhz = 10000    # Tune the CR4
    for pll in cr4.plls.values():
        pll.reset_enable(1)

    cr4.tune_pll("D", single_convert_freq_mhz)
    cr4.tune_pll("B", single_convert_freq_mhz)
    for pll in cr4.plls.values():
        pll.set_pll_power("A", 63)
        pll.set_pll_power("B", 63)
    cr4.set_switch("AB", "single")
    cr4.set_switch("CD", "single")
    cr4.tune_filters(0, 0, 0, 0)
    cr4.set_attenuation_db([1,2,3,4], 0)
    time.sleep(0.1)
    cr4.set_attenuation_db([1,2,3,4], 0)
    time.sleep(0.1)
    cr4.set_attenuation_db([1,2,3,4], 0)

    for pll in cr4.plls.values():
        pll.reset_enable(1)

    cr4.tune_pll("D", single_convert_freq_mhz)
    cr4.tune_pll("B", single_convert_freq_mhz)
    for pll in cr4.plls.values():
        pll.set_pll_power("A", 31)
        pll.set_pll_power("B", 31)
    cr4.set_switch("AB", "single")
    cr4.set_switch("CD", "single")
    cr4.tune_filters(0, 0, 0, 0)
    cr4.set_attenuation_db([1,2,3,4], 0)
    time.sleep(0.1)
    cr4.set_attenuation_db([1,2,3,4], 0)
    time.sleep(0.1)
    cr4.set_attenuation_db([1,2,3,4], 0)

for i in range(10000):
    # Turn the power supplies on
    psu.output_enable(1)
    psu.output_enable(2)

    # Expect 5V power draw to be less than 3A
    current_draw = psu.read_current(1)
    if current_draw > 3:
        raise ValueError("Expect the current to be less than 3 amps on 5V")
    
    # Expect 12V power draw to be less than 0.5A
    current_draw = psu.read_current(2)
    if current_draw > 0.5:
        raise ValueError("Expect the current to be less than 0.5 amps on 12V")
    
    tune()
    tune()

    

    # Expect 5V power draw to be less than 4A
    current_draw = psu.read_current(1)
    if current_draw > 4:
        raise ValueError("Expect the current to be less than 4 amps on 5V after tuning")
    
    # Expect 12V power draw to be less than 0.5A
    current_draw = psu.read_current(2)
    if current_draw > 0.5:
        raise ValueError("Expect the current to be less than 0.5 amps on 12V")
    
    # Keep it on for 2 min
    time.sleep(10)

    # Turn the power supplies off
    psu.output_disable(1)
    psu.output_disable(2)

    # Keep it off for 1 min
    time.sleep(2)