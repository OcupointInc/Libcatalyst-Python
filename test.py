from main import generate_soft_spi_word_sequence, reconstruct_spi_input

def test_spi_communication(GPA_CS_MASK, GPB_CS_MASK, word, num_input_bits, num_output_bits):
    print("Original Input:")
    print(f"GPA_CS_MASK: 0x{GPA_CS_MASK:02X}")
    print(f"GPB_CS_MASK: 0x{GPB_CS_MASK:02X}")
    num_hex_chars = num_input_bits // 4
    print(f"Word: 0x{word:0{num_hex_chars}X}")
    print(f"Number of bits: {num_input_bits}")
    print()

    data = generate_soft_spi_word_sequence(GPA_CS_MASK, GPB_CS_MASK, word, num_input_bits)

    reconstructed_GPA_CS_MASK, reconstructed_GPB_CS_MASK, reconstructed_word, reconstructed_num_bits = reconstruct_spi_input(data)

    print("Reconstructed Output:")
    print(f"GPA_CS_MASK: 0x{reconstructed_GPA_CS_MASK:02X}")
    print(f"GPB_CS_MASK: 0x{reconstructed_GPB_CS_MASK:02X}")
    num_hex_chars = num_output_bits // 4
    print(f"Word: 0x{reconstructed_word:0{num_hex_chars}X}")
    print(f"Number of bits: {reconstructed_num_bits}")
    print()

    if (GPA_CS_MASK == reconstructed_GPA_CS_MASK and
        GPB_CS_MASK == reconstructed_GPB_CS_MASK and
        word == reconstructed_word):
        print("Input and reconstructed output match!")
    else:
        print("Input and reconstructed output do not match.")

# Example usage
GPA_CS_MASK = 0xF0
GPB_CS_MASK = 0xFF
word = 0x008071
num_bits = 24

test_spi_communication(GPA_CS_MASK, GPB_CS_MASK, word, num_bits, num_bits)