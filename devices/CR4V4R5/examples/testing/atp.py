import argparse
import csv
import json
import os
import sys
import time

from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5
from libcatalyst.devices.sig_gen import SignalGenerator
from libcatalyst.devices.spec_ann import SpectrumAnalyser
from plot_data import plot_data
from tune_from_json import tune_from_json

# Constants
TEST_BANDS_JSON_PATH = "./examples/testing/test_bands.json"
STEP_COUNT = 20

# --------------------------- Helper Functions --------------------------- #

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Run measurements for a specific channel and update the plot after each band.',
        epilog=(
            'Example:\n'
            '  python script.py --channel 1 --serial ABC123 --mode rx\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--channel', type=str, required=True,
                        help='Channel number (1-4) to test.')
    parser.add_argument('--serial', type=str, required=True,
                        help='Serial number of the device.')
    parser.add_argument('--mode', type=str, choices=['rx', 'tx'], default='rx',
                        help='Operation mode: "rx" for receive (default) or "tx" for transmit.')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force overwrite without confirmation.')
    return parser.parse_args()


def get_csv_filename(serial_number):
    """Return a CSV filename based on the serial number."""
    return f"data_{serial_number}.csv"


def remove_existing_data(csv_path, channel, force=False):
    """Remove rows from the CSV corresponding to the given channel."""
    if not force:
        prompt = (f"Warning: You are about to overwrite data for channel {channel} in '{csv_path}'. "
                  "Do you want to proceed? (y/n): ")
        while True:
            response = input(prompt).strip().lower()
            if response in ['y', 'yes']:
                break
            elif response in ['n', 'no']:
                print("Operation canceled by the user.")
                sys.exit(0)
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            preserved_rows = [row for row in reader if row[1] != channel]

        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(preserved_rows)

        print(f"Existing data for channel {channel} has been removed from '{csv_path}'.")


def write_csv_header_if_needed(csv_path, writer):
    """Write CSV header if the file is empty."""
    if os.path.getsize(csv_path) == 0:
        # Header: Band, Channel, Serial_Number, Frequency_MHz, Gain_dBm
        writer.writerow(["Band", "Channel", "Serial_Number", "Frequency_MHz", "Gain_dBm"])
        print(f"Header written to new CSV file: '{csv_path}'.")


# --------------------------- Main Execution --------------------------- #

def main():
    args = parse_args()
    mode = args.mode.lower()
    channel = args.channel
    serial_number = args.serial
    force_overwrite = args.force

    csv_filename = get_csv_filename(serial_number)

    # If the CSV file already exists, remove data for the current channel.
    if os.path.exists(csv_filename):
        remove_existing_data(csv_filename, channel, force=force_overwrite)

    print(f"Starting data collection for channel: {channel} on serial: {serial_number}")
    
    # Initialize hardware devices
    spec_ann = SpectrumAnalyser('GPIB0::20::INSTR')
    sig_gen = SignalGenerator('GPIB1::4::INSTR')
    spec_ann.sweep_continious = 0  # Disable continuous sweep

    # Initialize device driver and device
    driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=False)
    cr4 = CR4V4R5(driver)

    # Load band configurations from JSON file
    with open(TEST_BANDS_JSON_PATH, 'r') as file:
        bands = json.load(file)

    spec_ann.sweep_continious = 0
    spec_ann.trace_mode = "WRIT"

    # Open the CSV file in append mode.
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        write_csv_header_if_needed(csv_filename, csv_writer)

        # Process each band
        for band in bands["bands"]:
            band_name = band.get("name", f"Band_{band['rf_center_mhz']}")
            print(f"\nProcessing {band_name}...")

            tune_from_json(band, cr4)

            # Choose frequency keys based on mode
            if mode == "tx":
                if_center_key = "rf_center_mhz"
                rf_center_key = "if_center_mhz"
            else:
                if_center_key = "if_center_mhz"
                rf_center_key = "rf_center_mhz"

            spec_ann.center_freq_mhz = band[if_center_key]
            spec_ann.span_mhz = band["ibw_freq_mhz"] * 0.98  # Slightly larger than the bandwidth
    

            # Calculate frequency stepping
            step_size = int(band["ibw_freq_mhz"] / STEP_COUNT)
            sig_gen_start_freq = int(band[rf_center_key] - (band["ibw_freq_mhz"] / 2))
            rf_freq_start_mhz = int(band["rf_center_mhz"] - (band["ibw_freq_mhz"] / 2))

            # Set the input power for the signal generator
            sig_gen.power_dbm = band["input_level_dbm"]

            
            spec_ann.trigger_sweep()
            time.sleep(1)
            spec_ann.trigger_sweep()

            # Loop over each frequency step
            for i in range(STEP_COUNT + 1):
                current_freq = sig_gen_start_freq + i * step_size
                sig_gen.freq_mhz = current_freq

                try:
                    spec_ann.trigger_sweep()
                    prev_level = 0
                    level = -1
                    while level != prev_level:
                        prev_level = level
                        _, level = spec_ann.MARK1.get_peak()
                        if level > 8: # Only being used for isolation measurements
                            _, level = spec_ann.MARK1.get_next_peak()
                    gain_db = level - band["input_level_dbm"]
                except Exception as e:
                    print(f"Error during sweep: {e}")
                    break

                actual_rf_freq = rf_freq_start_mhz + i * step_size
                print(f"{band_name} - Channel: {channel}, Frequency: {current_freq} MHz, Gain: {gain_db} dBm")

                csv_writer.writerow([band_name, channel, serial_number, actual_rf_freq, gain_db])
                csv_file.flush()  # Ensure data is written immediately

            print(f"Completed processing {band_name}.")

            # Update plot for the current serial number after finishing this band.
            print("Updating plot for the current serial number...")
            plot_data(csv_filename, TEST_BANDS_JSON_PATH, serial_number)

    print(f"\nData saved to '{csv_filename}'.")

if __name__ == "__main__":
    main()
