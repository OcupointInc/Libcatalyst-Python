# CR4 Example.py
from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.sensors.digital_attenuators.ADAR400X import ADAR400X

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/ADAR400X_FTDI.json", debug=True)

adar = ADAR400X(driver, "CS", 0)

adar.load_file("./sleep.csv")

adar.sleep_mode()