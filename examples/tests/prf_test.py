# QC Example.py
import sys
import os
import time
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r4 import CR4V4R4

driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R4(driver)

# Example usage
cr4.set_attenuation_db([1, 2, 3, 4], 0)
filter_bands = [
    [0, 0, 0, 0, 0, "Bypass"], # Bypass
    [0, 0, 0, 0, 31, "Bypass"], # Bypass
    [0, 0, 0, 0, 0, "Bypass"], # Bypass
    [1, 0, 2, 6, 0, "2-4 Ghz"], # 2-4
    [2, 0, 2, 15, 0, "4-6 GHz"], # 4-6
    [0, 10, 3, 1, 0, "6-8 GHz"], #6-8
    [2, 15, 3, 4, 0, "8-10 GHz"],
    [3, 10, 4, 2, 0, "10-12 GHz"],
    [3, 15, 4, 5, 0, "12-14 GHz"],
    [4, 4, 4, 12, 0, "14-16 GHz"],
    [4, 8, 4, 15, 0, "16-18 GHz"]
]
for filter_band in filter_bands[0:]:
    cr4.set_attenuation_db([1,2,3,4], filter_band[4])
    cr4.tune_filters(filter_band[0],filter_band[1],filter_band[2],filter_band[3])
    input(f"Tuned the filter band {filter_band[5]} att: {filter_band[4]}")
#cr4.tune_filters(0,0,0,0)
# 2-4GHz cr4.tune_filters(1, 0, 2, 6)
# 4-6GHz cr4.tune_filters(2, 0, 2, 15)
# 6-8GHz cr4.tune_filters(2, 10, 3, 5)
#input("Tune to 8-1GHz")
#cr4.tune_filters(3, 4, 0, 10)
# 8-10GHz cr4.tune_filters(3, 3, 3, 10)
# 10-12GHz cr4.tune_filters(3, 10, 4, 2)
# 12-14GHz cr4.tune_filters(3, 15, 4, 5)
# 14-16GHz cr4.tune_filters(4, 4, 4, 12)
# 16-18GHz cr4.tune_filters(4, 8, 4, 15)