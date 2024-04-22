# QC Example.py
from devices.QC import QC, QCBank
from drivers.interface import MockDriver

driver = MockDriver("device_id", "configs/QC_FTDI.json")

qc = QC(driver)
qc.set_attenuation_db(15.5)
qc.read_attenuation_db()
qc.set_bypass_enable(0)
qc.set_filter_bank(QCBank.LPF_1GHz)