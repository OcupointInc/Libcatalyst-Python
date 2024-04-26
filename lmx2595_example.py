# QC Example.py
import time
from drivers.rpi_driver import RaspberryPiDriver
from sensors.pll.LMX2595 import LMX2595

driver = RaspberryPiDriver("configs/lmx2595_rpi.json")

pll = LMX2595(driver, "CS")
pll.tune_pll(14000)
# while True:
#     pll.tune_pll(14000)
#     time.sleep(1)
#     pll.tune_pll(12000)
#pll.tune_pll(14000)