import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "data_SN1_W.csv"  # Replace with your file path

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Group by 'Channel' and create a plot for each channel
for channel in df['Channel'].unique():
    channel_data = df[df['Channel'] == channel]
    bands = channel_data['Band'].unique()

    # Create a figure with subplots for each band
    fig, axes = plt.subplots(len(bands), 1, figsize=(10, 6 * len(bands)))
    if len(bands) == 1:
        axes = [axes]  # Ensure axes is always a list

    for ax, band in zip(axes, bands):
        band_data = channel_data[channel_data['Band'] == band]

        # Exclude the first and last data points
        if len(band_data) > 2:
            band_data = band_data.iloc[1:-1]

        # Plot gain values over the index
        ax.plot(band_data.index, band_data['Gain_dBm'], marker='o', label=f"{band}")
        ax.set_title(f"Channel {channel} - Band {band}")
        ax.set_xlabel("Index")
        ax.set_ylabel("Gain (dBm)")
        ax.grid(True)
        ax.legend()

    # Adjust layout to make each subplot take the full width
    plt.tight_layout(rect=[0, 0, 1, 1])
    output_file = f"channel_{channel}_all_bands.png"
    plt.savefig(output_file)
    plt.close()