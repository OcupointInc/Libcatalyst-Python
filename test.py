from main import generate_soft_spi_word_sequence, reconstruct_spi_input

def test_spi_communication(GPA_CS_MASK, GPB_CS_MASK, word, num_input_bits, num_output_bits):
    print("Original Input:")
    print(f"GPA_CS_MASK: 0x{GPA_CS_MASK:02X}")
    print(f"GPB_CS_MASK: 0x{GPB_CS_MASK:02X}")
    print(f"Word: 0x{word:02X}")
    print(f"Number of bits: {num_input_bits}")
    print()

    data = generate_soft_spi_word_sequence(GPA_CS_MASK, GPB_CS_MASK, word, num_input_bits)
    hex_values = [f"0x{((data[i] << 16) | (data[i+1] << 8) | data[i+2]):06X}" for i in range(0, len(data), 3)]

    print("Generated SPI Words:")
    for hex_value in hex_values:
        print(hex_value)
    print()

    reconstructed_GPA_CS_MASK, reconstructed_GPB_CS_MASK, reconstructed_word, reconstructed_num_bits = reconstruct_spi_input(hex_values, num_output_bits)

    print("Reconstructed Output:")
    print(f"GPA_CS_MASK: 0x{reconstructed_GPA_CS_MASK:02X}")
    print(f"GPB_CS_MASK: 0x{reconstructed_GPB_CS_MASK:02X}")
    print(f"Word: 0x{reconstructed_word:02X}")
    print(f"Number of bits: {reconstructed_num_bits}")
    print()

    if (GPA_CS_MASK == reconstructed_GPA_CS_MASK and
        GPB_CS_MASK == reconstructed_GPB_CS_MASK and
        word == reconstructed_word):
        print("Input and reconstructed output match!")
    else:
        print("Input and reconstructed output do not match.")

# Example usage
GPA_CS_MASK = 0xFE
GPB_CS_MASK = 0xFF
word = 0x1A
num_input_bits = 6
num_output_bits = 8

test_spi_communication(GPA_CS_MASK, GPB_CS_MASK, word, num_input_bits, num_output_bits)