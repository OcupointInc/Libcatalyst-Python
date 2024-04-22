# QC Example.py
from devices.queens_canyon import QueensCanyon, QCBank
from drivers.interface import MockDriver
from sensors.digital_attenuators.ADAR400X import ADAR400X

driver = MockDriver("device_id", "configs/QC_FTDI.json")
adar = ADAR400X(driver, "adar400x_cs", 0)
#adar.set_attenuation_db(0, 10)
#adar.set_time_delay(0, 10)