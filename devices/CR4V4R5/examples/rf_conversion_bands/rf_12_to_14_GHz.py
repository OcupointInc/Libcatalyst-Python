from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5

# Initialize driver and device
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=True)
cr4 = CR4V4R5(driver, clock_frequency_mhz=100)

# Set the attenuation and RF filter settings
cr4.set_attenuation_db(channels=[1,2,3,4], attenuation_db=0)
cr4.tune_filters(lpf_switch=0, lpf_band=0, hpf_switch=0, hpf_band=0)

# Set the switch state, single or dual convert
cr4.set_switch("AB", "single")
cr4.set_switch("CD", "single")

# Tune the downconvert PLLs in MHz
cr4.tune_pll("D", 10000)
cr4.tune_pll("B", 10000)

# Tune the upconvert PLLs in MHz
cr4.tune_pll("A", 0)
cr4.tune_pll("C", 0)