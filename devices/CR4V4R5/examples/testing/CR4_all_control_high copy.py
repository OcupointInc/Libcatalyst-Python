from libcatalyst.drivers.ftdi_driver import FTDISPIDriver, pin_map
from libcatalyst.devices.CR4V5 import CR4V4R5
import time

driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)