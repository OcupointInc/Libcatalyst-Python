import pyvisa

class Keysight_e36311a:
    def __init__(self, resource_name):
        self.rm = pyvisa.ResourceManager()
        self.psu = self.rm.open_resource(resource_name)

    def write_voltage(self, channel, voltage):
        self.psu.write(f"VOLT {voltage}, (@{channel})")

    def write_current(self, channel, current):
        self.psu.write(f"CURR {current}, (@{channel})")

    def read_voltage(self, channel):
        return float(self.psu.query(f"MEAS:VOLT? (@{channel})"))

    def read_current(self, channel):
        return float(self.psu.query(f"MEAS:CURR? (@{channel})"))

    def output_enable(self, channel):
        self.psu.write(f"OUTP ON, (@{channel})")

    def output_disable(self, channel):
        self.psu.write(f"OUTP OFF, (@{channel})")

    def query_output_state(self, channel):
        state = self.psu.query(f"OUTP? (@{channel})")
        return bool(int(state))

    def close(self):
        self.psu.close()
        self.rm.close()