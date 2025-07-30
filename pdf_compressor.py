# -*- coding: utf-8 -*-
"""
PDF Compressor Pro
==================

A professional, command-line tool to compress any PDF file.
It intelligently handles both scanned (image-based) and text-based
documents to achieve the best balance of file size and quality.

This script uses the PyMuPDF library for robust and effective PDF manipulation.
"""

import os
import sys
import argparse
import time
import fitz  # PyMuPDF
from PIL import Image
import io

# --- Configuration ---
# Define compression profiles with their associated JPEG quality setting.
# Quality is an integer from 1 (lowest) to 95 (highest).
COMPRESSION_PROFILES = {
    'low': 20,       # Highest compression, smallest size
    'medium': 40,    # Good balance between size and quality (default)
    'high': 60,      # Better quality, larger size
    'best': 80       # Near-original quality, minimal compression
}

DEFAULT_PROFILE = 'medium'
DEFAULT_OUTPUT_DIR = 'compressed_pdfs'

# --- Core Functions ---

def get_output_path(input_path, output_dir, profile_name, quality_val):
    """
    Generates a unique, descriptive output path for the compressed file.
    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"INFO: Created output directory: {output_dir}")
        except OSError as e:
            print(f"ERROR: Could not create output directory {output_dir}. {e}")
            return None

    base_name = os.path.basename(input_path)
    file_name, file_ext = os.path.splitext(base_name)
    
    timestamp = int(time.time())
    new_filename = f"{file_name}__{profile_name}_q{quality_val}_{timestamp}{file_ext}"
    
    return os.path.join(output_dir, new_filename)

def compress_smart(doc, quality):
    """
    Compresses a PDF by selectively re-compressing only the images within it,
    preserving all text and vector graphics. This is the best method for
    mixed-content or text-based PDFs.

    Args:
        doc (fitz.Document): The PyMuPDF document object.
        quality (int): The image compression quality (1-95).

    Returns:
        int: The number of images that were re-compressed.
    """
    image_count = 0
    total_images = 0

    for page_num, page in enumerate(doc):
        sys.stdout.write(f"\r  -> Analyzing page {page_num + 1}/{len(doc)}...")
        sys.stdout.flush()

        for img_index, img in enumerate(page.get_images(full=True)):
            total_images += 1
            xref = img[0]
            
            # Extract the image bytes
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Convert to a PIL Image and compress
                pil_img = Image.open(io.BytesIO(image_bytes))
                img_buffer = io.BytesIO()
                pil_img.save(img_buffer, format="JPEG", quality=quality, optimize=True)
                img_buffer.seek(0)

                # Replace the old image with the new compressed one
                page.update_image(img_buffer.read(), xref=xref)
                image_count += 1
            except Exception:
                # Skip images that cause errors (e.g., non-standard formats)
                continue
    
    print(f"\nINFO: Re-compressed {image_count} out of {total_images} total images.")
    return image_count

def compress_aggressive(doc, quality):
    """
    Compresses a PDF by converting every page into a compressed image.
    This is best for scanned documents with no selectable text.

    Args:
        doc (fitz.Document): The PyMuPDF document object.
        quality (int): The image compression quality (1-95).

    Returns:
        fitz.Document: A new document object with the compressed pages.
    """
    output_doc = fitz.open() # Create a new PDF
    for page_num, page in enumerate(doc):
        sys.stdout.write(f"\r  -> Rasterizing page {page_num + 1}/{len(doc)}...")
        sys.stdout.flush()

        # Get the page as an image
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))

        # Compress the image
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG", quality=quality, optimize=True)
        img_buffer.seek(0)

        # Create a new page and insert the compressed image
        new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=img_buffer)
    
    return output_doc

# --- Main Execution ---

def main():
    """
    Main function to parse arguments and orchestrate the PDF compression.
    """
    parser = argparse.ArgumentParser(
        description="PDF Compressor Pro: A tool for intelligent PDF compression.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "input_file",
        help="Path to the input PDF file to be compressed."
    )
    parser.add_argument(
        "-m", "--mode",
        choices=['smart', 'aggressive'],
        default='smart',
        help="Compression mode:\n"
             "  - smart: (Default) Selectively compresses images, preserving text quality.\n"
             "             Best for text-based or mixed-content PDFs.\n"
             "  - aggressive: Converts entire pages to images. Best for scanned documents."
    )
    parser.add_argument(
        "-p", "--profile",
        choices=COMPRESSION_PROFILES.keys(),
        default=DEFAULT_PROFILE,
        help="Compression profile. Determines the image quality.\n"
             f"  - low:    (quality: {COMPRESSION_PROFILES['low']})\n"
             f"  - medium: (quality: {COMPRESSION_PROFILES['medium']}) (default)\n"
             f"  - high:   (quality: {COMPRESSION_PROFILES['high']})\n"
             f"  - best:   (quality: {COMPRESSION_PROFILES['best']})"
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        metavar="1-95",
        help="Specify a custom compression quality (1-95).\n"
             "This overrides the --profile setting."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save the compressed file.\n(default: ./{DEFAULT_OUTPUT_DIR}/)"
    )

    args = parser.parse_args()

    # --- Input Validation ---
    if not os.path.isfile(args.input_file):
        print(f"ERROR: The file '{args.input_file}' was not found.")
        sys.exit(1)

    if args.quality:
        if not 1 <= args.quality <= 95:
            print("ERROR: Custom quality must be an integer between 1 and 95.")
            sys.exit(1)
        quality_val = args.quality
        profile_name = "custom"
    else:
        quality_val = COMPRESSION_PROFILES[args.profile]
        profile_name = args.profile

    # --- Process ---
    print("-" * 60)
    print("PDF Compressor Pro Initialized")
    print(f"  - Input File:   {os.path.basename(args.input_file)}")
    print(f"  - Mode:         {args.mode.capitalize()}")
    print(f"  - Profile:      {profile_name.capitalize()}")
    print(f"  - Quality:      {quality_val}")
    print(f"  - Output Dir:   {args.output_dir}")
    print("-" * 60)

    output_path = get_output_path(args.input_file, args.output_dir, profile_name, quality_val)
    if not output_path:
        sys.exit(1)
        
    original_size_mb = os.path.getsize(args.input_file) / (1024 * 1024)
    print(f"Original file size: {original_size_mb:.2f} MB")

    start_time = time.time()
    doc = None
    try:
        doc = fitz.open(args.input_file)
        
        if args.mode == 'smart':
            print("Running in Smart mode (preserving text)...")
            compress_smart(doc, quality_val)
            # Save the modified original document
            doc.save(output_path, garbage=4, deflate=True, clean=True)
        
        elif args.mode == 'aggressive':
            print("Running in Aggressive mode (image conversion)...")
            output_doc = compress_aggressive(doc, quality_val)
            output_doc.save(output_path, garbage=4, deflate=True, clean=True)
            output_doc.close()

        success = True
    except Exception as e:
        print(f"\nFATAL ERROR during compression: {e}")
        success = False
    finally:
        if doc:
            doc.close()

    # --- Report Results ---
    if success and os.path.exists(output_path):
        compressed_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        reduction_percent = (1 - compressed_size_mb / original_size_mb) * 100 if original_size_mb > 0 else 0
        duration = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("Compression Successful!")
        print(f"  - Output File:    {output_path}")
        print(f"  - New Size:       {compressed_size_mb:.2f} MB")
        print(f"  - Size Reduction: {reduction_percent:.1f}%")
        print(f"  - Duration:       {duration:.2f} seconds")
        print("=" * 60)
    else:
        print("\n" + "!" * 60)
        print("Compression Failed.")
        if os.path.exists(output_path):
            os.remove(output_path) # Clean up failed file
        print("!" * 60)

if __name__ == "__main__":
    try:
        import fitz
        from PIL import Image
    except ImportError:
        print("ERROR: Missing required libraries. Please run:")
        print("pip install PyMuPDF Pillow")
        sys.exit(1)
        
    main()
