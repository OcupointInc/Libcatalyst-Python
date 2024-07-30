class ADMV8818():
    def __init__(self, driver, cs):
        self.driver = driver
        self.cs = cs

    def set_switches(self, lpf_band, hpf_band):
        address = 0x0020  # 16 bits
        sw_write = 0b11   # 2 bits, always set to write mode

        if not (0 <= lpf_band <= 4):
            raise ValueError("LPF band setting needs to be from 0 to 4")

        if not (0 <= hpf_band <= 4):
            raise ValueError("HPF band setting needs to be from 0 to 4")

        # Combine all parts into a single 24-bit word
        combined_word = (address << 8) | (sw_write << 6) | (lpf_band << 3) | (hpf_band)

        # Ensure the MSB is 0, which is already handled as we are using a 24-bit word
        return combined_word
