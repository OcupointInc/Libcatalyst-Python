# QC Example.py
from devices.queens_canyon import QueensCanyon, QCBank
from drivers.ftdi_driver import FTDISPIDriver
import time
from devices.queens_canyon import QueensCanyon

driver = FTDISPIDriver("configs/QC_FTDI.json")
qc = QueensCanyon(driver)

qc.set_bypass_enable(True)