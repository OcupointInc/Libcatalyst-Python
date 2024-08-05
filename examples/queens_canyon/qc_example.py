# ADRF5720 Control
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from sensors.digital_attenuators.ADRF5720 import ADRF5720
from drivers.ftdi_driver import FTDISPIDriver

driver = FTDISPIDriver("configs/QC_FTDI.json")
attenuator = ADRF5720(driver, "attenuator_cs")

for i in range(31):
    attenuator.set_attenuation_db(i)
    input("Press enter for the next value")