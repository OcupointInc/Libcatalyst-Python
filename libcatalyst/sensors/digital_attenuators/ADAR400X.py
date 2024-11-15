import time

class ADAR400X():
    def __init__(self, driver, cs, hardware_address):
        self.max_time_delay = 255
        self.num_bits = 32
        self.driver = driver
        self.cs = cs
        self.hardware_address = hardware_address
        self.register_map = {i: None for i in range(0x3ED)}  # Initialize register map
        self.TDmode = [0, 0, 0, 0]

        #self.setup()

    def setup(self):
        self._soft_reset()
        self._soft_reset()
        self._set_direct_control()

    def _soft_reset(self):
        addr = 0x000
        data = 0xBD
        spi_word = (addr << 8) | data
        self.driver.write_spi(self.cs, spi_word, self.num_bits)

    def _set_direct_control(self):
        addr = 0x011
        data = 0x00
        spi_word = (addr << 8) | data
        self.driver.write_spi(self.cs, spi_word, self.num_bits)

    def set_time_delay(self, channel, time_delay):
        if channel < 0 or channel > 3:
            raise ValueError("Channel must be between 0 and 3.")
        
        if time_delay < 0 or time_delay > self.max_time_delay:
            raise ValueError(f"Time delay must be between 0 and {self.max_time_delay}.")
        
        # Address mapping: 0x100 + 2 * channel
        addr = 0x100 + channel * 2
        spi_word = (addr << 8) | time_delay

        self.driver.write_spi(self.cs, spi_word, self.num_bits)
        self.register_map[addr] = time_delay
        self._update_TDmode()

        return spi_word

    def set_time_delay_all(self, time_delay):
        for channel in range(4):
            self.set_time_delay(channel, time_delay)

    def set_time_delay_spectrum(self, channel):
        for delay in range(0, 256, 13):
            self.set_time_delay(channel, delay)
            time.sleep(2)

    def load_file(self, filename):
        with open(filename, "r") as file:
            for line in file:
                # Split and validate fields
                fields = line.strip().split(",")
                if len(fields) < 2:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue

                try:
                    # Parse address (24 bits) and data (8 bits) as hexadecimal
                    address, data = map(lambda x: int(x, 16), fields[:2])

                    # Ensure address and data fit within their respective ranges
                    if address > 0xFFFFFF:  # 24 bits for address
                        raise ValueError(f"Address {address:#X} exceeds 24-bit limit.")
                    if data > 0xFF:  # 8 bits for data
                        raise ValueError(f"Data {data:#X} exceeds 8-bit limit.")

                    # Construct the 32-bit SPI word: [24 bits of address | 8 bits of data]
                    spi_word = (address << 8) | data

                    # Write SPI word
                    self.driver.write_spi(self.cs, spi_word, 32)  # Send 32 bits
                    self.register_map[address] = data
                except ValueError as e:
                    print(f"Skipping line due to parsing or range error: {line.strip()}")
                    print(f"Error: {e}")


    def _update_TDmode(self):
        for i, addr in enumerate(range(0x100, 0x107, 2)):
            reg_value = self.register_map.get(addr)
            self.TDmode[i] = 0 if reg_value is None or reg_value <= 127 else 1

    def sleep_mode(self):
        self.load_file("./sleep.csv")
