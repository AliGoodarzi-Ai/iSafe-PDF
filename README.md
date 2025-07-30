# iSafe PDF - The Ultimate PDF Tool
```

 ██  ███████╗  █████╗  ███████╗███████╗    ██████╗  ██████╗  ███████╗
     ██╔═══ ╝ ██╔══██╗ ██╔════╝██╔════╝    ██╔══██╗ ██╔══██╗ ██╔════╝
 ██╗ ███████╗ ███████║ █████╗  █████╗      ██████╔╝ ██║  ██║ █████╗
 ██║ ╚════██║ ██╔══██║ ██╔══╝  ██╔══╝      ██╔═══╝  ██║  ██║ ██╔══╝
 ██║ ███████║ ██║  ██║ ██║     ███████╗    ██║      ██████╔╝ ██║
 ╚═╝ ╚══════╝ ╚═╝  ╚═╝ ╚═╝     ╚══════╝    ╚═╝      ╚═════╝  ╚═╝

================================================================================
                  iSafe PDF - The Ultimate PDF Tool by Ali Goodarzi
================================================================================
```
A professional, command-line utility to compress, enhance, and archive PDF files with advanced image optimization capabilities.


## Overview

This tool provides high-quality PDF manipulation using the PyMuPDF (fitz) library. It's designed for both technical users who prefer command-line interfaces and non-technical users who need a simple, menu-driven solution.

## Features

-   **Multi-Function**: Compress, Enhance, or Archive your PDFs.
-   **Intelligent Compression**:
    -   **Smart Mode**: Compresses only images, preserving 100% of text and vector quality. Perfect for mixed-content documents.
    -   **Aggressive Mode**: Converts entire pages to compressed images for maximum size reduction. Ideal for scanned documents.
    -   **Archival Mode**: Applies lossless compression, optimizing the file structure without reducing quality.
-   **Quality Enhancement**:
    -   Increases the resolution (DPI) of the entire document, making text and images sharper and clearer. Ideal for improving the quality of old scans.
-   **Flexible Interface**: A powerful command-line tool and a user-friendly Windows batch file (`compress.bat`).
-   **Standalone Executable**: A `build.py` script is included to package the tool into a single `.exe` file using PyInstaller, allowing it to run on any Windows machine without installing Python.

## Installation

### Prerequisites

-   Python 3.7 or higher
-   Windows (for `.bat` file usage)

### Setup

1.  Clone or download this repository.
2.  It's recommended to create a virtual environment:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
3.  Install the required packages:
    ```bash
    pip install PyMuPDF Pillow
    ```
4.  Ensure `pdf_compressor.py` and `compress.bat` are in the same directory.

## Usage

### Method 1: Windows Batch File (Recommended for most users)

Simply double-click `compress.bat`.

1.  **Enter the path** to your PDF file.
2.  **Choose a task**:
    -   `[1] Compress PDF`: To reduce file size.
    -   `[2] Enhance PDF`: To increase quality and sharpness.
3.  **Follow the on-screen menus** to select the appropriate mode and profile for your chosen task.

The processed file will be saved in a new `processed_pdfs` folder.

### Method 2: Command Line Interface (Advanced Users)

The CLI is now task-based. You must specify whether you want to `compress` or `enhance`.

#### To Compress a PDF

```bash
# General syntax
python pdf_compressor.py compress <input_file> --mode <mode> --profile <profile>

# Example: Smart compress with medium quality
python pdf_compressor.py compress "C:\docs\my_report.pdf" --mode smart --profile medium

# Example: Aggressive compress with low quality for max size reduction
python pdf_compressor.py compress "C:\scans\receipt.pdf" --mode aggressive --profile low

# Example: Lossless archival compression
python pdf_compressor.py compress "C:\archive\important.pdf" --mode archival
```

#### To Enhance a PDF

```bash
# General syntax
python pdf_compressor.py enhance <input_file> --profile <profile>

# Example: Enhance to crisp 300 DPI
python pdf_compressor.py enhance "C:\docs\blurry_scan.pdf" --profile high

# Example: Enhance to 600 DPI for professional printing
python pdf_compressor.py enhance "C:\docs\for_print.pdf" --profile archive
```

#### Get Help

```bash
# General help
python pdf_compressor.py --help

# Help for the 'compress' task
python pdf_compressor.py compress --help

# Help for the 'enhance' task
python pdf_compressor.py enhance --help
```

## Building the Executable

To create a standalone `pdf_compressor.exe` that can be run on any Windows computer (even without Python installed), simply run the build script:

```bash
python build.py
```

This requires `pyinstaller` to be installed (`pip install pyinstaller`). The final `.exe` will be located in the `dist` folder.

---

**iSafe PDF - The Ultimate PDF Tool**  
*Professional PDF manipulation made simple*
