import json
import matplotlib.pyplot as plt
import os
import csv
import random

def plot_data(csv_path, test_bands_json, serial_number):
    """
    Reads the CSV file and plots data for the specified serial number.
    Data is grouped by channel and band, and each band's data is plotted 
    as an individual line segment so that lines for different bands are not connected.
    Each channel is plotted with a fixed color. Channels are represented as strings.
    If a channel is not in the fixed channel list, a random color is assigned.
    """
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found. No plot was generated.")
        return

    # Load band configurations so that bands can be sorted by RF center.
    with open(test_bands_json, 'r') as file:
        bands_config = json.load(file)

    band_rf_map = {}
    for band in bands_config["bands"]:
        # Use the band name if provided, otherwise generate one.
        band_name = band.get("name", f"Band_{band['rf_center_mhz']}")
        band_rf_map[band_name] = band["rf_center_mhz"]

    # Data structure: data[channel][band] = {'frequencies': [], 'gains': []}
    data = {}
    with open(csv_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Serial_Number"] != serial_number:
                continue  # Skip rows not matching the serial number.
            
            # Treat channel as a string.
            channel = row["Channel"]
            band_name = row["Band"]
            frequency = float(row["Frequency_MHz"])
            gain = float(row["Gain_dBm"])

            if channel not in data:
                data[channel] = {}
            if band_name not in data[channel]:
                data[channel][band_name] = {'frequencies': [], 'gains': []}
            data[channel][band_name]['frequencies'].append(frequency)
            data[channel][band_name]['gains'].append(gain)

    if not data:
        print(f"No data found for serial number: {serial_number}")
        return

    # Define a fixed color for some channels (using strings as keys).
    channel_colors = {
        "1": 'blue',
        "2": 'orange',
        "3": 'green',
        "4": 'red',
        "1_to_3_iso": 'blue',
        '2_to_4_iso': 'red'
    }

    # For any channel not specified in channel_colors, assign a random color.
    for channel in data.keys():
        if channel not in channel_colors:
            # Generate a random hex color.
            random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            channel_colors[channel] = random_color

    plt.figure(figsize=(12, 8))

    # Plot the data for each channel.
    for channel in sorted(data.keys()):
        channel_color = channel_colors.get(channel, 'black')  # Should always have a color now.
        first_segment_for_channel = True
        # Sort the bands by their RF center frequency (if available).
        sorted_band_names = sorted(data[channel].keys(), key=lambda bn: band_rf_map.get(bn, bn))
        for band_name in sorted_band_names:
            freqs = data[channel][band_name]['frequencies']
            gains = data[channel][band_name]['gains']
            label = f"{channel}" if first_segment_for_channel else None
            first_segment_for_channel = False

            # Plot the line segment for this band.
            plt.plot(freqs, gains, linestyle='-', color=channel_color, label=label)

    plt.title(f"Gain vs Frequency: {serial_number}")
    plt.xlabel("RF Frequency (MHz)")
    plt.ylabel("Gain (dB)")
    plt.grid(True)
    plt.legend()

    # Set Y-axis limits to 0 dB and 35 dB.
    plt.ylim(0, 35)

    # Ensure the plots directory exists.
    plots_dir = "./plots"
    os.makedirs(plots_dir, exist_ok=True)
    plot_filename = os.path.join(plots_dir, f"gain_vs_frequency_{serial_number}.png")
    plt.savefig(plot_filename)
    print(f"Plot saved to '{plot_filename}'.")
    plt.close()

if __name__ == "__main__":
    # Example call. Replace "ABC123" with the desired serial number.
    plot_data("data_SN1_W copy 2.csv", "./examples/testing/test_bands.json", "SN1_W")
