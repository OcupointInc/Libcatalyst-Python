# QC Example.py
import time
from drivers.mock import MockDriver
from sensors.pll.LMX2595 import LMX2595
from devices.keysight_e36311a import Keysight_e36311a


config = "configs/lmx2595_rpi.json"
driver = MockDriver(config)
for i in range(10):
    #psu = Keysight_e36311a("configs/lmx2595_rpi.json")

   # with open("hex_nick.txt", "r") as file:
        # Loop through each line in the file
   #     for line in file:
            # Convert each line to a hexadecimal value
           # hex_value = int(line.strip(), 16)
            # Process the hexadecimal value here
           # driver.write_spi("CS", hex_value, 24)
            # Check to see if the PLL Lock is high or low
    pll = LMX2595(driver, "CS")
    pll.tune(10000)
    pll.tune(12000)
    pll.tune(14000)
    time.sleep(0.1)
    state = driver.read_gpio_pin("MISO")
    if not state:
        print("Failed")
        break

    #input("press any key to stop")
    #psu.output_disable(1)
    #psu.close()