
import sys
import os
import time
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from drivers.ftdi_driver import FTDISPIDriver

# Initialize the FTDI SPI Driver
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=True)

# Read SPI words from the file
with open('./examples/cr4v4r4/spi_words.txt', 'r') as file:
    words = file.readlines()

# Remove any whitespace or newline characters
words = [word.strip() for word in words]


# Write each 24-bit SPI word
for word in words:
    # Assuming the word is a hexadecimal string and needs to be converted to an integer
    spi_word = int(word, 16)
    driver.write_spi("CS_PLL_B", spi_word, 24)