def generate_soft_spi_word_sequence(GPA_CS_MASK, GPB_CS_MASK, word, num_bits):
    NUM_BYTES_PER_WORD = 3
    NUM_BYTES = 2 * num_bits * NUM_BYTES_PER_WORD + 5 * NUM_BYTES_PER_WORD
    
    word_rev = bit_reverse(word, 0xFFFFFF) if num_bits >= 8 else bit_reverse(word, 0xFF)
    word_rev = word_rev << 1
    
    data = [0] * NUM_BYTES
    
    # Reset at start
    data[0:6] = [0x40, 0x12, 0xFF & 0xEF & 0xDF & 0x3F, 0x40, 0x13, 0x3C & 0xF7 & 0xFB]
    
    for ii in range(6, num_bits * 3 * 2 + 6, 3):
        data[ii] = 0x40
        
        if GPA_CS_MASK != 0xFF:
            data[ii + 1] = 0x12
            data[ii + 2] = 0xFF & GPA_CS_MASK
            
            if (word_rev & 0x1) == 0:
                data[ii + 2] &= 0xDF
            
            if (ii % 2) == 0:
                data[ii + 2] &= 0xEF
                word_rev = word_rev >> 1
        
        elif GPB_CS_MASK != 0xFF:
            data[ii + 1] = 0x13
            data[ii + 2] = 0x3C & GPB_CS_MASK
            
            if ii % 2 == 0:
                data[ii + 2] &= 0xFB
                word_rev = word_rev >> 1
            
            if (word_rev & 0x1) == 0:
                data[ii + 2] &= 0xF7
    
    # Reset at end
    if GPA_CS_MASK != 0xFF:
        data[NUM_BYTES - 9:NUM_BYTES - 6] = [0x40, 0x12, data[NUM_BYTES - 10] & 0xEF & 0x3F]
    elif GPB_CS_MASK != 0xFF:
        data[NUM_BYTES - 9:NUM_BYTES - 6] = [0x40, 0x13, data[NUM_BYTES - 10] & 0xF7]
    
    data[NUM_BYTES - 6:] = [0x40, 0x12, 0xFF & 0xEF & 0xDF & 0x3F, 0x40, 0x13, 0x3C & 0xF7 & 0xFB]
    
    return data

def bit_reverse(data, mask):
    total_bits = 32
    shift_msb = 0
    reversed_data = 0
    
    for ii in range(total_bits):
        if mask & (1 << (total_bits - 1 - ii)):
            temp = (data & (1 << (total_bits - 1 - ii)))
            
            if temp:
                reversed_data |= (1 << (shift_msb))
            else:
                reversed_data |= (0 << (shift_msb))
            
            shift_msb += 1
    
    return reversed_data

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

def reconstruct_spi_input(hex_values, num_bits):
    data = [int(hex_value, 16) for hex_value in hex_values]

    GPA_CS_MASK = 0xFF
    GPB_CS_MASK = 0xFF

    word = 0
    bit_count = 0

    for i in range(len(data)):
        value = data[i]
        bank = (value >> 8) & 0xFF

        if bank == 0x12:  # Bank GPA
            if (value & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 0)  # CS_ATTEN_CH4
            if ((value >> 1) & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 1)  # CS_ATTEN_CH3
            if ((value >> 2) & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 2)  # CS_ATTEN_CH2
            if ((value >> 3) & 0x01) == 0:
                GPA_CS_MASK &= ~(1 << 3)  # CS_ATTEN_CH1

            if GPA_CS_MASK != 0xFF:  # Check if any CS in GPA is set low
                if ((value >> 5) & 0x01) == 1:  # MOSI_ATTEN
                    word = (word << 1) | ((value >> 5) & 0x01)
                    bit_count += 1

        elif bank == 0x13:  # Bank GPB
            if ((value >> 4) & 0x01) == 0:
                GPB_CS_MASK &= ~(1 << 4)  # CS_FILTER_CH1_CH2
            if ((value >> 5) & 0x01) == 0:
                GPB_CS_MASK &= ~(1 << 5)  # CS_FILTER_CH3_CH4

            if GPB_CS_MASK != 0xFF:  # Check if any CS in GPB is set low
                if ((value >> 3) & 0x01) == 1:  # MOSI_FILTER
                    word = (word << 1) | ((value >> 3) & 0x01)
                    bit_count += 1

        if bit_count == num_bits:
            break

    # Adjust the word based on the number of bits
    if num_bits == 24:
        word = word >> (24 - bit_count)  # Right-shift the word to align with the actual data
    else:
        word = word >> (8 - bit_count)  # Right-shift the word to align with the actual data

    return GPA_CS_MASK, GPB_CS_MASK, word, num_bits