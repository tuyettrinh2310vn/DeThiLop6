import os
from PyPDF2 import PdfMerger

def merge_pdfs():
    """Merge all PDF files in the repository into a single PDF."""
    pdf_merger = PdfMerger()
    
    # Find all PDF files (excluding the output file)
    pdf_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories like .github
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in sorted(files):
            if file.endswith('.pdf') and file != 'Tong_hop_de_thi_lop_6.pdf':
                pdf_files.append(os.path.join(root, file))
    
    # Merge PDFs
    if not pdf_files:
        print("No PDF files found to merge")
        return
    
    print(f"Merging {len(pdf_files)} PDF files...")
    for pdf_file in pdf_files:
        print(f"  Adding: {pdf_file}")
        pdf_merger.append(pdf_file)
    
    # Write the merged PDF
    output_file = 'Tong_hop_de_thi_lop_6.pdf'
    pdf_merger.write(output_file)
    pdf_merger.close()
    print(f"Successfully created: {output_file}")

if __name__ == '__main__':
    merge_pdfs()
