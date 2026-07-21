#!/usr/bin/env python3
"""Script to extract only question parts from PDFs and merge them."""

import os
from PyPDF2 import PdfReader, PdfWriter

def main():
    """Main function."""
    
    # Get all PDF files
    all_files = sorted([f for f in os.listdir('.') if f.endswith('.pdf')])
    
    # Remove output file from list
    if 'Tong_hop_de_thi_lop_6.pdf' in all_files:
        all_files.remove('Tong_hop_de_thi_lop_6.pdf')
    
    if not all_files:
        print("ERROR: No PDF files found!")
        return
    
    print("="*80)
    print(f"PROCESSING {len(all_files)} FILES")
    print("="*80)
    
    # Create ONE final merger object
    final_merger = PdfWriter()
    
    total_pages_added = 0
    
    # Process EACH file ONE time only
    for file_num, pdf_file in enumerate(all_files, 1):
        print(f"\n[{file_num}/{len(all_files)}] {pdf_file}")
        
        try:
            # Open this file
            reader = PdfReader(pdf_file)
            original_page_count = len(reader.pages)
            print(f"  Original pages: {original_page_count}")
            
            pages_from_this_file = 0
            solution_found_at_page = None
            
            # Go through EACH page in this file
            for page_idx in range(len(reader.pages)):
                page = reader.pages[page_idx]
                
                try:
                    text = page.extract_text() or ""
                except:
                    text = ""
                
                # Check if this page has solution marker
                if "HƯỚNG DẪN GIẢI CHI TIẾT" in text:
                    solution_found_at_page = page_idx + 1
                    print(f"  Found solution at page {solution_found_at_page}, STOPPING")
                    break
                
                # Add this page to final output (ONLY ONCE)
                final_merger.add_page(page)
                pages_from_this_file += 1
                total_pages_added += 1
            
            # Report for this file
            if solution_found_at_page:
                removed = original_page_count - pages_from_this_file
                print(f"  Added to output: {pages_from_this_file} pages")
                print(f"  Removed (solution): {removed} pages")
            else:
                print(f"  Added to output: {pages_from_this_file} pages")
                print(f"  Removed: 0 pages (no solution section)")
        
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
    
    # Write final output file (ONCE)
    output_file = "Tong_hop_de_thi_lop_6.pdf"
    print(f"\n{'='*80}")
    print(f"WRITING OUTPUT FILE: {output_file}")
    print(f"Total pages to write: {total_pages_added}")
    
    with open(output_file, 'wb') as f:
        final_merger.write(f)
    
    output_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"File size: {output_size:.2f} MB")
    print(f"{'='*80}")
    
    # Verify output
    print(f"\nVERIFICATION:")
    verify_reader = PdfReader(output_file)
    output_page_count = len(verify_reader.pages)
    print(f"Output file has: {output_page_count} pages\n")
    
    problems = 0
    for page_idx in range(len(verify_reader.pages)):
        try:
            text = verify_reader.pages[page_idx].extract_text() or ""
        except:
            text = ""
        
        if "HƯỚNG DẪN GIẢI CHI TIẾT" in text:
            print(f"  ❌ Page {page_idx + 1}: FOUND SOLUTION TEXT!")
            problems += 1
    
    print(f"\n{'='*80}")
    if problems == 0:
        print(f"✅ SUCCESS: Output is CLEAN!")
        print(f"   - {output_page_count} pages total")
        print(f"   - No 'HƯỚNG DẪN GIẢI CHI TIẾT' found")
        print(f"   - File size: {output_size:.2f} MB")
    else:
        print(f"❌ FAILED: Found solution text on {problems} page(s)!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
