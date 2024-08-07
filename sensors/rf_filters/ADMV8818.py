class ADMV8818():
    def __init__(self, driver, cs):
        self.driver = driver
        self.cs = cs

    def tune(self, lpf_switch_band, lpf_filter_state, hpf_switch_band, hpf_filter_band):
        """
        Tune the ADMV8818 by setting both switch and filter settings.
        
        Parameters:
        - lpf_switch_band (int): LPF switch band setting (0-4)
        - lpf_filter_state (int): LPF filter state setting (0-15)
        - hpf_switch_band (int): HPF switch band setting (0-4)
        - hpf_filter_band (int): HPF filter band setting (0-15)
        
        Returns:
        - tuple: (switch_word, filter_word) - The 24-bit words written to the device
        """
        # Set the switches
        switch_word = self.set_switches(lpf_switch_band, hpf_switch_band)
        
        # Set the filter settings
        filter_word = self.set_filter_setting(lpf_filter_state, hpf_filter_band)
        
        return (switch_word, filter_word)

    def set_switches(self, lpf_band, hpf_band):
        """
        Set the switch settings for LPF and HPF.
        
        Parameters:
        - lpf_band (int): LPF band setting (0-4)
        - hpf_band (int): HPF band setting (0-4)
        
        Returns:
        - int: The 24-bit word written to the device
        """
        address = 0x0020  # 16 bits
        sw_write = 0b11   # 2 bits, always set to write mode

        if not (0 <= lpf_band <= 4):
            raise ValueError("LPF band setting needs to be from 0 to 4")

        if not (0 <= hpf_band <= 4):
            raise ValueError("HPF band setting needs to be from 0 to 4")

        # Combine all parts into a single 24-bit word
        combined_word = (address << 8) | (sw_write << 6) | (lpf_band << 3) | (hpf_band)
        
        self.driver.write_spi(self.cs, combined_word, 24)
        return combined_word
    
    def set_filter_setting(self, lpf_band, hpf_band):
        """
        Set the filter settings for LPF and HPF.
        
        Parameters:
        - lpf_band (int): LPF band setting (0-15)
        - hpf_band (int): HPF band setting (0-15)
        
        Returns:
        - int: The 24-bit word written to the device
        """
        address = 0x0021  # 16 bits

        if not (0 <= lpf_band <= 15):
            raise ValueError("LPF band setting needs to be from 0 to 15")

        if not (0 <= hpf_band <= 15):
            raise ValueError("HPF band setting needs to be from 0 to 15")

        # Combine all parts into a single 24-bit word
        combined_word = (address << 8) | (lpf_band << 4) | (hpf_band)
        
        self.driver.write_spi(self.cs, combined_word, 24)
        return combined_word
    
    def set_spi_mode(self):
        """Set the SPI mode for communication."""
        self.driver.write_spi(self.cs, 0x00003C, 24)

    def reset(self):
        """Reset the device."""
        self.driver.write_spi(self.cs, 0x000081, 24)