# QC Example.py
import time
from drivers.ftdi_driver import FTDISPIDriver
from drivers.mock import MockDriver
from devices.cr4_v4r4 import CR4V4R4
from sensors.rf_filters.ADMV8818 import ADMV8818
from sensors.io_expanders.MCP23S17T import MCP23S17T
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=True)

io = MCP23S17T(driver, "CS_PRF_IO")

filt = ADMV8818(driver, "CS_PRF_IO")

cr4 = CR4V4R4(driver)

driver.write_spi("CS", 0x00081, 24)
driver.write_spi("CS", 0x0020c0, 24)
driver.write_spi("CS", 0x00210f, 24)
exit()

cr4.set_attenuation_db([1,2,3,4], 16)
#exit()

# Sets all pins other than the SFL pins for the 8818 high
cr4.io_expander.write_bank_state("A", 0x0F)
MOSI_pin = 0x08
SCLK_pin = 0x04
num_bits = 24
cs_mask = 0x30

#cr4.io_expander.write_bank_state("A", 0xC0)
cr4.io_expander.write_spi("B", 0x00081, cs_mask, MOSI_pin, SCLK_pin, num_bits)
cr4.io_expander.write_spi("B", 0x0003C, cs_mask, MOSI_pin, SCLK_pin, num_bits)
#print()
cr4.io_expander.write_spi("B", 0x0020c0, cs_mask, MOSI_pin, SCLK_pin, num_bits)
cr4.io_expander.write_spi("B", 0x00210f, cs_mask, MOSI_pin, SCLK_pin, num_bits)
#print()

#io.write_spi("B", 0x0210f, cs_mask, MOSI_pin, SCLK_pin, num_bits)


#cr4.io_expander.write_bank_state("A", 0xFF)

