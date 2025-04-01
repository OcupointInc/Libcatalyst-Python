class MCP23S17T:
    # Device opcode
    OPCODE = 0x40

    # Register addresses
    IODIRA = 0x00  # I/O direction register for bank A
    IODIRB = 0x01  # I/O direction register for bank B
    GPIOA = 0x12  # GPIO register for bank A
    GPIOB = 0x13  # GPIO register for bank B

    def __init__(self, driver, cs, device_address=0x00, mosi_pin=0x08, sclk_pin=0x04, cs_mask=0x30, spi_bank='B'):
        self.driver = driver
        self.cs = cs
        self.device_address = device_address
        self.mosi_pin = mosi_pin
        self.sclk_pin = sclk_pin
        self.cs_mask = cs_mask
        self.spi_bank = spi_bank
        self.bank_a_state = 0x00  # Initialize bank A state
        self.bank_b_state = 0x00  # Initialize bank B state
        self.bank_a_direction = 0xFF  # Initialize bank A direction (all inputs)
        self.bank_b_direction = 0xFF  # Initialize bank B direction (all inputs)

    def _write_register(self, register, data):
        # Construct the control byte
        control_byte = self.OPCODE | (self.device_address << 1)

        # Construct the full message as an integer
        message = (control_byte << 16) | (register << 8) | data

        # Write the data using SPI
        self.driver.write_spi(self.cs, message, 24)

    def set_bank_direction(self, bank, direction):
        if bank.upper() == 'A':
            register = self.IODIRA
            self.bank_a_direction = direction
        elif bank.upper() == 'B':
            register = self.IODIRB
            self.bank_b_direction = direction
        else:
            raise ValueError("Invalid bank. Use 'A' or 'B'.")

        self._write_register(register, direction)

    def write_bank_state(self, bank, state):
        if bank.upper() == 'A':
            register = self.GPIOA
            self.bank_a_state = state
        elif bank.upper() == 'B':
            register = self.GPIOB
            self.bank_b_state = state
        else:
            raise ValueError("Invalid bank. Use 'A' or 'B'.")

        self._write_register(register, state)

    def set_bit(self, bank, bit_index, value):
        """
        Sets the state of a single bit in the specified bank.

        Args:
            bank (str):  'A' or 'B' to specify the bank.
            bit_index (int): The index of the bit to set (0-7).
            value (int): 0 or 1, the desired state of the bit.
        """
        if not 0 <= bit_index <= 7:
            raise ValueError("Bit index must be between 0 and 7.")
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1.")

        if bank.upper() == 'A':
            current_state = self.bank_a_state
        elif bank.upper() == 'B':
            current_state = self.bank_b_state
        else:
            raise ValueError("Invalid bank. Use 'A' or 'B'.")

        if value == 1:
            current_state |= (1 << bit_index)  # Set the bit
        else:
            current_state &= ~(1 << bit_index) # Clear the bit

        self.write_bank_state(bank, current_state)

    def write_spi(self, cs, data, num_bits):
        bank_state = self.bank_b_state if self.spi_bank.upper() == 'B' else self.bank_a_state

        initial_state = bank_state | self.cs_mask  # CS high
        initial_state &= ~self.sclk_pin  # SCLK low
        initial_state &= ~self.mosi_pin  # MOSI low
        self.write_bank_state(self.spi_bank, initial_state)

        # Pull CS low to start transmission
        current_state = initial_state & ~self.cs_mask
        self.write_bank_state(self.spi_bank, current_state)

        # Bit-bang the data
        for i in range(num_bits):
            bit = (data >> (num_bits - 1 - i)) & 1

            # Set MOSI for the current bit while clock is low
            if bit:
                current_state |= self.mosi_pin
            else:
                current_state &= ~self.mosi_pin
            self.write_bank_state(self.spi_bank, current_state)

            # Set clock high
            current_state |= self.sclk_pin
            self.write_bank_state(self.spi_bank, current_state)

            # Set clock low
            current_state &= ~self.sclk_pin
            self.write_bank_state(self.spi_bank, current_state)

        # Pull CS high to end transmission
        current_state |= self.cs_mask
        self.write_bank_state(self.spi_bank, current_state)

        # Reset MOSI and SCLK to low after transmission
        current_state &= ~self.mosi_pin
        current_state &= ~self.sclk_pin
        self.write_bank_state(self.spi_bank, current_state)