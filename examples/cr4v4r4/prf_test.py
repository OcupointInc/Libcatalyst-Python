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
time.sleep(1)
cr4.tune_filters(0, 3, 3, 3)
time.sleep(1)
cr4.set_attenuation_db([1, 2, 3, 4], 15)
time.sleep(1)
cr4.tune_filters(2, 3, 0, 3)