# QC Example.py
from devices.queens_canyon import QueensCanyon, QCBank
from drivers.interface import MockDriver
from devices.queens_canyon import QueensCanyon

driver = MockDriver("device_id", "configs/QC_FTDI.json")
qc = QueensCanyon(driver)

qc.set_attenuation_db(30.5)