from pyftdi.ftdi import Ftdi

# Open the device
ftdi = Ftdi()
ftdi.open_from_url('ftdi://ftdi:ft232h/1')

# Read the current EEPROM configuration
eeprom = bytearray(ftdi.read_eeprom())

# Set CBUS pins to GPIO mode
eeprom[0x1A] = 0x08  # CBUS0 to GPIO
eeprom[0x1B] = 0x08  # CBUS1 to GPIO
eeprom[0x1C] = 0x08  # CBUS2 to GPIO
eeprom[0x1D] = 0x08  # CBUS3 to GPIO

# Write the modified EEPROM configuration
ftdi.write_eeprom(0, eeprom)  # Start writing from address 0

# Close the device
ftdi.close()

print("EEPROM updated successfully. Please unplug and replug your FT232H for the changes to take effect.")