# ADRF5720 Control
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from sensors.rf_filters.ADMV8818 import ADMV8818
from drivers.ftdi_driver import FTDISPIDriver

driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=True)
fil = ADMV8818(driver, "CS_PLL_D")
fil.reset()
fil.tune(4,0,4,15)
#driver.write_spi("CS_PLL_D", 0x00003c, 24)
#driver.write_spi("CS_PLL_D", 0x0020DC, 24)
#driver.write_spi("CS_PLL_D", 0x002100, 24)
#driver.write_spi("CS_PLL_D", 0x000081, 24)

#fil.set_switches(1,1)