# /// script
# requires-python = ">=3.12"
# ///

"""Simple GUI wrapper for save-layers-my-credentials.py
Just launches a GUI to collect inputs then runs the original script.
"""

import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
import os
import winreg
import shutil
import re

# Get the actual path to the user's Documents folder
def get_documents_path():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            documents_path = winreg.QueryValueEx(key, "Personal")[0]
        return documents_path
    except WindowsError:
        return os.path.expanduser("~/Documents")

# Default folders
DEFAULT_INPUT = r"\\portal-prd\ProLayerfiles"
DEFAULT_OUTPUT = str(Path(get_documents_path()) / "ArcGIS" / "Layers")

# ANSI color code regex
ANSI_RE = re.compile(r'\x1b\[([\d;]+)m')

# ANSI color code to tag mapping
ANSI_TO_TAG = {
    '32': 'success',    # Green
    '31': 'error',      # Red
    '34': 'info',       # Blue
    '33': 'warning',    # Yellow
    '1': 'bold',        # Bold
    '0': None,          # Reset
}

class ColorText(tk.Text):
    """Text widget with color support"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure tags for different styles
        self.tag_configure('success', foreground='green')
        self.tag_configure('error', foreground='red')
        self.tag_configure('info', foreground='blue')
        self.tag_configure('warning', foreground='brown')
        self.tag_configure('bold', font='TkDefaultFont 9 bold')
        
    def append_colored_text(self, text):
        """Append text with ANSI color codes converted to tags"""
        self.config(state='normal')
        
        # Process text segments with color codes
        last_end = 0
        current_tags = set()
        
        for match in ANSI_RE.finditer(text):
            # Add text before the color code
            start, end = match.span()
            if start > last_end:
                self.insert('end', text[last_end:start], tuple(current_tags))
            
            # Update current tags based on color code
            codes = match.group(1).split(';')
            for code in codes:
                if code == '0':  # Reset
                    current_tags.clear()
                elif code in ANSI_TO_TAG:
                    tag = ANSI_TO_TAG[code]
                    if tag:
                        current_tags.add(tag)
            
            last_end = end
        
        # Add remaining text
        if last_end < len(text):
            self.insert('end', text[last_end:], tuple(current_tags))
            
        self.see('end')
        self.config(state='disabled')

def browse_directory(entry):
    """Open file dialog starting from parent of current path"""
    try:
        # Start from parent of current path if it exists
        current = entry.get()
        start_dir = str(Path(current).parent) if current else None
    except ValueError as e:
        start_dir = None
    
    directory = filedialog.askdirectory(initialdir=start_dir)
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def append_output(text):
    """Append text to status widget with color support"""
    status.append_colored_text(text)
    root.update()

def toggle_password():
    """Toggle password visibility"""
    if password.cget('show') == '*':
        password.config(show='')
        show_password.config(text='Hide')
    else:
        password.config(show='*')
        show_password.config(text='Show')

def run_script():
    script_dir = Path(__file__).parent
    credentials_script = script_dir / "save-layers-my-credentials.py"
    
    # Debug info with bold headers
    status.config(state='normal')
    status.delete('1.0', tk.END)
    status.append_colored_text(
        "\n".join([
            f"\x1b[1mScript directory:\x1b[0m\n {script_dir}",
            f"\x1b[1mCredentials script:\x1b[0m\n {credentials_script}",
            f"\x1b[1mScript exists:\x1b[0m\n {credentials_script.exists()}",
            f"\x1b[1mUV executable:\x1b[0m\n {shutil.which('uv')}"
        ])
    )
    status.config(state='disabled')
    root.update()
    
    if not credentials_script.exists():
        append_output(f"\x1b[31mError: Cannot find script at:\n{credentials_script}\x1b[0m\n")
        return
        
    if not shutil.which('uv'):
        append_output("\x1b[31mError: 'uv' command not found in PATH\x1b[0m\n\n")
        append_output("To install UV:\n")
        append_output("\x1b[1m1. Run in PowerShell:\x1b[0m\n")
        append_output("  powershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"\n\n")
        append_output("\x1b[1m2. Make friendly with corporate firewall:\x1b[0m\n")
        append_output("  setx UV_NATIVE_TLS true\n")
        return

    cmd = [
        "uv",
        "run",
        str(credentials_script),
        "--username", username.get(),
        "--password", password.get(),
        "--input-dir", input_dir.get(),
        "--output-dir", output_dir.get()
    ]
    if flatten.get():
        cmd.append("--flatten")
        
    # Show command being executed
    append_output(f"\n\x1b[1mRunning command:\x1b[0m\n{' '.join(cmd)}\n")
    
    try:
        # Run process with real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read output in real-time and add colors
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                # Add colors to specific types of messages
                colored_line = line
                if "Processing" in line:
                    colored_line = f"\x1b[34m{line.strip()}\x1b[0m\n"  # Blue for processing
                elif "Found" in line:
                    colored_line = f"\x1b[33m{line.strip()}\x1b[0m\n"  # Yellow for found
                elif "Successfully processed" in line:
                    colored_line = f"\x1b[32m{line.strip()}\x1b[0m\n"  # Green for success
                elif "Skipped" in line:
                    colored_line = f"\x1b[33m{line.strip()}\x1b[0m\n"  # Yellow for skipped
                elif "Error:" in line or "Failed:" in line:
                    colored_line = f"\x1b[31m{line.strip()}\x1b[0m\n"  # Red for errors
                append_output(colored_line)
        
        return_code = process.wait()
        
        if return_code == 0:
            append_output("\x1b[32mSuccess!\x1b[0m\n")  # Green success message
            # Open output folder in Explorer
            output_path = Path(output_dir.get())
            if output_path.exists():
                subprocess.run(['explorer', str(output_path)], check=False)
            else:
                append_output("\x1b[33mNote: Output folder does not exist yet\x1b[0m\n")  # Yellow warning
    except Exception as e:
        append_output(f"\x1b[31mError: {str(e)}\x1b[0m\n")  # Red error message

def update_text_height(*args):
    """Update Text widget height based on content"""
    num_lines = int(status.index('end-1c').split('.')[0])
    new_height = min(max(12, num_lines), 30)  # Min 12 lines, max 30 lines
    status.configure(height=new_height)
    root.update_idletasks()

root = tk.Tk()
root.title("Update Layer Credentials")

# Calculate initial window width based on wider of input or output paths
test_label = ttk.Label(root)
test_label.grid()

# Test width of input path
test_label.config(text=DEFAULT_INPUT)
input_width = test_label.winfo_reqwidth()

# Test width of output path
test_label.config(text=DEFAULT_OUTPUT)
output_width = test_label.winfo_reqwidth()

# Use the wider of the two paths
width = max(input_width, output_width) + 250  # Add space for padding and browse button
test_label.grid_remove()
root.geometry(f"{width}x600")  # Increase initial window height

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

# Title and subtitle
title = ttk.Label(frame, text=root.title(), font="TkDefaultFont 12 bold")
title.grid(row=0, column=0, columnspan=3, pady=(0,2), sticky="w")
subtitle = ttk.Label(frame, text="Change ArcGIS Pro layers to use specified DB login credentials and save in specified location.\n\nIt takes about a minute to process 500 files, the window appears to freeze occasionally, that's okay.\n\nWARNING: password is saved in plaintext in the .lyrx files, so select Ouput folder within personal profile. Password is not tested for validity.", 
                    wraplength=width-40, font="TkDefaultFont 9")
subtitle.grid(row=1, column=0, columnspan=3, pady=(0,10), sticky="w")

# Username
ttk.Label(frame, text="Username:").grid(row=2, column=0, sticky="w")
username = ttk.Entry(frame)
username.insert(0, os.environ.get('USERNAME'))
username.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# Password with show/hide toggle
ttk.Label(frame, text="Password:").grid(row=3, column=0, sticky="w")
password_frame = ttk.Frame(frame)  # Frame to hold password entry and show/hide button
password_frame.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
password_frame.columnconfigure(0, weight=1)  # Make password entry expand

password = ttk.Entry(password_frame, show="*")
password.grid(row=0, column=0, sticky="ew")

show_password = ttk.Button(password_frame, text="Show", width=6, command=toggle_password)
show_password.grid(row=0, column=1, padx=(5,0))

# Input dir
ttk.Label(frame, text="In Layerfiles folder:").grid(row=4, column=0, sticky="w")
input_dir = ttk.Entry(frame)
input_dir.insert(0, DEFAULT_INPUT)
input_dir.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame, text="Browse", 
           command=lambda: browse_directory(input_dir)).grid(row=4, column=2)

# Output dir
ttk.Label(frame, text="Output folder:").grid(row=5, column=0, sticky="w")
output_dir = ttk.Entry(frame)
output_dir.insert(0, DEFAULT_OUTPUT)
output_dir.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame, text="Browse",
           command=lambda: browse_directory(output_dir)).grid(row=5, column=2)

# Flatten option
flatten = tk.BooleanVar()
ttk.Checkbutton(frame, text="Flatten output", variable=flatten).grid(row=6, column=0, columnspan=3, pady=5, sticky="w")

# Run button
ttk.Button(frame, text="Run", command=run_script).grid(row=7, column=0, columnspan=3, pady=10)

# Status with text that can be selected/copied
status_frame = ttk.Frame(frame)  # Create a frame for status and scrollbar
status_frame.grid(row=8, column=0, columnspan=3, pady=10, sticky="nsew")
status_frame.columnconfigure(0, weight=1)
status_frame.rowconfigure(0, weight=1)

status = ColorText(status_frame, height=12, wrap=tk.WORD)
status.insert('1.0', "Ready")
status.config(state='disabled')  # Make read-only
status.grid(row=0, column=0, sticky="nsew")

# Add scrollbar
scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=status.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
status.configure(yscrollcommand=scrollbar.set)

# Bind text changes to height update
status.bind('<<Modified>>', update_text_height)

# Configure grid expansion
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)  # Make the entry column expandable
frame.columnconfigure(0, weight=0)  # Keep label column fixed
frame.columnconfigure(2, weight=0)  # Keep button column fixed
frame.rowconfigure(8, weight=1)     # Allow status row to expand

root.mainloop()
