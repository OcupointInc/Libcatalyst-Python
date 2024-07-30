# QC Example.py
import time
from drivers.ftdi_driver import FTDISPIDriver
from drivers.mock import MockDriver
from devices.cr4_v4r4 import CR4V4R4
from sensors.rf_filters.ADMV8818 import ADMV8818
from sensors.io_expanders.MCP23S17T import MCP23S17T
driver = MockDriver("configs/CR4_V4_FTDI.json")

io = MCP23S17T(driver, "CS_PRF_IO")

filt = ADMV8818(driver, "CS_PRF_IO")
#data = filt.set_switches(1,2)

#print(hex(data))

io.set_bank_direction("A", 0xFF)
io.set_bank_direction("B", 0x1E)
io.write_bank_state("A", 0x0F)
io.write_spi("B", 0x02112, 0x30, 0x08, 0x04, 24)
io.write_spi("B", 0x020ca, 0x30, 0x08, 0x04, 24)