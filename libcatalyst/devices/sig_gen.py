import easy_scpi as scpi
import time

class SignalGenerator():
    def __init__(self, id) -> None:
        self.id = id
        self.instrument = scpi.Instrument(self.id)
        self.instrument.connect()
        self._freq_mhz = 3000
        self._power_dbm = -10

    @property
    def freq_mhz(self):
        return self._freq_mhz

    @freq_mhz.setter
    def freq_mhz(self, value):
        self._freq_mhz = value
        cmd = "SOUR:FREQ " + str(value) + " MHz"
        self.write(cmd)

    def write(self, msg):
        self.instrument.write(msg)

    def query(self, msg):
        return self.instrument.query(msg)

    @property
    def power_dbm(self):
        return self._power_dbm

    @power_dbm.setter
    def power_dbm(self, value):
        self._power_dbm = value
        cmd = "SOUR:POW " + str(value) + " dBm"
        self.write(cmd)

