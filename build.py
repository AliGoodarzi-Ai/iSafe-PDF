# -*- coding: utf-8 -*-
"""
Build Script for PDF Compressor
===============================

This script prepares the PDF Compressor tool for distribution.
It performs the following actions:

1.  **Installs Dependencies**: Ensures that all required libraries
    (PyMuPDF, Pillow) are installed in the current Python environment.
2.  **Creates an Executable**: Uses PyInstaller to bundle the
    `pdf_compressor.py` script and its dependencies into a single,
    standalone executable file (`.exe` on Windows).

This allows the tool to be run on other machines without needing to
install Python or any libraries manually.
"""

import os
import sys
import subprocess

# --- Configuration ---
SCRIPT_TO_BUNDLE = "pdf_compressor.py"
EXECUTABLE_NAME = "pdf_compressor"
ICON_FILE = "icon.ico" # Optional: Create an icon for your app

# --- Functions ---

def install_dependencies():
    """
    Installs required packages using pip.
    """
    required_packages = ["PyMuPDF", "Pillow", "pyinstaller"]
    print("--- Checking and Installing Dependencies ---")
    for package in required_packages:
        try:
            print(f"Installing {package}...")
            # Use sys.executable to ensure pip from the correct env is used
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )
            print(f"  - {package} is installed.")
        except subprocess.CalledProcessError:
            print(f"  - FAILED to install {package}. Please install it manually.")
            return False
    print("All dependencies are satisfied.\n")
    return True

def create_executable():
    """
    Uses PyInstaller to create a standalone executable.
    """
    print("--- Creating Standalone Executable with PyInstaller ---")
    if not os.path.exists(SCRIPT_TO_BUNDLE):
        print(f"Error: The main script '{SCRIPT_TO_BUNDLE}' was not found.")
        print("Cannot build the executable.")
        return

    # PyInstaller command arguments
    command = [
        "pyinstaller",
        "--name", EXECUTABLE_NAME,
        "--onefile",          # Bundle everything into a single .exe
        "--windowed",         # Use '--console' for a visible command window
        "--clean",            # Clean PyInstaller cache
        SCRIPT_TO_BUNDLE
    ]

    # Add an icon if it exists
    if os.path.exists(ICON_FILE):
        print(f"Using icon: {ICON_FILE}")
        command.extend(["--icon", ICON_FILE])
    else:
        print("No icon file found (optional).")

    print(f"Running PyInstaller command: {' '.join(command)}")
    
    try:
        subprocess.check_call(command)
        print("\n--- Build Successful! ---")
        print(f"Executable created in the '{os.getcwd()}\\dist' directory.")
        print("You can now share the .exe file with others.")
    except subprocess.CalledProcessError as e:
        print("\n--- Build Failed! ---")
        print(f"PyInstaller returned an error: {e}")
        print("Check the output above for more details.")
    except FileNotFoundError:
        print("\n--- Build Failed! ---")
        print("Error: 'pyinstaller' command not found.")
        print("Please ensure PyInstaller was installed correctly.")

# --- Main Execution ---

if __name__ == "__main__":
    print("=" * 50)
    print("PDF Compressor Build Process Started")
    print("=" * 50)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        sys.exit(1) # Exit if dependencies fail

    # Step 2: Create the executable
    create_executable()
    
    print("\n" + "=" * 50)
    print("Build Process Finished")
    print("=" * 50)
