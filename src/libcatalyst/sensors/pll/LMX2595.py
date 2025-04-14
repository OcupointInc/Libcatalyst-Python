# LMX2595.py
import math
import time # Added for sleep

# Updated register defaults based on recommendations
# Key changes:
# R20: VCO_SEL_FORCE (bit 10) set to 0 (was 1) -> Allows internal calibration to select VCO core
# R8:  VCO_DACISET_FORCE (bit 14) set to 0 (was 1) -> Allows internal calibration for amplitude
# R44: OUTA_PWR (bits 13:8) set to 50 (0x32) (was 63), OUTA_PD (bit 6) set to 0 (was 1) -> Enable Output A, reduce power setting
# R45: OUTB_PWR (bits 5:0) set to 50 (0x32) (was 63) -> Reduce power setting
registers = {
    "R112": 0x700000, # Readback only
    "R111": 0x6F0000, # Readback only
    "R110": 0x6E0000, # Readback only
    "R109": 0x6D0000, # Ramping - Default OK if not used
    "R108": 0x6C0000, # Ramping - Default OK if not used
    "R107": 0x6B0000, # Ramping - Default OK if not used
    "R106": 0x6A0000, # Ramping - Default OK if not used
    "R105": 0x690021, # Ramping - Default OK if not used
    "R104": 0x680000, # Ramping - Default OK if not used
    "R103": 0x670000, # Ramping - Default OK if not used
    "R102": 0x663F80, # Ramping - Default OK if not used
    "R101": 0x650011, # Ramping - Default OK if not used
    "R100": 0x640000, # Ramping - Default OK if not used
    "R99":  0x630000, # Ramping - Default OK if not used
    "R98":  0x620200, # Ramping - Default OK if not used
    "R97":  0x610888, # Ramping - Default OK if not used
    "R96":  0x600000, # Ramping - Default OK if not used
    "R95":  0x5F0000, # Reserved
    "R94":  0x5E0000, # Reserved
    "R93":  0x5D0000, # Reserved
    "R92":  0x5C0000, # Reserved
    "R91":  0x5B0000, # Reserved
    "R90":  0x5A0000, # Reserved
    "R89":  0x590000, # Reserved
    "R88":  0x580000, # Reserved
    "R87":  0x570000, # Reserved
    "R86":  0x560000, # Ramping Limit Low [15:0] - Default OK if not used
    "R85":  0x55E700, # Ramping Limit Low [31:16] - Default OK if not used
    "R84":  0x540001, # Ramping Limit Low [32] - Default OK if not used
    "R83":  0x530000, # Ramping Limit High [15:0] - Default OK if not used
    "R82":  0x523200, # Ramping Limit High [31:16] - Default OK if not used
    "R81":  0x510000, # Ramping Limit High [32] - Default OK if not used
    "R80":  0x506666, # Ramping Threshold [15:0] - Default OK if not used
    "R79":  0x4F0026, # Ramping Threshold [31:16] - Default OK if not used
    "R78":  0x4E0003, # Ramping Threshold [32], QUICK_RECAL=0, VCO_CAPCTRL_STRT=1 (OK default)
    "R77":  0x4D0000, # Reserved
    "R76":  0x4C000C, # Reserved
    "R75":  0x4B0800, # CHDIV = 0 (Divide by 2)
    "R74":  0x4A0000, # SYSREF - Default OK if not used
    "R73":  0x49003F, # SYSREF - Default OK if not used
    "R72":  0x480001, # SYSREF - Default OK if not used
    "R71":  0x470081, # SYSREF - Default OK if not used
    "R70":  0x46C350, # MASH Reset Count - Default OK if not used
    "R69":  0x450000, # MASH Reset Count - Default OK if not used
    "R68":  0x4403E8, # MASH Reset Count - Default OK if not used
    "R67":  0x430000, # Reserved
    "R66":  0x4201F4, # Reserved
    "R65":  0x410000, # Reserved
    "R64":  0x401388, # Reserved
    "R63":  0x3F0000, # Reserved
    "R62":  0x3E0322, # Reserved
    "R61":  0x3D00A8, # Reserved
    "R60":  0x3C0000, # Lock Detect Delay - Default OK
    "R59":  0x3B0001, # Lock Detect Type - Default OK
    "R58":  0x3A9001, # INPIN_IGNORE=1 (Pins ignored), other settings default OK
    "R57":  0x390020, # Reserved
    "R56":  0x380000, # Reserved
    "R55":  0x370000, # Reserved
    "R54":  0x360000, # Reserved
    "R53":  0x350000, # Reserved
    "R52":  0x340820, # Reserved
    "R51":  0x330080, # Reserved
    "R50":  0x320000, # Reserved
    "R49":  0x314180, # Reserved
    "R48":  0x300300, # Reserved
    "R47":  0x2F0300, # Reserved
    "R46":  0x2E07FD, # OUTB_MUX=1 (VCO) - Default OK
    "R45":  0x2DC832, # *** UPDATED *** OUTA_MUX=1 (VCO), OUT_ISET=0, OUTB_PWR=50 (0x32)
    "R44":  0x2C3220, # *** UPDATED *** OUTA_PWR=50 (0x32), OUTB_PD=0, OUTA_PD=0 (Output A Enabled), MASH_RESET_N=1, MASH_ORDER=0 (Integer)
    "R43":  0x2B0000, # PLL_NUM [15:0] - Default 0 (Integer)
    "R42":  0x2A0000, # PLL_NUM [31:16] - Default 0 (Integer)
    "R41":  0x290000, # MASH_SEED [15:0] - Default 0
    "R40":  0x280000, # MASH_SEED [31:16] - Default 0
    "R39":  0x2703E8, # PLL_DEN [15:0] - Default 1000 (Need 2^32-1 for fractional, OK for Int)
    "R38":  0x260000, # PLL_DEN [31:16] - Default 0
    "R37":  0x250104, # MASH_SEED_EN=0, PFD_DLY_SEL=1 (Set dynamically in code)
    "R36":  0x240032, # PLL_N [15:0] (Set dynamically in code, default 50 here)
    "R35":  0x230004, # Reserved
    "R34":  0x220000, # PLL_N [18:16] (Set dynamically in code)
    "R33":  0x211E21, # Reserved
    "R32":  0x200393, # Reserved
    "R31":  0x1F43EC, # SEG1_EN=1 (Required if CHDIV > 2), CHDIV_DIV2=1 - Default OK
    "R30":  0x1E318C, # Reserved
    "R29":  0x1D318C, # Reserved
    "R28":  0x1C0488, # Reserved
    "R27":  0x1B0002, # VCO2X_EN=0 (Use VCO Doubler if needed)
    "R26":  0x1A0DB0, # Reserved
    "R25":  0x190C2B, # DBLR_IBIAS_CTRL1=3115 (New recommended value)
    "R24":  0x18071A, # Reserved
    "R23":  0x17007C, # Reserved
    "R22":  0x160001, # Reserved
    "R21":  0x150401, # Reserved
    "R20":  0x14A048, # *** UPDATED *** VCO_SEL=5 (Initial, not forced), VCO_SEL_FORCE=0 (Calibration selects core)
    "R19":  0x1327B7, # VCO_CAPCTRL = 183 (Used if forced, default OK)
    "R18":  0x120064, # Reserved
    "R17":  0x11012C, # VCO_DACISET_STRT = 300 (OK default)
    "R16":  0x100080, # VCO_DACISET = 128 (Used if forced, default OK)
    "R15":  0x0F064F, # Reserved
    "R14":  0x0E1E70, # CPG=7 (15mA) - Default OK
    "R13":  0x0D4000, # Reserved
    "R12":  0x0C5001, # PLL_R_PRE=1 (Bypass) - Default OK
    "R11":  0x0B0018, # PLL_R=1 (Bypass) - Default OK
    "R10":  0x0A10D8, # MULT=1 (Bypass) - Default OK
    "R9":   0x091604, # OSC_2X=1 (Set dynamically in code) - Default OK
    "R8":   0x002000, # *** UPDATED *** VCO_DACISET_FORCE=0, VCO_CAPCTRL_FORCE=0
    "R7":   0x0740B2, # OUT_FORCE=1 (Needed if OUT_MUTE=0)
    "R6":   0x06C802, # Reserved
    "R5":   0x0500C8, # Reserved
    "R4":   0x040A43, # ACAL_CMP_DLY=10 (Set dynamically) - Default OK
    "R3":   0x030642, # Reserved
    "R2":   0x020500, # Reserved
    "R1":   0x010808, # CAL_CLK_DIV=3 (Slowest, safest) - Default OK
    "R0":   0x00251C, # RAMP_EN=0, VCO_PHASE_SYNC=0, OUT_MUTE=0, FCAL Adj/EN set dynamically - Default OK initial state
}

class LMX2595():
    def __init__(self, driver, cs, clock_frequency_mhz = 100):
        self.driver = driver
        self.cs = cs
        self.max_freq_mhz = 20000 # Datasheet max is 20GHz with doubler
        self.min_freq_mhz = 10     # Datasheet min is 10MHz
        self.freq_mhz = 8000       # Default initial frequency
        self.registers = registers.copy() # Use a copy to allow instance modification

        self.osc_freq = clock_frequency_mhz
        # Determine initial PFD frequency based on clock and doubler possibility
        self._set_osc_doubler() # Determine if doubler is needed and set initial state
        self.pfd_freq = self.osc_freq * 2 if self.osc_doubler_enabled else self.osc_freq

        # Set MASH_ORDER based on register default R44[2:0] = 0
        self.mash_order = (self.registers["R44"] & 0x07)

        print(f"LMX2595 Initialized: OSC Freq={self.osc_freq} MHz, PFD Freq={self.pfd_freq} MHz")

    def set_register_bits_with_mask(self, register, mask, values):
        """ Sets specific bits in a register value using a mask. """
        if register not in self.registers:
             raise ValueError(f"Register {register} not found.")
        
        # Ensure mask and values are within the valid range (24 bits for full SPI word)
        if mask < 0 or mask > 0xFFFFFF:
            raise ValueError("Invalid mask value. It should be a 24-bit integer.")
        
        if values < 0 or values > 0xFFFFFF:
             raise ValueError("Invalid values. It should be a 24-bit integer.")

        # Get current register value (full 24-bit SPI word)
        current_value = self.registers[register]
        
        # Clear the bits specified by the mask
        cleared_value = current_value & (~mask)
        
        # Set the bits using the provided values (ensure values align with mask)
        # We assume 'values' here contains the bits already shifted to their correct positions within the mask
        self.registers[register] = cleared_value | (values & mask)


    def _set_osc_doubler(self):
        """ Automatically enables/disables OSC_2X based on osc_freq """
        # Datasheet: OSCin doubler doubles input reference frequency up to 400 MHz.
        # Enable if osc_freq < 200 MHz to potentially reach higher PFD frequencies.
        # Max input freq without doubler is 1400 MHz. Max with doubler is 200 MHz.
        state = 0 # Default disabled
        if self.osc_freq < 200: # Enable doubler for lower frequencies
             state = 1
        
        self.osc_doubler_enabled = bool(state)
        print(f"OSC Doubler {'Enabled' if self.osc_doubler_enabled else 'Disabled'} based on OSC Freq={self.osc_freq} MHz.")
        # R9[12] is OSC_2X bit
        self.set_register_bits_with_mask("R9", (1 << 12), (state << 12))
        # Update PFD frequency
        self.pfd_freq = self.osc_freq * 2 if self.osc_doubler_enabled else self.osc_freq


    # def unlock(self): # This function name was confusing, use power_down() or power_up()
    #     """ Powers down the device (useful before reconfiguration maybe?) """
    #     print("Powering down LMX2595 (via POWERDOWN bit)...")
    #     self.set_register_bits_with_mask("R0", 0x01, 1) # Set POWERDOWN bit
    #     self._write_register("R0")

    def mute_port(self, port, value):
        """ Mutes (powers down) or unmutes an output port """
        port_str = f"Output {port.upper()}"
        action = "Muting" if value else "Unmuting"
        print(f"{action} {port_str}...")
        
        if port.upper() == "A":
            # R44[6] is OUTA_PD
            mask = (1 << 6)
            bit_value = (1 << 6) if value else 0
            self.set_register_bits_with_mask("R44", mask, bit_value)
            self._write_register("R44")
        elif port.upper() == "B":
             # R44[7] is OUTB_PD
            mask = (1 << 7)
            bit_value = (1 << 7) if value else 0
            self.set_register_bits_with_mask("R44", mask, bit_value)
            self._write_register("R44")
        else:
            print(f"Warning: Invalid port '{port}' for mute operation.")


    def set_osc_freq_mhz(self, freq_mhz):
        """ Updates the stored oscillator frequency and related settings """
        print(f"Setting OSC Frequency to {freq_mhz} MHz.")
        self.osc_freq = freq_mhz
        self._set_osc_doubler()    # Recalculate if doubler should be used
        self._set_ACAL_CMP_DLY()   # Update based on new OSC freq
        self._set_FCAL_HPFD_ADJ()  # Update based on new PFD freq
        self._write_register("R9") # Write updated OSC_2X setting
        self._write_register("R4") # Write updated ACAL_CMP_DLY
        self._write_register("R0") # Write updated FCAL settings

    def _set_ACAL_CMP_DLY(self):
        """ Sets R4[15:8] ACAL_CMP_DLY based on Fsmclk recommendation """
        # Fsmclk = Fosc / 2^CAL_CLK_DIV. CAL_CLK_DIV is R1[2:0]. Default R1=0x010808 -> CAL_CLK_DIV=3 -> Div=8
        cal_clk_div_val = self.registers["R1"] & 0x07
        fsmclk = self.osc_freq / (2**cal_clk_div_val)
        # Recommendation: ACAL_CMP_DLY > Fsmclk / 10 MHz. Minimum 10. Default 10.
        # Let's use default 10 for simplicity unless very slow clock
        val = 10
        # Recommendation from datasheet: If lock time is NOT a concern, set CAL_CLK_DIV=3.
        # If time IS a concern, set ACAL_CMP_DLY >= 25. Let's keep it simple at 10 for now.
        # val = max(10, math.ceil(fsmclk / 10)) # Optional calculation
        print(f"Setting ACAL_CMP_DLY (R4[15:8]) to {val}.")
        self.set_register_bits_with_mask("R4", 0xFF00, val << 8)


    def _set_FCAL_HPFD_ADJ(self):
        """ Sets R0[8:7] FCAL_HPFD_ADJ based on PFD frequency """
        val = 0
        # Use the calculated PFD frequency (considers OSC_2X)
        freq = self.pfd_freq
        if freq <= 100:
            val = 0
        elif 100 < freq <= 150:
            val = 1
        elif 150 < freq <= 200:
            val = 2
        else: # freq > 200
             val = 3
        print(f"Setting FCAL_HPFD_ADJ (R0[8:7]) to {val} based on PFD Freq={freq} MHz.")
        self.set_register_bits_with_mask("R0", 0x0180, val << 7)
        # Note: FCAL_LPFD_ADJ (R0[6:5]) adjustment is usually 0 for PFD >= 10 MHz. We'll assume PFD is high enough.


    def set_pll_power(self, port, power):
        """ Sets output power level for port A or B """
        if power < 0 or power > 63:
            raise ValueError("Power level must be from 0 - 63")

        port_upper = port.upper()
        print(f"Setting Output {port_upper} Power to {power}.")
        if port_upper == "A":
             # R44[13:8] is OUTA_PWR
            self.set_register_bits_with_mask("R44", 0x3F00, power << 8)
            self._write_register("R44")
        elif port_upper == "B":
            # R45[5:0] is OUTB_PWR
            self.set_register_bits_with_mask("R45", 0x003F, power)
            self._write_register("R45")
        else:
             print(f"Warning: Invalid port '{port}' for set_pll_power.")


    def _write_register(self, register_id):
        """ Writes a single register value (24-bit SPI word) to the device """
        if register_id not in self.registers:
             print(f"Warning: Attempted to write unknown register {register_id}")
             return
        #print(f"Writing {register_id}: 0x{self.registers[register_id]:06X}")
        self.driver.write_spi(self.cs, self.registers[register_id], 24)

    def _write_all_registers(self):
        """ Writes all registers in recommended reverse order """
        print("Writing all registers...")
        # Program registers in REVERSE order from highest to lowest address (R112 down to R0)
        # Skip readback registers (R107-R112)
        register_keys = sorted(self.registers.keys(), key=lambda r: int(r[1:]), reverse=True)
        for reg_id in register_keys:
             if int(reg_id[1:]) < 107: # Only write R0-R106
                 self._write_register(reg_id)
                 # Small delay might be needed between writes depending on SPI speed and driver
                 # time.sleep(0.001) # Example: 1ms delay


    def reset_chip(self):
        """ Performs a software reset """
        print("Performing software reset...")
        # Set RESET bit (R0[1])
        original_r0 = self.registers["R0"]
        reset_val = original_r0 | (1 << 1)
        self.driver.write_spi(self.cs, reset_val, 24)
        time.sleep(0.001) # Short delay might be prudent
        # Clear RESET bit (R0[1]), keeping other bits as intended in default dict
        # Important: Use the *intended* default R0 value, not the potentially modified one
        self.driver.write_spi(self.cs, registers["R0"], 24) # Write initial default R0
        time.sleep(0.001)
        self.registers["R0"] = registers["R0"] # Restore R0 in our shadow registers


    def set_PLL_N(self, vco_freq_mhz):
        """ Calculates and sets PLL_N based on target *VCO* frequency """
        # VCO range is 7.5 GHz to 15 GHz (or 20 GHz with doubler enabled)
        # This function assumes target freq is VCO freq. Output freq might be divided.
        
        # Ensure we are calculating based on the actual PFD frequency
        current_pfd_freq = self.osc_freq * 2 if self.osc_doubler_enabled else self.osc_freq
        if current_pfd_freq == 0:
             print("Error: PFD Frequency is zero.")
             return

        # Calculate PLL_N
        # Note: Integer mode calculation N = fVCO / fPFD
        pll_n_val = math.floor(vco_freq_mhz / current_pfd_freq)
        print(f"Calculated PLL_N = {pll_n_val} for VCO Freq={vco_freq_mhz} MHz, PFD Freq={current_pfd_freq} MHz.")

        # Update R36 (PLL_N[15:0]) and R34 (PLL_N[18:16])
        self.set_register_bits_with_mask("R36", 0xFFFF, pll_n_val & 0xFFFF)
        self.set_register_bits_with_mask("R34", 0x0007, (pll_n_val >> 16) & 0x07)

        # Update PFD_DLY_SEL based on VCO frequency and MASH_ORDER
        self.set_PFD_DLY_SEL(vco_freq_mhz)


    def set_PFD_DLY_SEL(self, vco_freq_mhz):
        """ Sets R37[13:8] PFD_DLY_SEL based on VCO freq and MASH order """
        reg_id = "R37"
        mash_o = self.mash_order # Assumes self.mash_order reflects R44 setting
        pfd_dly = 1 # Default minimum

        # Determine PFD_DLY_SEL based on Table 2 from datasheet
        if mash_o == 0: # Integer
            if vco_freq_mhz <= 12500: pfd_dly = 1
            else: pfd_dly = 2
        elif mash_o == 1:
            if vco_freq_mhz <= 10000: pfd_dly = 1
            elif 10000 < vco_freq_mhz <= 12500: pfd_dly = 2
            else: pfd_dly = 3
        elif mash_o == 2:
            if vco_freq_mhz <= 10000: pfd_dly = 2
            else: pfd_dly = 3
        elif mash_o == 3:
            if vco_freq_mhz <= 10000: pfd_dly = 3
            else: pfd_dly = 4
        elif mash_o == 4:
            if vco_freq_mhz <= 10000: pfd_dly = 5
            else: pfd_dly = 6
        else:
             print(f"Warning: Invalid MASH Order {mash_o} for PFD_DLY_SEL calculation.")
             pfd_dly = 1 # Fallback

        print(f"Setting PFD_DLY_SEL (R37[13:8]) to {pfd_dly} for VCO Freq={vco_freq_mhz} MHz, MASH Order={mash_o}.")
        self.set_register_bits_with_mask(reg_id, 0x3F00, pfd_dly << 8)


    def read_register(self, register_address):
        """ Reads a register value from the LMX2595 """
        print(f"Reading register {register_address}")
        
        # 1. Ensure MUXout is configured for readback (R0[2] = 0)
        muxout_mask = (1 << 2)
        self.set_register_bits_with_mask("R0", muxout_mask, 0) # Set MUXOUT_LD_SEL to 0
        self._write_register("R0")

        # Convert register address string (e.g., "R7") to integer address
        try:
            reg_addr_int = int(register_address[1:])
            if not (0 <= reg_addr_int <= 127):
                 raise ValueError("Register address out of range (0-127)")
        except (ValueError, IndexError):
             print(f"Error: Invalid register address format '{register_address}'. Use 'Rx'.")
             return None

        # 2. Prepare the read command (24 bits: R/W=1, Addr[6:0], Data=0x0000)
        # R/W bit is bit 23, Address is bits 22:16
        read_command = (1 << 23) | (reg_addr_int << 16)
        # print(f"Sending Read command: 0x{read_command:06X}")

        # 3. Perform SPI transaction (Send read command, receive data on MUXout via SDI during *next* transaction)
        # The LMX2595 datasheet implies readback happens on MUXout pin, clocked by SCK *after* CSB goes low
        # for the *next* transaction, or potentially during the read command itself if the SPI driver handles MISO (MUXout).
        # This implementation assumes the driver's exchange_spi handles MISO correctly during the transaction.
        # If MUXout needs separate handling, this needs adjustment.
        
        # We send the read command and simultaneously read data clocked out from the *previous* command (if any).
        # The actual data for *this* read command will be available on MUXout for the *next* SPI cycle.
        # TI examples often show sending the read command, then sending R0 (or another command) to clock out the data.
        
        # Send read command
        self.driver.write_spi(self.cs, read_command, 24)
        
        # Send a dummy write (e.g., R0) to clock out the readback data on MUXout/MISO
        # Assume driver.read_spi reads MISO while sending dummy data
        read_data = self.driver.read_spi(self.cs, self.registers["R0"], 24) # Send R0, read MISO

        # The read data should contain the 16 bits from the requested register
        result = read_data & 0xFFFF
        print(f"Read {register_address} (command 0x{read_command:06X}), Raw data received during next cycle: 0x{read_data:06X}, Parsed result: 0x{result:04X}")

        return result


    # *** Renamed function and added check for freq=0 ***
    def tune(self, output_freq_mhz):
        """ Configures the LMX2595 for a specific *output* frequency.
            If output_freq_mhz is 0, the device is powered down.
        """
        print(f"\nTune Command Received for: {output_freq_mhz} MHz")

        # --- Handle Frequency = 0 Case ---
        if output_freq_mhz == 0:
             print("Frequency is 0, powering down PLL.")
             self.power_down()
             return # Exit function after powering down

        # --- Frequency Validation (Exclude 0 now) ---
        if not (self.min_freq_mhz <= output_freq_mhz <= self.max_freq_mhz):
            raise ValueError(f"Requested frequency {output_freq_mhz} MHz is outside device range ({self.min_freq_mhz}-{self.max_freq_mhz} MHz).")

        # --- Determine Required VCO Frequency, Doubler state, and Channel Divider ---
        target_vco_freq_mhz = 0
        chdiv_val = 0 # Corresponds to CHDIV register value
        chdiv_divider = 2 # Actual division ratio (default is 2 if CHDIV=0)
        use_doubler = False
        seg1_en = 0 # R31[14]

        vco_min = 7500
        vco_max = 15000
        doubler_max = 20000

        if vco_min <= output_freq_mhz <= vco_max:
            target_vco_freq_mhz = output_freq_mhz
            chdiv_val = 0 # Set to div=2 default
            chdiv_divider = 2
            seg1_en = 0 # Because CHDIV=0 (div=2)
            print(f"Targeting direct VCO frequency: {target_vco_freq_mhz} MHz")

        elif output_freq_mhz > vco_max:
            # Need VCO Doubler
            if output_freq_mhz > doubler_max:
                raise ValueError(f"Frequency {output_freq_mhz} MHz exceeds maximum with doubler ({doubler_max} MHz).")
            target_vco_freq_mhz = output_freq_mhz / 2.0
            if target_vco_freq_mhz < vco_min:
                 raise ValueError(f"Required VCO frequency {target_vco_freq_mhz} MHz for doubler is below VCO minimum ({vco_min} MHz).")
            use_doubler = True
            chdiv_val = 0 # No channel division needed
            chdiv_divider = 2
            seg1_en = 0
            print(f"Targeting VCO frequency: {target_vco_freq_mhz} MHz (for Doubler)")

        else: # output_freq_mhz < vco_min
            # Need Channel Divider
            div_map = { # CHDIV_reg_val: divider
                0: 2, 1: 4, 2: 6, 3: 8, 4: 12, 5: 16, 6: 24, 7: 32,
                8: 48, 9: 64, 10: 72, 11: 96, 12: 128, 13: 192, 14: 256,
                15: 384, 16: 512, 17: 768
            }
            found_divider = False
            for reg_val, divider in sorted(div_map.items()):
                 required_vco = output_freq_mhz * divider
                 if vco_min <= required_vco <= vco_max:
                      target_vco_freq_mhz = required_vco
                      chdiv_val = reg_val
                      chdiv_divider = divider
                      found_divider = True
                      break
            
            if not found_divider:
                 raise ValueError(f"Could not find suitable channel divider for {output_freq_mhz} MHz to place VCO in {vco_min}-{vco_max} MHz range.")
            
            seg1_en = 1 if chdiv_val > 0 else 0
            print(f"Targeting VCO frequency: {target_vco_freq_mhz} MHz (using Channel Divider={chdiv_divider}, CHDIV Reg={chdiv_val})")

        # --- Integer Mode Check ---
        current_pfd_freq = self.osc_freq * 2 if self.osc_doubler_enabled else self.osc_freq
        if abs(target_vco_freq_mhz % current_pfd_freq) > 1e-6: # Check for non-integer multiple (allow tolerance)
             raise ValueError(f"Required VCO frequency {target_vco_freq_mhz} MHz is not an integer multiple of PFD frequency {current_pfd_freq} MHz. Fractional mode not implemented.")
        
        # --- Update Registers ---
        print("Updating registers for new frequency...")
        
        # Set VCO2X_EN (R27[0])
        self.set_register_bits_with_mask("R27", 0x0001, 1 if use_doubler else 0)
        # Set Channel Divider (CHDIV) value (R75[10:6])
        self.set_register_bits_with_mask("R75", (0x1F << 6), chdiv_val << 6)
        # Set SEG1_EN (R31[14])
        self.set_register_bits_with_mask("R31", (1 << 14), seg1_en << 14)

        # Set Output Muxes
        outa_mux_val = 1 # Default direct VCO
        outb_mux_val = 1 # Default direct VCO
        if use_doubler:
             outa_mux_val = 2 # Doubler output on A
             outb_mux_val = 3 # Example: High-Z B
        elif chdiv_divider > 2: # Use actual divider value > 2 implies chdiv_val > 0
             outa_mux_val = 0 # Channel divider output
             outb_mux_val = 0 # Channel divider output
        # Set OUTA_MUX (R45[12:11])
        self.set_register_bits_with_mask("R45", (0x03 << 11), outa_mux_val << 11)
        # Set OUTB_MUX (R46[1:0])
        self.set_register_bits_with_mask("R46", 0x0003, outb_mux_val)

        # Calculate and set PLL_N and PFD_DLY_SEL for the target VCO frequency
        self.set_PLL_N(target_vco_freq_mhz)

        # Ensure OSC Freq and related settings are correct (important if changed externally)
        self.set_osc_freq_mhz(self.osc_freq) # Re-apply OSC settings just in case

        # --- Write All Registers and Calibrate ---
        self.reset_chip() # Software reset
        self._write_all_registers() # Program all registers with updated values
        
        print("Waiting 10ms before final calibration...")
        time.sleep(0.01)

        self.toggle_fcal() # Program R0 one last time with FCAL_EN=1

        print(f"Configuration complete for {output_freq_mhz} MHz output.")


    def power_down(self):
        """ Powers down device using POWERDOWN bit """
        print("Setting POWERDOWN bit...")
        self.set_register_bits_with_mask("R0", 0x0001, 1)
        self._write_register("R0")
    
    def power_up(self):
        """ Clears POWERDOWN bit """
        print("Clearing POWERDOWN bit...")
        self.set_register_bits_with_mask("R0", 0x0001, 0)
        self._write_register("R0")
        # It might be necessary to re-run calibration after power-up
        # self.toggle_fcal() # Consider if needed after power_up

    def toggle_fcal(self):
        """ Toggles FCAL_EN bit (R0[3]) to trigger VCO calibration """
        print("Toggling FCAL_EN to trigger VCO calibration...")
        fcal_mask = (1 << 3)
        # Read current R0 value from shadow register
        r0_val = self.registers["R0"]
        # Ensure FCAL_EN is low first (clear bit 3)
        self.set_register_bits_with_mask("R0", fcal_mask, 0)
        self._write_register("R0")
        time.sleep(0.001) # Optional short delay
        # Ensure FCAL_EN is high (set bit 3)
        self.set_register_bits_with_mask("R0", fcal_mask, fcal_mask)
        self._write_register("R0")