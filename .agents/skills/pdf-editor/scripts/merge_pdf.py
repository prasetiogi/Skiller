#!/usr/bin/env python3
"""
Merge multiple PDF files into one

Usage:
    merge_pdf.py <output.pdf> <input1.pdf> <input2.pdf> [<input3.pdf> ...]

Arguments:
    output.pdf     Path for the merged output PDF
    input*.pdf     Two or more PDF files to merge (in order)

Examples:
    merge_pdf.py merged.pdf doc1.pdf doc2.pdf
    merge_pdf.py report.pdf cover.pdf chapter1.pdf chapter2.pdf appendix.pdf
"""

import sys
from pathlib import Path

try:
    from pypdf import PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def merge_pdfs(output_path, input_paths):
    """
    Merge multiple PDF files into a single output PDF.

    Args:
        output_path: Path for the merged output PDF
        input_paths: List of paths to input PDF files (merged in order)
    """
    writer = PdfWriter()
    total_pages = 0

    for input_path in input_paths:
        if not Path(input_path).exists():
            print(f"Error: File not found: {input_path}")
            sys.exit(1)

        writer.append(input_path)
        from pypdf import PdfReader
        page_count = len(PdfReader(input_path).pages)
        total_pages += page_count
        print(f"  Added: {input_path} ({page_count} page(s))")

    with open(output_path, 'wb') as f:
        writer.write(f)

    print(f"\n✅ Merged {len(input_paths)} file(s) → {total_pages} total page(s)")
    print(f"   Output: {output_path}")


def main():
    args = sys.argv[1:]

    if len(args) < 3:
        print("Usage: merge_pdf.py <output.pdf> <input1.pdf> <input2.pdf> [<input3.pdf> ...]")
        print("Error: At least 2 input files required")
        sys.exit(1)

    output_path = args[0]
    input_paths = args[1:]

    merge_pdfs(output_path, input_paths)


if __name__ == "__main__":
    main()
