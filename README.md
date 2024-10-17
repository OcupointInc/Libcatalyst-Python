# Libcatalyst-Python

## Description
Libcatalyst-Python is a Python library for interfacing with Ocupoint hardware devices using FTDI drivers.

## Installation and Setup

1. Clone the repository: git clone https://github.com/OcupointInc/Libcatalyst-Python.git
2. Move into the root directory: cd Libcatalyst-Python
3. Install the package: pip install -e .

## Usage

Examples are provided in each devices example folder. To run an example on the CR4, run the following commands.

1. cd devices/CR4V4R5
2. python ./cr4_gui.py

# Example Code
```python
# CR4 Example.py
from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V4R5 import CR4V4R5

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

# Define the downconvert PLL LO frequency
single_convert_freq_mhz = 10000

# Set the attenuators to 0 dB attenuation on all 4 channels
cr4.set_attenuation_db([1,2,3,4], 0)

# Tune the filter into bypass mode
cr4.tune_filters(0, 0, 0, 0)

# Tune the downconvert PLLs
cr4.tune_pll("D", single_convert_freq_mhz)
cr4.tune_pll("B", single_convert_freq_mhz)
```

## Configuration

The 'configs' directory contains JSON files that specify how the pins are connected through the FTDI chip. These configuration files are crucial for proper communication with the hardware.

## Windows-Specific Setup

If you encounter a driver error on Windows, with the FT232 chip, you may need to update the driver:

1. Download and install Zadig from https://zadig.akeo.ie/
2. Plug in your FTDI device, and go to Options -> List all Devices
3. Select the FTDI device and set the driver to WinUSB (Or libusb-win32 if WinUSB doesn't work)

After updating the driver, the library should work as expected on Windows systems.