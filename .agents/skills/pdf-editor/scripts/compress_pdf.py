#!/usr/bin/env python3
"""
Compress a PDF to reduce file size

Usage:
    compress_pdf.py <input.pdf> <output.pdf>

Arguments:
    input.pdf    Path to the source PDF file
    output.pdf   Path for the compressed output PDF

Note:
    Compression applies stream compression and removes duplicate objects.
    Results vary — PDFs already optimized may see minimal size reduction.
    For aggressive image compression, consider using Ghostscript externally.

Examples:
    compress_pdf.py large_document.pdf compressed.pdf
"""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def compress_pdf(input_path, output_path):
    """
    Compress a PDF by applying stream compression and deduplication.

    Args:
        input_path: Path to source PDF
        output_path: Path for compressed output PDF
    """
    input_size = Path(input_path).stat().st_size

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    # Compress streams and deduplicate objects
    writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)

    with open(output_path, 'wb') as f:
        writer.write(f)

    output_size = Path(output_path).stat().st_size
    reduction = (1 - output_size / input_size) * 100

    print(f"✅ Compression complete")
    print(f"   Input:  {input_size / 1024:.1f} KB")
    print(f"   Output: {output_size / 1024:.1f} KB")
    print(f"   Reduction: {reduction:.1f}%")
    print(f"   Output: {output_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: compress_pdf.py <input.pdf> <output.pdf>")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    if not Path(input_path).exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    compress_pdf(input_path, output_path)


if __name__ == "__main__":
    main()
