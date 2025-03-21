import easy_scpi as scpi
import time

class Marker():
    def __init__(self, instrument, id) -> None:
        self.id = str(id)
        self.instrument = instrument
        self._freq_mhz = 0
        self.level_dbm = -100

    def get_peak(self):
        self.write("CALC:MARK:SEL " + self.id)
        self.write("CALC:MARK:SEL " + self.id)
        self.write("CALC:MARK:MAX")
        self.write("CALC:MARK:MAX")
        #self.get_freq_mhz()
        #self.get_freq_mhz()
        self.get_level_dbm()
        self.get_level_dbm()
        return self.freq_mhz, self.level_dbm
    
    def get_next_peak(self):
        self.write("CALCULATE:MARKER:UPDATE ON")
        self.write("CALC:MARK:MAX:next")
        next_peak_freq = self.instrument.query("CALC:MARK:X?")
        self.get_level_dbm()
        self.get_level_dbm()
        return next_peak_freq, self.level_dbm


    def get_freq_mhz(self):
        self.write("CALC:MARK:SEL " + self.id)
        self.freq_mhz = float(self.instrument.query("CALC:MARK:X?")) * 1e-6
        return self.freq_mhz

    def write(self, msg):
        self.instrument.write(msg)

    def get_level_dbm(self):
        self.write("CALC:MARK:SEL " + self.id)
        self.level_dbm = float(self.instrument.query("CALC:MARK:Y?"))
        return self.level_dbm

    @property
    def freq_mhz(self):
        return self._freq_mhz

    @freq_mhz.setter
    def freq_mhz(self, value):
        self._freq_mhz = value
        self.write("CALC:MARK:SEL " + self.id)
        cmd = "CALC:MARK:X " + str(value * 1e6)
        self.get_level_dbm()
        self.write(cmd)

class SpectrumAnalyser():
    def __init__(self, id) -> None:
        self.id = id
        self.instrument = scpi.Instrument(self.id)
        self.instrument.connect()
        self._center_freq_mhz = 3000
        self._span_mhz = 2000
        self._sweep_time_s = 0
        self._sweep_continious = 0
        self._RBW_mhz = 0
        self.MARK1 = Marker(self.instrument, 1)
        self._sweep_count = 1
        self._trace_mode = None
        self._ref_level_dbm = None


    @property
    def ref_level_dbm(self):
        if self.ref_level_dbm == None:
            self._ref_level_dbm = int(self.query("SENSe:SWEep:COUNt?"))
        return self._ref_level_dbm

    @ref_level_dbm.setter
    def ref_level_dbm(self, value):
        self._ref_level_dbm = value
        cmd = "DISP:TRAC:Y:RLEV " + str(value) + 'dBm'
        self.write(cmd)

    @property
    def sweep_count(self):
        if self._sweep_count == None:
            self._sweep_count = int(self.query("SENSe:SWEep:COUNt?"))
        return self._sweep_count

    @sweep_count.setter
    def sweep_count(self, value):
        self._sweep_count = value
        cmd = "SENSe:SWEep:COUNt " + str(value)
        self.write(cmd)


    @property
    def trace_mode(self):
        if self._trace_mode == None:
            self._trace_mode = self.query("DISPlay:WINDow:TRACe:MODE?")
        return self._trace_mode

    @trace_mode.setter
    def trace_mode(self, value):
        self._trace_mode = value
        cmd = "DISPlay:WINDow:TRACe:MODE " + str(value)
        self.write(cmd)


    @property
    def RBW_mhz(self):
        if self._RBW_mhz == 0:
            self._RBW_mhz = float(self.query("SENSe:BAND?")) * 1e-6
        return self._RBW_mhz

    @RBW_mhz.setter
    def RBW_mhz(self, value):
        self._RBW_mhz = value
        cmd = "SENSe:BAND " + str(value) + "MHz"
        self.write(cmd)

    def trigger_sweep(self):
        self.write("INIT:IMM")
        #time.sleep(self.sweep_time_s * 100)

    @property
    def sweep_continious(self):
        return self._sweep_continious

    @sweep_continious.setter
    def sweep_continious(self, value):
        self._sweep_continious = value
        cmd = "INIT:CONT " + str(value)
        self.write(cmd)

    @property
    def sweep_time_s(self):
        if self._sweep_time_s == 0:
            self._sweep_time_s = float(self.query("SWE:TIME?"))
            return self._sweep_time_s
        else:
            return self._sweep_time_s

    @sweep_time_s.setter
    def sweep_time_s(self, value):
        self._sweep_time_s = value
        cmd = "SWE:TIME " + str(value)
        self.write(cmd)
        self.MARK1.freq_mhz = value

    @property
    def center_freq_mhz(self):
        return self._center_freq_mhz

    @center_freq_mhz.setter
    def center_freq_mhz(self, value):
        self._center_freq_mhz = value
        cmd = "FREQ:CENT " + str(value * 1e6)
        self.write(cmd)

    def query(self, msg):
        return self.instrument.query(msg)

    def write(self, msg):
        self.instrument.write(msg)

    @property
    def span_mhz(self):
        return self._span_mhz

    @span_mhz.setter
    def span_mhz(self, value):
        self._span_mhz = value
        cmd = "FREQ:SPAN " + str(value * 1e6)
        self.write(cmd)