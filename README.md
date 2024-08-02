# Libcatalyst-Python

## Description
Libcatalyst-Python is a Python library for interfacing with Ocupoint hardware devices using FTDI drivers.

## Installation and Setup

1. Clone the repository from GitHub.
2. Install the required dependency 'pyftdi' using pip.

## Usage

Examples are provided in the main directory of the repository. Currently, you can find 'qc_example.py' which demonstrates basic usage of the library.

```python
# QC Example.py
from devices.queens_canyon import QueensCanyon, QCBank
from drivers.ftdi_driver import FTDISPIDriver
import time
from devices.queens_canyon import QueensCanyon

driver = FTDISPIDriver("configs/QC_FTDI.json", debug=True) #Prints out the words being written
qc = QueensCanyon(driver)

for i in range(31):
    qc.set_attenuation_db(i)
    time.sleep(1)
```

## Configuration

The 'configs' directory contains JSON files that specify how the pins are connected through the FTDI chip. These configuration files are crucial for proper communication with the hardware.

## Windows-specific Setup

If you encounter a driver error on Windows, particularly with the FT232 chip, you may need to update the driver:

1. Download and install Zadig from https://zadig.akeo.ie/
2. Plug in your FTDI device, and go to Options -> List all Devices
3. Select the FTDI device and set the driver to WinUSB

After updating the driver, the library should work as expected on Windows systems.