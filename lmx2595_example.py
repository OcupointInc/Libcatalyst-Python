# QC Example.py
import time
from drivers.ftdi_driver import FTDISPIDriver
from drivers.mock import MockDriver
from sensors.pll.LMX2595 import LMX2595

driver = FTDISPIDriver("configs/lmx2595_FTDI.json", debug=True)

pll_d = LMX2595(driver, "CS_PLL_A")
pll_d.tune(14000)
