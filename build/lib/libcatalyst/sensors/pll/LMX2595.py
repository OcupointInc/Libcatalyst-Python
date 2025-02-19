# LMX2595.py
import math

registers = {
"R112":	0x700000,
"R111":	0x6F0000,
"R110":	0x6E0000,
"R109":	0x6D0000,
"R108":	0x6C0000,
"R107":	0x6B0000,
"R106":	0x6A0000,
"R105":	0x690021,
"R104":	0x680000,
"R103":	0x670000,
"R102":	0x663F80,
"R101":	0x650011,
"R100":	0x640000,
"R99":	0x630000,
"R98":	0x620200,
"R97":	0x610888,
"R96":	0x600000,
"R95":	0x5F0000,
"R94":	0x5E0000,
"R93":	0x5D0000,
"R92":	0x5C0000,
"R91":	0x5B0000,
"R90":	0x5A0000,
"R89":	0x590000,
"R88":	0x580000,
"R87":	0x570000,
"R86":	0x560000,
"R85":	0x55E700,
"R84":	0x540001,
"R83":	0x530000,
"R82":	0x523200,
"R81":	0x510000,
"R80":	0x506666,
"R79":	0x4F0026,
"R78":	0x4E0003,
"R77":	0x4D0000,
"R76":	0x4C000C,
"R75":	0x4B0800,
"R74":	0x4A0000,
"R73":	0x49003F,
"R72":	0x480001,
"R71":	0x470081,
"R70":	0x46C350,
"R69":	0x450000,
"R68":	0x4403E8,
"R67":	0x430000,
"R66":	0x4201F4,
"R65":	0x410000,
"R64":	0x401388,
"R63":	0x3F0000,
"R62":	0x3E0322,
"R61":	0x3D00A8,
"R60":	0x3C0000,
"R59":	0x3B0001,
"R58":	0x3A9001,
"R57":	0x390020,
"R56":	0x380000,
"R55":	0x370000,
"R54":	0x360000,
"R53":	0x350000,
"R52":	0x340820,
"R51":	0x330080,
"R50":	0x320000,
"R49":	0x314180,
"R48":	0x300300,
"R47":	0x2F0300,
"R46":	0x2E07FD,
"R45":	0x2DC8FF,
"R44":	0x2C3F60,
"R43":	0x2B0000,
"R42":	0x2A0000,
"R41":	0x290000,
"R40":	0x280000,
"R39":	0x2703E8,
"R38":	0x260000,
"R37":	0x250104,
"R36":	0x240032,
"R35":	0x230004,
"R34":	0x220000,
"R33":	0x211E21,
"R32":	0x200393,
"R31":	0x1F43EC,
"R30":	0x1E318C,
"R29":	0x1D318C,
"R28":	0x1C0488,
"R27":	0x1B0002,
"R26":	0x1A0DB0,
"R25":	0x190C2B,
"R24":	0x18071A,
"R23":	0x17007C,
"R22":	0x160001,
"R21":	0x150401,
"R20":	0x14E048,
"R19":	0x1327B7,
"R18":	0x120064,
"R17":	0x11012C,
"R16":	0x100080,
"R15":	0x0F064F,
"R14":	0x0E1E70,
"R13":	0x0D4000,
"R12":	0x0C5001,
"R11":	0x0B0018,
"R10":	0x0A10D8,
"R9":	0x091604,
"R8":	0x082000,
"R7":	0x0740B2,
"R6":	0x06C802,
"R5":	0x0500C8,
"R4":	0x040A43,
"R3":	0x030642,
"R2":	0x020500,
"R1":	0x010808,
"R0":	0x00251C,
}

class LMX2595():
    def __init__(self, driver, cs, clock_frequency_mhz = 100):
        self.driver = driver
        self.cs = cs
        self.max_freq_mhz = 16000
        self.freq_mhz = 14000
        self.registers = registers

        self.osc_doubler_enabled = True
        self.mash_order = 0 # Integer mode
        self.osc_freq = clock_frequency_mhz
        self.pfd_dly_sel = 1
        self.pll_n = 70

    def set_register_bits_with_mask(self, register, mask, values):
        # Ensure mask and values are within the valid range (24 bits)
        if mask < 0 or mask > (1 << 24) - 1:
            raise ValueError("Invalid mask value. It should be a 24-bit integer.")
        
        if values < 0 or values > (1 << 24) - 1:
            raise ValueError("Invalid values. It should be a 24-bit integer.")
        
        # Iterate over each bit position
        for bit_position in range(24):
            # Check if the bit in the mask is set
            if mask & (1 << bit_position):
                # Extract the corresponding bit from the values
                bit_value = (values >> bit_position) & 1
                
                # Clear the bit at the specified position
                bit_mask = ~(1 << bit_position)
                cleared_value = self.registers[register] & bit_mask
                
                # Set the bit at the specified position with the given value
                self.registers[register] = cleared_value | (bit_value << bit_position)

    def _set_osc_doubler(self):
        state = 1
        if self.osc_freq >= 200:
            state = 1
        self.osc_doubler_enabled = state
        self.set_register_bits_with_mask("R9", 0x1000, int(state) << 12)

    def unlock(self):
        self.set_register_bits_with_mask("R0", 0x02, 0x02)
        self._write_register("R0")

    def mute_port(self, port, value):        
        if port == "A":
            self.set_register_bits_with_mask("R44", 0x80, value << 6)

        if port == "B":
            self.set_register_bits_with_mask("R44", 0x100, value << 7)

    def set_osc_freq_mhz(self, freq_mhz):
        self.osc_freq = freq_mhz
        self._set_osc_doubler()
        self._set_ACAL_CMP_DLY()

    def _set_ACAL_CMP_DLY(self):
        val = math.floor(self.osc_freq / 10)
        self.set_register_bits_with_mask("R4", 0xFF00, val << 8)

    def _set_FCAL_HPFD_ADJ(self):
        val = 0
        freq = self.osc_freq
        if self.osc_doubler_enabled:
            freq = self.osc_freq *2
        if (freq) <= 100:
            val = 0
        if 100 < (freq) <= 150:
            val = 1
        if 150 <= (freq) <= 200:
            val = 2
        if (freq) > 200:
            val = 4
        self.set_register_bits_with_mask("R0", 0x180, val << 7)

    def set_pll_power(self, port, power):
        if power < 0 or power > 63:
            raise ValueError("Power level must be from 0 - 63")

        if port == "A":
            self.set_register_bits_with_mask("R44", 0x3F00, power << 8)
            self._write_register("R44")
        elif port == "B":
            self.set_register_bits_with_mask("R45", 0x1F, power)
            self._write_register("R45")

    def _write_register(self,register_id):
        self.driver.write_spi(self.cs, self.registers[register_id], 24)

    def reset_enable(self, state):
        self._reset_enable(state)
        self._write_register("R0")

    def _reset_enable(self, state):
        self.set_register_bits_with_mask("R0", 0x02, state << 1)

    def set_PLL_N(self, freq_mhz):
        reg_id = "R36"
        pll_n = math.floor(freq_mhz / int(self.osc_freq * 2))
        self.registers[reg_id] = 0x240000 + pll_n
        self.set_PFD_DLY_SEL(freq_mhz)

    def set_PFD_DLY_SEL(self, freq_mhz):
        reg_id = "R37"
        if self.mash_order == 0: # Integer mode
            if freq_mhz % 200 != 0:
                print("Error, frequency should be divisible by 200")
            elif freq_mhz <= 12500:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x01 << 8)
            else:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x02 << 8)
        elif self.mash_order == 1:
            if freq_mhz <= 10000:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x01 << 8)
            elif freq_mhz > 10000 and freq_mhz <= 12500:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x02 << 8)
            elif freq_mhz > 12500:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x03 << 8)
        elif self.mash_order == 2:
            if freq_mhz <= 10000:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x02 << 8)
            else:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x03 << 8)
        elif self.mash_order == 3:
            if freq_mhz <= 10000:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x03 << 8)
            else:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x04 << 8)
        elif self.mash_order == 4:
            if freq_mhz <= 10000:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x05 << 8)
            elif freq_mhz > 10000:
                self.set_register_bits_with_mask(reg_id, 0xFF << 8, 0x06 << 8)

    def read_register(self, register_address):
        print(f"Reading register {register_address}")
        
        # Ensure MUXout is configured for readback
        self.set_register_bits_with_mask("R0", 0x4, 0x0)
        self._write_register("R0")

        # Convert register address string to integer
        reg_addr = int(register_address[1:])

        # Prepare the read command
        read_command = (1 << 23) | (reg_addr << 16)
        print(f"Read command: 0x{read_command:06X}")

        # Step 2: Perform a second SPI transaction to read the data
        read_data = self.driver.exchange_spi(self.cs, read_command, 24)  # Send 24 zeroes to clock out the data
        print(f"Raw read data: 0x{read_data:06X}")

        # The first 8 bits are the register address, we're interested in the last 16 bits
        result = read_data & 0xFFFF
        print(f"Parsed result: 0x{result:04X}")

        return result



    def tune(self, freq_mhz):
        if freq_mhz > self.max_freq_mhz or freq_mhz < 0:
            raise ValueError(f"PLL Frequency must be between 0 and {self.max_freq} dB (inclusive).")
        
        if freq_mhz % self.osc_freq != 0:
            raise ValueError(f"Currently only supports integer mode. Output frequency must be a multiple of the clock frequency: {self.osc_freq}")

        if freq_mhz == 0:
            self.reset_enable(1)
            return

        self.reset_enable(0)



        self.set_PLL_N(freq_mhz)

        # Write the data
        for spi_word in self.registers.values():
           self.driver.write_spi(self.cs, spi_word, 24)

        self.toggle_fcal()

    def power_down(self):
        self.set_register_bits_with_mask("R0", 0x000001, 1)
        self._write_register("R0")
    
    def power_up(self):
        self.set_register_bits_with_mask("R0", 0x000001, 0)
        self._write_register("R0")

    def toggle_fcal(self):
        self.set_register_bits_with_mask("R0", 0x000000, 0x000000)
        self._write_register("R0")
        self.set_register_bits_with_mask("R0", 0x000008, 0x000008)
        self._write_register("R0")