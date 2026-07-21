#!/usr/bin/env python3
"""Script to merge all PDF files in the repository into one file."""

import os
from pathlib import Path
from PyPDF2 import PdfMerger

def merge_pdfs():
    """Merge all PDF files in the current directory into one file."""
    
    # Get all PDF files in the repository root directory
    pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.pdf')])
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    print(f"Found {len(pdf_files)} PDF files to merge:")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    # Create merger object
    merger = PdfMerger()
    
    try:
        # Add all PDFs to merger
        for pdf_file in pdf_files:
            print(f"Adding {pdf_file}...")
            try:
                merger.append(pdf_file)
            except Exception as e:
                print(f"Warning: Could not add {pdf_file}: {e}")
                continue
        
        # Write merged PDF
        output_file = "Tong_hop_de_thi_lop_6.pdf"
        print(f"\nMerging into {output_file}...")
        merger.write(output_file)
        merger.close()
        
        # Get file size
        file_size = os.path.getsize(output_file)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✓ Successfully created {output_file}")
        print(f"  File size: {file_size_mb:.2f} MB")
        print(f"  Total pages: Please check the output file")
        
    except Exception as e:
        print(f"Error during merge: {e}")
        merger.close()
        raise

if __name__ == "__main__":
    merge_pdfs()
