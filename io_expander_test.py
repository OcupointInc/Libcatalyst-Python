# QC Example.py
import time
from drivers.ftdi_driver import FTDISPIDriver
from drivers.mock import MockDriver
from sensors.io_expanders.MCP23S17T import MCP23S17T
from sensors.digital_attenuators.HMC1018A import HMC1018A
driver = MockDriver("configs/CR4_V4_FTDI.json")

io = MCP23S17T(driver, "CS_PRF_IO")

io.write_spi("A", 31, 0x0F, 0x20, 0x10, 6)