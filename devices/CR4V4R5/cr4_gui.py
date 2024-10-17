import os
import sys
import tkinter as tk
from tkinter import scrolledtext, Button, Label, Frame, Canvas, ttk
import subprocess
import threading
import queue

# Define the path to the examples directory
path = 'examples'

# Get all folders and Python files from the examples directory
try:
    example_folders = [
        f for f in os.listdir(path)
        if os.path.isdir(os.path.join(path, f))
    ]
    print(example_folders)
except FileNotFoundError:
    print(f"The directory '{path}' does not exist.")
    sys.exit(1)

# Create the main application window
root = tk.Tk()
root.title("CR4 Hardware UI - Python Scripts")
root.geometry("1000x750")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Create a frame for the console output
console_frame = Frame(root)
console_frame.grid(column=0, row=1, columnspan=4, padx=10, pady=10, sticky="nsew")
console_frame.columnconfigure(0, weight=1)
console_frame.rowconfigure(1, weight=1)

# Add a title label for the console
console_label = Label(console_frame, text="Console Output", font=("Helvetica", 14, "bold"))
console_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")

# Create a scrolled text widget for output
output_text = scrolledtext.ScrolledText(
    console_frame,
    wrap=tk.WORD,
    width=120,
    height=20,
    font=('Courier', 10)
)
output_text.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

# Create a Notebook widget to hold tabs for each folder
tabs = ttk.Notebook(root)
tabs.grid(column=0, row=2, columnspan=4, padx=10, pady=10, sticky="nsew")

# Create a frame and buttons for each folder
for folder in example_folders:
    folder_path = os.path.join(path, folder)
    tab_frame = Frame(tabs)
    tabs.add(tab_frame, text=folder)
    tab_frame.columnconfigure(tuple(range(4)), weight=1)

    # Get all Python files in the current folder
    python_files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(".py")
    ]

    # Create buttons for each Python file
    if python_files:
        for idx, file in enumerate(python_files):
            button = Button(
                tab_frame,
                text=file.split('.')[0],
                command=lambda f=os.path.join(folder, file): handle_python_click(f),
                width=20,
                height=2
            )
            button.grid(column=idx % 4, row=idx // 4 + 1, padx=10, pady=5, sticky="nsew")
    else:
        no_files_label = Label(tab_frame, text="No Python scripts found.", font=("Helvetica", 12))
        no_files_label.grid(column=0, row=1, columnspan=4, padx=5, pady=5, sticky="w")

# Global variables to keep track of the subprocess and its output queue
current_process = None
current_filename = None  # To keep track of the filename

# Create a unified output queue
output_queue = queue.Queue()

# Redirect stdout to the GUI console
class StdoutRedirector:
    def __init__(self, queue):
        self.queue = queue
        self.original_stdout = sys.__stdout__

    def write(self, message):
        if message:
            self.queue.put(message)

    def flush(self):
        self.original_stdout.flush()

sys.stdout = StdoutRedirector(output_queue)

def handle_python_click(filename):
    global current_process, current_filename
    if current_process is not None and current_process.poll() is None:
        print("A process is already running. Please stop it before starting a new one.")
        return
    try:
        # Run the Python script asynchronously with unbuffered output
        process = subprocess.Popen(
            [sys.executable, '-u', os.path.join(path, filename)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Start threads to read stdout and stderr
        threading.Thread(target=enqueue_subprocess_output, args=(process.stdout,), daemon=True).start()
        threading.Thread(target=enqueue_subprocess_output, args=(process.stderr,), daemon=True).start()
        threading.Thread(target=monitor_subprocess, args=(process, filename), daemon=True).start()
        current_process = process
        current_filename = filename  # Store the filename
        print(f"Started Python script: {filename}")
    except Exception as e:
        print(f"Failed to run Python script {filename}: {e}")

def enqueue_subprocess_output(pipe):
    try:
        for line in iter(pipe.readline, ''):
            if line:
                output_queue.put(line)
        pipe.close()
    except Exception as e:
        output_queue.put(f"Error reading subprocess output: {e}\n")

def monitor_subprocess(process, filename):
    process.wait()
    print(f"Script '{filename}' has completed.")
    # Reset the current process and filename
    global current_process, current_filename
    current_process = None
    current_filename = None
    # Check and update PLL Lock status
    # lock_status = check_pll_lock_status()  # Replace with actual logic to determine lock status
    # update_pll_lock_led(lock_status)

def stop_process():
    global current_process, current_filename
    if current_process is not None and current_process.poll() is None:
        current_process.terminate()
        current_process = None
        current_filename = None
        print("Process terminated by user.\n")
    else:
        print("No process is currently running.\n")

def process_output_queue():
    while True:
        try:
            message = output_queue.get_nowait()
        except queue.Empty:
            break
        else:
            if '__CLEAR_CONSOLE__' in message:
                # Clear the console
                output_text.delete('1.0', tk.END)
                # Remove the marker from the message
                message = message.replace('__CLEAR_CONSOLE__', '')
            output_text.insert(tk.END, message)
            output_text.yview(tk.END)
    # Schedule the next check
    root.after(100, process_output_queue)

# def update_pll_lock_led(lock_status):
#     """Update the PLL Lock LED based on the provided lock status."""
#     if lock_status:
#         pll_lock_canvas.itemconfig(pll_lock_led, fill="lightgreen")
#     else:
#         pll_lock_canvas.itemconfig(pll_lock_led, fill="grey")

# def check_pll_lock_status():
#     """Placeholder function to check PLL Lock status. Replace with actual implementation."""
#     # Replace with logic to determine PLL lock status
#     return True

# Add a Stop button
stop_button = Button(
    root,
    text="Stop",
    command=stop_process,
    width=20,
    height=2
)
# Position the Stop button in a separate row
stop_button.grid(
    column=0,
    row=3,
    columnspan=4,
    padx=10,
    pady=10
)

# Start processing the output queue
root.after(100, process_output_queue)

# Ensure subprocesses are terminated and resources are cleaned up when exiting
def on_closing():
    global current_process
    if current_process is not None and current_process.poll() is None:
        current_process.terminate()
        print("Terminated running subprocess on exit.\n")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()
