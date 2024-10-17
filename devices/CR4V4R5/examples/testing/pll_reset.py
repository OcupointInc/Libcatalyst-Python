import time
import logging
from collections import defaultdict
from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5

sleep_time = 0.0005  # Reduced sleep time

# Initialize driver and device
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

# Set all PLLs to reset mode
for name, pll in cr4.plls.items():
    cr4.pll_reset_enable(name, 1)

sw_ab_state = "single"
sw_cd_state = "single"

cr4.set_switch("AB", sw_ab_state)
cr4.set_switch("CD", sw_cd_state)