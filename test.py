from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioMpsseController
import time

# Initialize the FTDI device in MPSSE mode
ftdi = Ftdi()
ftdi.open_mpsse(vendor=0x0403, product=0x6014)

# Create a GPIO controller
gpio = GpioMpsseController()
gpio.configure('ftdi://ftdi:232h/1', direction=1, frequency=600000)

# First two bytes are the cbus, next two are for the dbus
ALL_PINS = 0xFFFF

# Set all pins as outputs
gpio.set_direction(ALL_PINS, ALL_PINS)

try:
    while True:
        # Set all pins high
        gpio.write(ALL_PINS)
        print("All pins set HIGH")
        time.sleep(1)

        # Set all pins low
        gpio.write(0x0000)
        print("All pins set LOW")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nScript terminated by user")
finally:
    # Clean up
    gpio.write(0x0000)  # Set all pins low
    gpio.close()
    ftdi.close()