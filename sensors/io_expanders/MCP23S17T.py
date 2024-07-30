# IO_expander.py

class MCP23S17T:
    # Device opcode
    OPCODE = 0x40
    
    # Register addresses
    IODIRA = 0x00  # I/O direction register for bank A
    IODIRB = 0x01  # I/O direction register for bank B
    GPIOA = 0x12   # GPIO register for bank A
    GPIOB = 0x13   # GPIO register for bank B

    def __init__(self, driver, cs, device_address=0x00):
        self.driver = driver
        self.cs = cs
        self.device_address = device_address
        
    def _write_register(self, register, data):
        # Construct the control byte
        control_byte = self.OPCODE | (self.device_address << 1)
        
        # Construct the full message as an integer
        message = (control_byte << 16) | (register << 8) | data
        
        # Write the data using SPI
        self.driver.write_spi(self.cs, message, 24)
    
    def write_spi(self, bank, data, cs_mask, mosi_pin, sclk_pin, num_bits):
        # Set the bank direction to all outputs
        self.set_bank_direction(bank, 0x00)
        
        # Prepare the initial state (CS high, SCLK low, MOSI low, unused pins high)
        initial_state = 0xFF  # All pins high
        initial_state &= ~sclk_pin  # SCLK low
        initial_state &= ~mosi_pin  # MOSI low
        self.write_bank_state(bank, initial_state)
        
        # Pull CS low to start transmission
        current_state = initial_state & ~cs_mask
        self.write_bank_state(bank, current_state)
        
        # Bit-bang the data
        for i in range(num_bits):
            bit = (data >> (num_bits - 1 - i)) & 1
            
            # Set MOSI and clock high
            current_state = (current_state & ~mosi_pin) | (mosi_pin if bit else 0) | sclk_pin
            self.write_bank_state(bank, current_state)
            
            # Clock low
            current_state &= ~sclk_pin
            self.write_bank_state(bank, current_state)
        
        # Pull CS high to end transmission
        self.write_bank_state(bank, initial_state)



    def set_bank_direction(self, bank, direction):
        """
        Sets the I/O direction for the specified bank (A or B).
        
        :param bank: 'A' or 'B'
        :param direction: 8-bit value where:
                          1 = pin is configured as an input
                          0 = pin is configured as an output
        """
        if bank.upper() == 'A':
            register = self.IODIRA
        elif bank.upper() == 'B':
            register = self.IODIRB
        else:
            raise ValueError("Invalid bank. Use 'A' or 'B'.")
        
        self._write_register(register, direction)

    def write_bank_state(self, bank, state):
        if bank.upper() == 'A':
            register = self.GPIOA
        elif bank.upper() == 'B':
            register = self.GPIOB
        else:
            raise ValueError("Invalid bank. Use 'A' or 'B'.")
        
        self._write_register(register, state)