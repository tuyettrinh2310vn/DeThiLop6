#!/usr/bin/env python3
"""Script to extract only question parts from PDFs and merge them."""

import os
from PyPDF2 import PdfReader, PdfWriter

def find_solution_start_page(pdf_file):
    """Find the page number where solution section starts."""
    try:
        reader = PdfReader(pdf_file)
        
        for page_idx in range(len(reader.pages)):
            page = reader.pages[page_idx]
            
            try:
                text = page.extract_text() or ""
            except:
                text = ""
            
            # Check for solution marker
            if "HƯỚNG DẪN GIẢI CHI TIẾT" in text:
                return page_idx  # Return 0-indexed page number
        
        return None  # No solution section found
    
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        return None

def extract_question_pages(pdf_file):
    """Extract only question pages (before solution section)."""
    try:
        reader = PdfReader(pdf_file)
        
        # Find where solution starts
        solution_page = find_solution_start_page(pdf_file)
        
        if solution_page is None:
            # No solution section, keep all pages
            return list(range(len(reader.pages))), None
        else:
            # Keep pages BEFORE solution section
            return list(range(solution_page)), solution_page
    
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")
        return [], None

def main():
    """Main function."""
    
    output_file = "Tong_hop_de_thi_lop_6.pdf"
    
    # DELETE output file if it exists (start fresh)
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"Removed existing {output_file}\n")
    
    # Get all PDF files
    all_files = sorted([f for f in os.listdir('.') if f.endswith('.pdf')])
    
    # Make sure output file is not in the list
    if output_file in all_files:
        all_files.remove(output_file)
    
    if not all_files:
        print("ERROR: No PDF files found!")
        return
    
    print("="*80)
    print(f"PROCESSING {len(all_files)} FILES - EXTRACTING QUESTIONS ONLY")
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
            
            # Find which pages to keep
            pages_to_keep, solution_page = extract_question_pages(pdf_file)
            
            # Add ONLY the question pages to output
            for page_idx in pages_to_keep:
                page = reader.pages[page_idx]
                final_merger.add_page(page)
                total_pages_added += 1
            
            # Report for this file
            if solution_page is not None:
                removed = original_page_count - len(pages_to_keep)
                print(f"  ✓ Added {len(pages_to_keep)} question pages")
                print(f"  ✓ Removed {removed} pages (solution from page {solution_page + 1})")
            else:
                print(f"  ✓ Added all {len(pages_to_keep)} pages (no solution found)")
        
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            continue
    
    # Write final output file (ONCE)
    print(f"\n{'='*80}")
    print(f"WRITING OUTPUT FILE: {output_file}")
    print(f"Total pages to write: {total_pages_added}")
    
    with open(output_file, 'wb') as f:
        final_merger.write(f)
    
    output_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"File size: {output_size:.2f} MB")
    print(f"{'='*80}")
    
    # FINAL VERIFICATION
    print(f"\nFINAL VERIFICATION: Checking for solution text in output...")
    print(f"{'='*80}")
    
    verify_reader = PdfReader(output_file)
    output_page_count = len(verify_reader.pages)
    print(f"Output file has: {output_page_count} total pages\n")
    
    violation_pages = []
    
    for page_idx in range(len(verify_reader.pages)):
        try:
            text = verify_reader.pages[page_idx].extract_text() or ""
        except:
            text = ""
        
        if "HƯỚNG DẪN GIẢI CHI TIẾT" in text:
            violation_pages.append(page_idx + 1)
    
    print(f"{'='*80}")
    if len(violation_pages) == 0:
        print(f"✅ SUCCESS!")
        print(f"   - {output_page_count} pages extracted")
        print(f"   - NO 'HƯỚNG DẪN GIẢI CHI TIẾT' found")
        print(f"   - Output contains ONLY questions")
        print(f"   - File size: {output_size:.2f} MB")
    else:
        print(f"❌ FAILED!")
        print(f"   - Found 'HƯỚNG DẪN GIẢI CHI TIẾT' on {len(violation_pages)} page(s)")
        print(f"   - Pages with violation: {violation_pages}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
