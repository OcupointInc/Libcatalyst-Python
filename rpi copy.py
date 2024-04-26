# QC Example.py
import time
from drivers.rpi_driver import RaspberryPiDriver
from sensors.pll.LMX2595 import LMX2595
from devices.keysight_e36311a import Keysight_e36311a

driver = RaspberryPiDriver("configs/lmx2595_rpi.json")
psu = Keysight_e36311a("configs/lmx2595_rpi.json")
psu.close()
exit()
# Open the file in read mode
with open("hex.txt", "r") as file:
    # Loop through each line in the file
    for line in file:
        # Convert each line to a hexadecimal value
        hex_value = int(line.strip(), 16)
        #hex_value_24bit = hex_value & 0xFFFFFF
        # Process the hexadecimal value here
        driver.write_spi("CS", hex_value, 24)

# Check to see if the PLL Lock is high or low
time.sleep(0.1)
lock_en = driver.read_gpio_pin("MISO")
