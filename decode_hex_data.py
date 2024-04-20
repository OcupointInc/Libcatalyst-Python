from main import reconstruct_spi_input

def decode_from_file(path, num_bits):
    # Load the hex data from hext.txt
    data = []
    with open(path, "r") as file:
        for line in file:
            data.append(int(line, 16))

    reconstructed_GPA_CS_MASK, reconstructed_GPB_CS_MASK, reconstructed_word, reconstructed_num_bits = reconstruct_spi_input(data, num_bits)

    print("Reconstructed Output:")
    print(f"GPA_CS_MASK: 0x{reconstructed_GPA_CS_MASK:02X}")
    print(f"GPB_CS_MASK: 0x{reconstructed_GPB_CS_MASK:02X}")
    num_hex_chars = reconstructed_num_bits // 4
    print(f"Word: 0x{reconstructed_word:0{num_hex_chars}X}")
    print(f"Number of bits: {reconstructed_num_bits}")
    print()

path = "hext.txt"
num_bits = 24
decode_from_file(path, 24)