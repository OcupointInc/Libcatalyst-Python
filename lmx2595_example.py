# QC Example.py
from devices.queens_canyon import QueensCanyon, QCBank
from drivers.interface import MockDriver
from sensors.pll.LMX2595 import LMX2595

driver = MockDriver("device_id", "configs/QC_FTDI.json")
pll = LMX2595(driver, "pll_d_cs")
pll.tune_pll(12000)
pll.tune_pll(14000)