# QC Example.py
from devices.queens_canyon import QueensCanyon, QCBank
from drivers.ftdi_driver import FTDISPIDriver
import time
from devices.queens_canyon import QueensCanyon

driver = FTDISPIDriver("configs/QC_FTDI.json", debug=True)
qc = QueensCanyon(driver)

for i in range(31):
    qc.set_attenuation_db(i)
    input("Press enter for the next value")