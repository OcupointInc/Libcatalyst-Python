from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.queens_canyon import QueensCanyon, QCBank
from libcatalyst.devices.keysight_p9375b import VisaManager, visa
import time

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/QC_FTDI.json", debug=False)

FlexDCA = visa.ResourceManager('C:/Windows/System32/visa64.dll')
vna_id = "TCPIP0::DESKTOP-RBPLMBQ::hislip_PXI0_CHASSIS2_SLOT1_INDEX0,4880::INSTR"
vna = VisaManager(vna_id)

qc = QueensCanyon(driver)

qc.set_bypass_enable(True)
qc.set_filter_bank(QCBank.Bypass)#

for i in range(30):
    qc.set_attenuation_db(i)
    time.sleep(0.5)