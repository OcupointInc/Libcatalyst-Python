

def generate_soft_spi_word_sequence(GPA_CS_MASK, GPB_CS_MASK, word, num_bits):
    data = []

    # Set CS for the attenuators high
    #data.append(0x4012FF)

    # Set CS for the filter high, MISO low
    #data.append(0x40133C)

    binary_word = bin(word)[2:]

    # Writes the words if CS for the attenuators were set low
    if (GPA_CS_MASK & 0x0F) != 0x0F:
        # Set the sclk and data lines low
        #row_data = GPB_CS_MASK & ~0x30
        #data.insert(0, 0x4012)
        #data.append(row_data)

        # Write the data bits
        for bit in binary_word[:num_bits]:
            row_data = 0x4012FF & ~0x000030  # Set the sclk and data lines low
            # set the chip select mask with GPA_CS_MASK on the last two bits
            mask = 0xFFFF00 | GPA_CS_MASK
            row_data = row_data & mask

            # Set the data bit
            if bit == '1':
                row_data |= 0x20

            # Send the data with the sclk low
            data.append(row_data)

            # Set the data with the sclk high
            row_data = row_data | 0x000010
            data.append(row_data)

    # Reset the CS for the attenuators high
    #data.append(0x4012FF)


    return data

def parse_24bit_value(value):
    # Extract the register and bank values
    register = (value >> 16) & 0xFF
    bank = (value >> 8) & 0xFF

    # Extract the pin values for the specified bank
    if bank == 0x12:  # Bank GPA
        pin_states = {
            0: {"name": "CS_ATTEN_CH4", "value": value & 0x01},
            1: {"name": "CS_ATTEN_CH3", "value": (value >> 1) & 0x01},
            2: {"name": "CS_ATTEN_CH2", "value": (value >> 2) & 0x01},
            3: {"name": "CS_ATTEN_CH1", "value": (value >> 3) & 0x01},
            4: {"name": "SCLK_ATTEN", "value": (value >> 4) & 0x01},
            5: {"name": "MOSI_ATTEN", "value": (value >> 5) & 0x01},
            6: {"name": "SFL_CH1_CH2", "value": (value >> 6) & 0x01},
            7: {"name": "SFL_CH3_CH4", "value": (value >> 7) & 0x01}
        }
    elif bank == 0x13:  # Bank GPB
        pin_states = {
            0: {"name": "MISO_FILTER_CH1", "value": value & 0x01},
            1: {"name": "MISO_FILTER_CH2", "value": (value >> 1) & 0x01},
            2: {"name": "SCLK_FILTER", "value": (value >> 2) & 0x01},
            3: {"name": "MOSI_FILTER", "value": (value >> 3) & 0x01},
            4: {"name": "CS_FILTER_CH1_CH2", "value": (value >> 4) & 0x01},
            5: {"name": "CS_FILTER_CH3_CH4", "value": (value >> 5) & 0x01},
            6: {"name": "MISO_FILTER_CH3", "value": (value >> 6) & 0x01},
            7: {"name": "MISO_FILTER_CH4", "value": (value >> 7) & 0x01}
        }
    else:
        raise ValueError(f"Invalid bank value: {bank}")

    # Print the register, bank values, and pin states on the same line
    print(f"0x{value:06X} Register: 0x{register:02X} Bank: {'GPA' if bank == 0x12 else 'GPB'}", end=" ")
    for bit, pin in pin_states.items():
        print(f"{pin['name']}: {'HIGH' if pin['value'] else 'LOW'}", end=" ")
    print()

def reconstruct_spi_input(data_24_bit, num_bits):
    GPA_CS_MASK = 0xFF
    GPB_CS_MASK = 0xFF
    channels_tuned = []
    word = 0
    bit_count = 0
    for value in data_24_bit:
        # Reverse the 8 LSBs of the 24-bit value
        #value = ((value & 0xFF00) >> 8)
        bank = (value >> 8) & 0xFF
        if bank == 0x12:  # Bank GPA
            if (value & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 0)  # CS_ATTEN_CH4
                channels_tuned.append("Attenuator CH4")
            if ((value >> 1) & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 1)  # CS_ATTEN_CH3
                channels_tuned.append("Attenuator CH3")
            if ((value >> 2) & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 2)  # CS_ATTEN_CH2
                channels_tuned.append("Attenuator CH2")
            if ((value >> 3) & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 3)  # CS_ATTEN_CH1
                channels_tuned.append("Attenuator CH1")
            if GPA_CS_MASK != 0xFF:  # Check if any CS in GPA is set low
                if ((value >> 4) & 0x01) == 1:  # SCLK_ATTEN
                    if ((value >> 5) & 0x01) == 1:  # MOSI_ATTEN
                        word = (word << 1) | 1
                        print(1, f"0x{value:02X}")
                    else:
                        word = (word << 1) | 0
                        # print the value as hex
                        print(0, f"0x{value:02X}")
                    bit_count += 1
        elif bank == 0x13:  # Bank GPB
            if ((value >> 4) & 0x01) == 0:
                GPB_CS_MASK &= ~(1 << 4)  # CS_FILTER_CH1_CH2
            if ((value >> 5) & 0x01) == 0:
                GPB_CS_MASK &= ~(1 << 5)  # CS_FILTER_CH3_CH4
            if GPB_CS_MASK != 0xFF:  # Check if any CS in GPB is set low
                if ((value >> 2) & 0x01) == 1:  # SCLK_FILTER
                    if ((value >> 3) & 0x01) == 1:  # MOSI_FILTER
                        word = (word << 1) | 1
                        print(1, f"0x{value:02X}")
                    else:
                        word = (word << 1) | 0
                        print(0,f"0x{value:02X}")
                    bit_count += 1

    return GPA_CS_MASK, GPB_CS_MASK, word, bit_count