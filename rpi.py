# LMX2595 testing
import time
from drivers.rpi_driver import RaspberryPiDriver
from sensors.pll.LMX2595 import LMX2595
from devices.keysight_e36311a import Keysight_e36311a


config = "configs/lmx2595_rpi.json"
driver = RaspberryPiDriver(config)
psu = Keysight_e36311a(config)

pll = LMX2595(driver, "CS")
pll.tune(12000)
time.sleep(0.1)
driver.exchange_spi("CS", 0xF0, 8, 16) # R112
driver.exchange_spi("CS", 0xEF, 8, 16) # R111
driver.exchange_spi("CS", 0xEE, 8, 16) # R110

psu.output_disable(1)
psu.close()