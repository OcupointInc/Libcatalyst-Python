from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5

driver = FTDISPIDriver("devices/CR4V4R5/configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

pins = [
    #"CS_PRF_IO",
    "CS_PLL_D",
    "CS_PLL_B",
    "CS_PLL_C",
    "CS_PLL_A",
    "MOSI",
    "SCLK"
]

# Turn all of them low
for pin in pins:
    cr4.driver.write_gpio_pin(pin, 0)
    

for pin in pins:

    cr4.driver.write_gpio_pin(pin, 1)
    input(f'{pin} pulled high')
    cr4.driver.write_gpio_pin(pin, 0)