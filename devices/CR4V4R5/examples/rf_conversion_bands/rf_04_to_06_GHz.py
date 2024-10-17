from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5

# Initialize driver and device
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

attenuation_db = 0
rf_filter_settings = (0,0,0,0)


pll_b_frequency_mhz  = 8000
pll_d_frequency_mhz  = 8000

pll_a_frequency_mhz  = 0
pll_c_frequency_mhz  = 0

sw_ab_state = "single"
sw_cd_state = "single"

# Set all PLLs to reset mode and max power
for name, pll in cr4.plls.items():
    cr4.pll_reset_enable(name, 1)
    pll.set_pll_power(name, 63)

cr4.set_attenuation_db([1,2,3,4], attenuation_db)
cr4.tune_filters(*rf_filter_settings)

cr4.set_switch("AB", sw_ab_state)
cr4.set_switch("CD", sw_cd_state)

# Set all PLLs to reset mode
for name, pll in cr4.plls.items():
    cr4.pll_reset_enable(name, 1)

# Tune the downconvert PLLs
if pll_d_frequency_mhz != 0:
    cr4.tune_pll("D", pll_d_frequency_mhz)

if pll_b_frequency_mhz != 0:
    cr4.tune_pll("B", pll_b_frequency_mhz)

# Tune the upconvert PLLs
if pll_a_frequency_mhz != 0:
    cr4.tune_pll("A", pll_a_frequency_mhz)

if pll_c_frequency_mhz != 0:
    cr4.tune_pll("C", pll_c_frequency_mhz)