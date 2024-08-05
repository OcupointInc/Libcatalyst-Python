# ADRF5720 Control
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from devices.spec_ann import SpectrumAnalyser
from devices.sig_gen import SignalGenerator
import pyvisa
from easy_scpi import Instrument
rm = pyvisa.ResourceManager('@py')
spec_ann_id = 'GPIB1::4::INSTR'
sig_gen_id = 'GPIB0::4::INSTR'

spec = SpectrumAnalyser(spec_ann_id)

spec.center_freq_mhz = 3000
spec.span_mhz(2000)