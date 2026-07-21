#!/usr/bin/env python3
"""Script to extract only question parts from PDFs and merge them."""

import os
from PyPDF2 import PdfReader, PdfWriter
import re

def extract_question_pages(pdf_file):
    """Extract only question pages from a PDF (up to 'HƯỚNG DẪN GIẢI CHI TIẾT')."""
    try:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        
        found_end = False
        pages_added = 0
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Check if this page contains the "HƯỚNG DẪN GIẢI CHI TIẾT" text
            if "HƯỚNG DẪN GIẢI CHI TIẾT" in text:
                # Don't add this page, just mark that we found the end
                found_end = True
                break
            
            # Add page to writer
            writer.add_page(page)
            pages_added += 1
        
        return writer, pages_added
    
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")
        return None, 0

def merge_question_sections():
    """Extract and merge question sections from all PDFs."""
    
    # Get all PDF files in the repository root directory
    pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.pdf')])
    
    # Remove the output file if it exists (to avoid processing it)
    if 'Tong_hop_de_thi_lop_6.pdf' in pdf_files:
        pdf_files.remove('Tong_hop_de_thi_lop_6.pdf')
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process:")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    # Create final merger
    final_merger = PdfWriter()
    total_pages = 0
    processed_files = 0
    
    try:
        for pdf_file in pdf_files:
            print(f"\nProcessing {pdf_file}...")
            writer, pages_added = extract_question_pages(pdf_file)
            
            if writer is not None and pages_added > 0:
                # Add all pages from this file to final merger
                for page_num in range(len(writer.pages)):
                    final_merger.add_page(writer.pages[page_num])
                    total_pages += 1
                
                print(f"  ✓ Added {pages_added} question pages")
                processed_files += 1
            else:
                print(f"  ✗ No question pages extracted")
        
        # Write final merged PDF
        output_file = "Tong_hop_de_lop_6.pdf"
        print(f"\nCreating {output_file}...")
        
        with open(output_file, 'wb') as output:
            final_merger.write(output)
        
        # Get file size
        file_size = os.path.getsize(output_file)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n✓ Successfully created {output_file}")
        print(f"  Total pages: {total_pages}")
        print(f"  Files processed: {processed_files}/{len(pdf_files)}")
        print(f"  File size: {file_size_mb:.2f} MB")
        
    except Exception as e:
        print(f"Error during merge: {e}")
        raise

if __name__ == "__main__":
    merge_question_sections()
