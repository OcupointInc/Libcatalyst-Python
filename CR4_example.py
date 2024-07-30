# QC Example.py
import time
from drivers.ftdi_driver import FTDISPIDriver

# Initialize the FTDI SPI Driver
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)

# Read SPI words from the file
with open('./PRF_Bypass.txt', 'r') as file:
    words = file.readlines()

# Remove any whitespace or newline characters
words = [word.strip() for word in words]

# Write each 24-bit SPI word
for word in words:
    # Assuming the word is a hexadecimal string and needs to be converted to an integer
    spi_word = int(word, 16)
    driver.write_spi("CS_PRF_IO", spi_word, 24)
    # Adding a small delay to ensure proper timing (adjust as needed)
    time.sleep(0.0001)
