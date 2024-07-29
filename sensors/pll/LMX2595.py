# rf_digital_attenuator.py
import math

registers={
    "R112": 0x700000,
    "R111": 0x6F0000,
    "R110": 0x6E0000,
    "R109": 0x6D0000,
    "R108": 0x6C0000,
    "R107": 0x6B0000,
    "R78": 0x4E0003,
    "R77": 0x4D0000,
    "R76": 0x4C000C,
    "R75": 0x4B0800,
    "R74": 0x4A0000,
    "R73": 0x49003F,
    "R72": 0x480001,
    "R71": 0x470081,
    "R70": 0x46C350,
    "R69": 0x450000,
    "R68": 0x4403E8,
    "R67": 0x430000,
    "R66": 0x4201F4,
    "R65": 0x410000,
    "R64": 0x401388,
    "R63": 0x3F0000,
    "R62": 0x3E0322,
    "R61": 0x3D00A8,
    "R60": 0x3C0000,
    "R59": 0x3B0001,
    "R58": 0x3A9001,
    "R57": 0x390020,
    "R56": 0x380000,
    "R55": 0x370000,
    "R54": 0x360000,
    "R53": 0x350000,
    "R52": 0x340820,
    "R51": 0x330080,
    "R50": 0x320000,
    "R49": 0x314180,
    "R48": 0x300300,
    "R47": 0x2F0300,
    "R46": 0x2E07FD,
    "R45": 0x2DC8DF,
    "R44": 0x2C1F20,
    "R43": 0x2B0000,
    "R42": 0x2A0000,
    "R41": 0x290000,
    "R40": 0x280000,
    "R39": 0x2703E8,
    "R38": 0x260000,
    "R37": 0x250204,
    "R36": 0x240046,
    "R35": 0x230004,
    "R34": 0x220000,
    "R33": 0x211E21,
    "R32": 0x200393,
    "R31": 0x1F43EC,
    "R30": 0x1E318C,
    "R29": 0x1D318C,
    "R28": 0x1C0488,
    "R27": 0x1B0002,
    "R26": 0x1A0DB0,
    "R25": 0x190C2B,
    "R24": 0x18071A,
    "R23": 0x17007C,
    "R22": 0x160001,
    "R21": 0x150401,
    "R20": 0x14E048,
    "R19": 0x1327B7,
    "R18": 0x120064,
    "R17": 0x11012C,
    "R16": 0x100080,
    "R15": 0x0F064F,
    "R14": 0x0E1E70,
    "R13": 0x0D4000,
    "R12": 0x0C5001,
    "R11": 0x0B0018,
    "R10": 0x0A10D8,
    "R9": 0x091604,
    "R8": 0x082000,
    "R7": 0x0740B2,
    "R6": 0x06C802,
    "R5": 0x0500C8,
    "R4": 0x040A43,
    "R3": 0x030642,
    "R2": 0x020500,
    "R1": 0x010808,
    "R0": 0x002518
}



class LMX2595():
    def __init__(self, driver, cs):
        self.driver = driver
        self.cs = cs
        self.max_freq_mhz = 16000
        self.freq_mhz = 14000
        self.registers = registers

        self.mash_order = 0 # Integer mode
        self.pfd_dly_sel = 1
        self.pll_n = 70

    def set_register_byte(self, register, bit_position, value):
        if bit_position < 0 or bit_position > 23:
            raise ValueError("Invalid bit position. It should be between 0 and 23.")
        
        if value < 0 or value > 15:
            raise ValueError("Invalid bit value. It should be between 0 and 15.")
        
        # Clear the bits at the specified position
        mask = ~(0xF << bit_position)
        cleared_value = self.registers[register] & mask
        
        # Set the bits at the specified position with the given value
        self.registers[register] = cleared_value | (value << bit_position)
        self.driver.write_spi(self.cs, self.registers[register], 24)

    def set_PLL_N(self, freq_mhz):
        reg_id = "R36"
        pll_n = math.floor(freq_mhz / 200)
        self.registers[reg_id] = 0x240000 + pll_n
        self.set_PFD_DLY_SEL(freq_mhz)


    def set_PFD_DLY_SEL(self, freq_mhz):
        reg_id = "R37"
        bit_position = 8
        if self.mash_order == 0: # Integer mode
            if freq_mhz % 200 != 0:
                print("Error, frequency should be divisible by 200")
            elif freq_mhz <= 12500:
                self.set_register_byte(reg_id, bit_position, 0x01)
            else:
                self.set_register_byte(reg_id, bit_position, 0x02)
        elif self.mash_order == 1:
            if freq_mhz <= 10000:
                self.set_register_byte(reg_id, bit_position, 0x01)
            elif freq_mhz > 10000 and freq_mhz <= 12500:
                self.set_register_byte(reg_id, bit_position, 0x02)
            elif freq_mhz > 12500:
                self.set_register_byte(reg_id, bit_position, 0x03)
        elif self.mash_order == 2:
            if freq_mhz <= 10000:
                self.set_register_byte(reg_id, bit_position, 0x02)
            else:
                self.set_register_byte(reg_id, bit_position, 0x03)
        elif self.mash_order == 3:
            if freq_mhz <= 10000:
                self.set_register_byte(reg_id, bit_position, 0x03)
            else:
                self.set_register_byte(reg_id, bit_position, 0x04)
        elif self.mash_order == 4:
            if freq_mhz <= 10000:
                self.set_register_byte(reg_id, bit_position, 0x05)
            elif freq_mhz > 10000:
                self.set_register_byte(reg_id, bit_position, 0x06)


    def tune(self, freq_mhz):
        if freq_mhz > self.max_freq_mhz or freq_mhz < 0:
            raise ValueError(f"PLL Frequency must be between 0 and {self.max_freq} dB (inclusive).")

        self.set_PLL_N(freq_mhz)

        # Write the data
        for spi_word in self.registers.values():
           self.driver.write_spi(self.cs, spi_word, 24) 
        
        
        # self.driver.write_spi(self.cs, spi_word, self.num_bits)
        #pass

