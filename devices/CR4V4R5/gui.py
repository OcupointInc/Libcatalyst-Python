import json
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, Button, Label, Frame
from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.devices.CR4V5 import CR4V4R5
import subprocess
import threading
import queue

# Initialize the driver and device
driver = FTDISPIDriver("configs/CR4_V4_FTDI.json", debug=True)
cr4 = CR4V4R5(driver)

# Get all JSON and Python files from the examples directory
path = 'examples'
file_list = [
    f for f in os.listdir(path)
    if os.path.isfile(os.path.join(path, f)) and (f.lower().endswith(".json") or f.lower().endswith(".py"))
]

# Create the main application window
root = tk.Tk()
root.title("CR4 Hardware UI")
root.geometry("1000x750")

# Create a frame for the console output
console_frame = Frame(root)
console_frame.grid(column=0, row=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Add a title label for the console
console_label = Label(console_frame, text="Console Output", font=("Helvetica", 14, "bold"))
console_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")

# Create a scrolled text widget for output
output_text = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, width=120, height=20, font=('Courier', 10))
output_text.grid(column=0, row=1, padx=10, pady=10)

# Create a frame for the script buttons
button_frame = Frame(root)
button_frame.grid(column=0, row=1, columnspan=4, padx=10, pady=10, sticky="nsew")

# Add a title label for the script buttons
scripts_label = Label(button_frame, text="Scripts", font=("Helvetica", 14, "bold"))
scripts_label.grid(column=0, row=0, columnspan=4, padx=5, pady=5, sticky="w")

# Global variables to keep track of the subprocess and its output queue
current_process = None
current_output_queue = None
process_threads = []  # To keep track of the threads
current_filename = None  # To keep track of the filename

# Redirect stdout to the GUI console
class StdoutRedirector:
    def __init__(self):
        self.original_stdout = sys.__stdout__

    def write(self, message):
        self.original_stdout.write(message)
        self.original_stdout.flush()
        # Ensure GUI updates happen in the main thread
        root.after(0, update_output, message)

    def flush(self):
        self.original_stdout.flush()

sys.stdout = StdoutRedirector()

def handle_button_click(filename):
    global current_process, current_output_queue, process_threads, current_filename
    if filename.endswith(".json"):
        try:
            # Load JSON configuration
            with open(os.path.join(path, filename), 'r') as json_file:
                config = json.load(json_file)

            # [Existing JSON handling code...]
            # Tune based on JSON configuration
            pll_b_freq_mhz = config.get("pll_b_frequency_mhz", 10000)
            pll_d_freq_mhz = config.get("pll_d_frequency_mhz", 10000)

            # Tune the PLLs
            cr4.tune_pll("D", pll_d_freq_mhz)
            cr4.tune_pll("B", pll_b_freq_mhz)

            # Set the unused PLLs into reset mode
            cr4.plls["A"].reset_enable(1)
            cr4.plls["C"].reset_enable(1)

            # Set the converter switches to specified conversion mode
            switch_state_12 = config.get("conversion_switch_state_ch_1_2", "single")
            switch_state_34 = config.get("conversion_switch_state_ch_3_4", "single")
            cr4.set_switch("AB", switch_state_12)
            cr4.set_switch("CD", switch_state_34)

            # Set the attenuators
            attenuation_db = config.get("rf_attenuation_db", 0)
            cr4.set_attenuation_db([1, 2, 3, 4], attenuation_db)

            # Tune the filter settings
            lpf_switch = config.get("rf_filter_lpf_switch", 0)
            lpf_band = config.get("rf_filter_lpf_band", 0)
            hpf_switch = config.get("rf_filter_hpf_switch", 0)
            hpf_band = config.get("rf_filter_hpf_band", 0)
            cr4.tune_filters(lpf_switch, lpf_band, hpf_switch, hpf_band)

            with open(os.path.join(path, filename), 'r') as json_file:
                config = json.load(json_file)
                print(json.dumps(config, indent=2))

            print(f"Tuned {filename} successfully.\n")  # Use print instead of update_output

        except Exception as e:
            print(f"Failed to tune configuration from {filename}: {e}\n")  # Use print instead of update_output

    elif filename.endswith(".py"):
        if current_process is not None and current_process.poll() is None:
            print("A process is already running. Please stop it before starting a new one.\n")
            return
        try:
            # Run the Python script asynchronously with unbuffered output
            process = subprocess.Popen(
                [sys.executable, '-u', os.path.join(path, filename)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output_queue = queue.Queue()
            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=enqueue_output, args=(process.stdout, output_queue), daemon=True)
            stderr_thread = threading.Thread(target=enqueue_output, args=(process.stderr, output_queue), daemon=True)
            stdout_thread.start()
            stderr_thread.start()
            process_threads = [stdout_thread, stderr_thread]
            current_process = process
            current_output_queue = output_queue
            current_filename = filename  # Store the filename
            root.after(100, lambda: check_queue(output_queue, process, filename))
        except Exception as e:
            print(f"Failed to run Python script {filename}: {e}\n")

def enqueue_output(out, output_queue):
    try:
        for line in iter(out.readline, ''):
            output_queue.put(line)
        out.close()
    except Exception as e:
        # Handle exceptions if needed
        pass

def check_queue(output_queue, process, filename):
    try:
        while True:
            line = output_queue.get_nowait()
            update_output(line)
    except queue.Empty:
        pass
    if process.poll() is None:
        # Process is still running, check again after 100 ms
        root.after(100, lambda: check_queue(output_queue, process, filename))
    else:
        # Process has finished, read any remaining output
        while not output_queue.empty():
            line = output_queue.get_nowait()
            update_output(line)
        print(f"Script '{filename}' has completed.\n")  # Include the filename in the message
        # Reset the current process and queue
        global current_process, current_output_queue, current_filename
        current_process = None
        current_output_queue = None
        current_filename = None

def stop_process():
    global current_process, current_output_queue, current_filename
    if current_process is not None and current_process.poll() is None:
        current_process.terminate()
        current_process = None
        current_output_queue = None
        print("Process terminated by user.\n")
    else:
        print("No process is currently running.\n")

def update_output(message):
    if '__CLEAR_CONSOLE__' in message:
        # Clear the console
        output_text.delete('1.0', tk.END)
        # Remove the marker from the message
        message = message.replace('__CLEAR_CONSOLE__', '')
    output_text.insert(tk.END, message)
    output_text.yview(tk.END)

# Create buttons for each JSON and Python file
for idx, file in enumerate(file_list):
    button = Button(button_frame, text=file.split('.')[0], command=lambda f=file: handle_button_click(f), width=20, height=2)
    button.grid(column=idx % 4, row=idx // 4 + 1, padx=10, pady=5)

# Add a Stop button
stop_button = Button(button_frame, text="Stop", command=stop_process, width=20, height=2)
stop_button.grid(column=0, row=len(file_list) // 4 + 2, columnspan=4, padx=10, pady=5)

# Start the Tkinter main loop
root.mainloop()