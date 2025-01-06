# CR4 Example.py
from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR2V2R1 import CR2V2R1
from libcatalyst.devices.sig_gen import SignalGenerator
from libcatalyst.devices.spec_ann import SpectrumAnalyser

import time
# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/CR2_FTDI.json", debug=False)

cr2 = CR2V2R1(driver)

# 4-6GHz
cr2.set_mixing_enable(True)
cr2.set_lowpass_filter_enable(True)
cr2.pll.set_pll_power("A", 63)
cr2.pll.set_pll_power("B", 63)
cr2.pll.tune(12000)

interface = "gpib1"
address = 4
sigen = SignalGenerator(f"{interface}::{address}::INSTR")

interface = "gpib0"
address = 20

#for i in range(8000, 10100, 100):
#    sigen.freq_mhz = i
#    time.sleep(0.1)


#spec_ann.center_freq_mhz = 3100

# Bypass Mode
def tune_band0():
    cr2.set_mixing_enable(False)
    cr2.set_lowpass_filter_enable(True)
    find_spurs(2000, 4000, 200)

# 4-6GHz Mode
def tune_band1():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(True)
    cr2.pll.tune(9000)
    find_spurs(5000, 6000, 200)

# 6-8GHz Mode
def tune_band2():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(True)
    cr2.pll.tune(10000)
    find_spurs(6000, 8000, 200)

# 6-8GHz Mode
def tune_band3():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(True)
    cr2.pll.tune(12000)
    find_spurs(8000, 10000, 200)

# 6-8GHz Mode
def tune_band4():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(True)
    cr2.pll.tune(14000)
    find_spurs(10000, 12000, 200)


# 6-8GHz Mode
def tune_band5():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(False)
    cr2.pll.tune(10000)
    find_spurs(12000, 14000, 200)

# 6-8GHz Mode
def tune_band6():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(False)
    cr2.pll.tune(12000)
    find_spurs(14000, 16000, 200)

# 6-8GHz Mode
def tune_band7():
    cr2.set_mixing_enable(True)
    cr2.set_lowpass_filter_enable(False)
    cr2.pll.tune(14000)
    find_spurs(16000, 18000, 200)


def find_spurs(start_freq_mhz, stop_freq_mhz, step_mhz):
    for freq in range(start_freq_mhz, stop_freq_mhz + step_mhz, step_mhz):
        # Set the RF Frequency
        sigen.freq_mhz = freq
        input(f"Step freq")
        

tune_band1()