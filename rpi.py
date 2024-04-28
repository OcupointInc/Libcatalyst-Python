# LMX2595 testing
import time
from drivers.rpi_driver import RaspberryPiDriver
from sensors.pll.LMX2595 import LMX2595
from devices.keysight_e36311a import Keysight_e36311a


config = "configs/lmx2595_rpi.json"
driver = RaspberryPiDriver(config)
psu = Keysight_e36311a(config)

pll = LMX2595(driver, "CS")
#pll.set_readback_mode(1)
pll.tune(12000)
#pll.set_power_down(1)
time.sleep(0.2)
is_locked, vco = pll.read_is_locked()
print(f"Pll Locked: {is_locked}. Tuned to VCO{vco}")
print(f"Voltage: {psu.read_voltage(1)}v")
print(f"Current: {psu.read_current(1)}a")
#pll.read_register("R36")
psu.output_disable(1)
psu.close()