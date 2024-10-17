from libcatalyst.drivers.ftdi_driver import FTDISPIDriver, pin_map
from libcatalyst.devices.CR4V5 import CR4V4R5
import time

driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

# Turn all of them low
for pin in pin_map:
    if pin == "D3":
        continue
    cr4.driver._write_gpio_pin(pin, 0)

# Toggle high individually
for pin in pin_map:
    if pin == "D3":
        continue
    print(f"Setting {pin} high")
    cr4.driver._write_gpio_pin(pin, 1)
    time.sleep(2)
    cr4.driver._write_gpio_pin(pin, 0)
    time.sleep(0.5)
