import pyvisa
import json
import time
import sys

class Keysight_e36311a:
    def __init__(self, config_file):
        self.rm = pyvisa.ResourceManager()
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.psu = self.rm.open_resource(self.config["psu"]["resource_id"], timeout=10000)
        
        self.channels = 3
        print(self.get_device_id())
        self._setup()


    def get_device_id(self):
        return self.psu.query("*IDN?").strip()

    def _setup(self):
        # Initalize all of the channels
        for channel in self.config["psu"]["channels"]:
            # Check to see if its already on
            if self.query_output_state(channel["index"]):
                self.output_disable(channel["index"])

            self.write_voltage(channel["index"], channel["voltage"])
            self.write_current(channel["index"], channel["current_limit"])
            self.output_enable(channel["index"])
            
            time.sleep(0.5)
            # Verify its drawing the correct power/current
            voltage = self.read_voltage(channel["index"])
            current = self.read_current(channel["index"])
            err = False
            vtp = 0.2 # Voltage tolerance percentage
            ctp = 0.1 # Current tolerance percentage

            if not self.is_within_percentage(channel["voltage"], voltage, 0.1):
                print(f"Error, the voltage was reading {voltage} when it should be from {round(channel['voltage'] * (1 + vtp), 3)} to {round(channel['voltage'] * (1 - vtp), 3)}. Shutting down.")
                self.output_disable(channel["index"])
                err = True

            if not self.is_within_percentage(channel["starting_current"], current, 0.1):
                print(f"Error, the current was reading {current} when it should be from {round(channel['starting_current'] * (1 + ctp), 3)} to {round(channel['starting_current'] * (1 - ctp), 3)} amps. Shutting down.")
                self.output_disable(channel["index"])
                err = True

            if err:
                sys.exit()

            time.sleep(0.25)




        


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

    def is_within_percentage(self, original_value, value, percentage):
        """
        Checks if a value is within a certain percentage of an original value.
        
        Parameters:
        original_value (float): The original value to compare against.
        value (float): The value to check.
        percentage (float): The percentage (as a decimal) that the value should be within.
        
        Returns:
        bool: True if the value is within the specified percentage, False otherwise.
        """
        lower_bound = original_value * (1 - percentage)
        upper_bound = original_value * (1 + percentage)
        return lower_bound <= value <= upper_bound
