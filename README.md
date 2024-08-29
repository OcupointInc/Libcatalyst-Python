# Libcatalyst-Python

## Description
Libcatalyst-Python is a Python library for interfacing with Ocupoint hardware devices using FTDI drivers.

## Installation and Setup

1. Clone the repository: https://github.com/OcupointInc/Libcatalyst-Python.git
2. Install the required dependency 'pyftdi' using pip.

## Usage

Examples are provided in the main directory of the repository. Currently, you can find 'cr4_tune_sweep.py' which demonstrates basic usage of the library.

```python
# CR4 Example.py
from drivers.ftdi_driver import FTDISPIDriver
from devices.cr4_v4r5 import CR4V4R5

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
cr4 = CR4V4R5(driver)

# Define the downconvert PLL LO frequency
single_convert_freq_mhz = 10000

# Tune the downconvert PLLs
cr4.tune_pll("D", single_convert_freq_mhz)
cr4.tune_pll("B", single_convert_freq_mhz)
```

## Configuration

The 'configs' directory contains JSON files that specify how the pins are connected through the FTDI chip. These configuration files are crucial for proper communication with the hardware.

## Windows-specific Setup

If you encounter a driver error on Windows, particularly with the FT232 chip, you may need to update the driver:

1. Download and install Zadig from https://zadig.akeo.ie/
2. Plug in your FTDI device, and go to Options -> List all Devices
3. Select the FTDI device and set the driver to WinUSB

After updating the driver, the library should work as expected on Windows systems.