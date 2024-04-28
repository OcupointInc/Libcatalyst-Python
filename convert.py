def convert_registers(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            # Clean up any whitespace or newlines
            clean_line = line.strip()
            # Extract the first two bytes and convert them to decimal
            if len(clean_line) >= 6:  # Ensure the line is at least as long as '0x0000'
                reg_number = int(clean_line[2:4], 16)  # Skip '0x' and take the next 4 characters (2 bytes)
            else:
                reg_number = 0  # Default to 0 if not enough characters

            # Write formatted output
            file.write(f'"R{reg_number}": {clean_line}\n')

# Specify the path to your input and output files
input_file_path = 'hex.txt'
output_file_path = 'hex_out.txt'

# Call the function with the file paths
convert_registers(input_file_path, output_file_path)