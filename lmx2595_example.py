# QC Example.py
import time
from drivers.ftdi_driver import FTDISPIDriver
from drivers.mock import MockDriver
from sensors.pll.LMX2595 import LMX2595

driver = FTDISPIDriver("configs/lmx2595_FTDI.json", debug=True)

pll_d = LMX2595(driver, "CS_PLL_D")
pll_d.tune(12000)
time.sleep(0.1)
print(driver.read_gpio_pin("PLL_D_MISO"))