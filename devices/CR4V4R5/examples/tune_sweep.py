import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r5 import CR4V4R5

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

# Define the downconvert PLL LO frequency
single_convert_freq_mhz = 10000

# Tune the PLLs
cr4.tune_pll("D", single_convert_freq_mhz)
cr4.tune_pll("B", single_convert_freq_mhz)

# Set the unused PLL's into reset mode
cr4.plls["A"].reset_enable(1)
cr4.plls["C"].reset_enable(1)

# Set the converter switches to single conversion mode
cr4.set_switch("AB", "single")
cr4.set_switch("CD", "single")

# Set the attenuators to 0 dB attenuation on all 4 channels
cr4.set_attenuation_db([1,2,3,4], 0)

# Tune the filter into bypass mode
cr4.tune_filters(0, 0, 0, 0)

input(f"Tuned single convert to {single_convert_freq_mhz/1000}GHz LO. Press enter to switch to dual conversion")

# Define both the up and down conversion PLL LO frequency
single_convert_freq_mhz = 14000
dual_convert_freq_mhz = 12000

# Tune the PLLs
cr4.tune_pll("D", single_convert_freq_mhz)
cr4.tune_pll("B", single_convert_freq_mhz)
cr4.tune_pll("A", dual_convert_freq_mhz)
cr4.tune_pll("C", dual_convert_freq_mhz)

# Set the converter switches to single conversion mode
cr4.set_switch("AB", "dual")
cr4.set_switch("CD", "dual")

# Set the attenuators to 0 dB attenuation on all 4 channels
cr4.set_attenuation_db([1,2,3,4], 0)

# Tune the filter into bypass mode
cr4.tune_filters(0, 0, 0, 0)
input("done")