import RPi.GPIO as GPIO
import time

# Define GPIO pins using BCM numbering
MOSI = 10
SCLK = 11
CS = 8

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

# Initialize CS high and SCLK low
GPIO.output(CS, GPIO.HIGH)
GPIO.output(SCLK, GPIO.LOW)

def spi_write_bits(data, num_bits):
    """
    Write a specified number of bits to SPI.
    """
    GPIO.output(CS, GPIO.LOW)  # Activate the CS line to start the transaction
    for i in range(num_bits):  # Loop over each bit
        # Calculate the position of the bit to send
        bit_pos = num_bits - 1 - i
        # Set MOSI according to the bit at bit_pos
        GPIO.output(MOSI, (data >> bit_pos) & 0x1)
        # Toggle SCLK to high and then low
        GPIO.output(SCLK, GPIO.HIGH)
        time.sleep(0.00000001)  # Short delay for SPI timing
        GPIO.output(SCLK, GPIO.LOW)
    GPIO.output(CS, GPIO.HIGH)  # Deactivate CS to end the transaction

def send_data(data, num_bits):
    """
    Send data to SPI, specifying the number of bits for each data item.
    """
    for item in data:
        spi_write_bits(item, num_bits)

# Data to send and the number of bits for each item
data_to_send = [0x11012c, 0x11012c, 0x11012c]  # Example data
bits_per_item = 24  # Example: sending 8 bits for each item
# Send data
send_data(data_to_send, bits_per_item)

# Cleanup GPIO
GPIO.cleanup()
