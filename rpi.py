# QC Example.py
import time
from drivers.rpi_driver import RaspberryPiDriver
from sensors.pll.LMX2595 import LMX2595

driver = RaspberryPiDriver("device_id", "configs/lmx2595_rpi.json")
driver.set_gpio_direction("input", 0)
driver.set_gpio_direction("output", 1)

driver.write_gpio_pin("output", 1)
driver.read_gpio_pin("input")