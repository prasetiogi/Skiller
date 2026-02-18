#!/usr/bin/env python3
"""
Split PDF into individual pages or extract a page range

Usage:
    split_pdf.py <input.pdf> <output_dir> [--pages <page_range>]

Arguments:
    input.pdf    Path to the source PDF file
    output_dir   Directory where output pages will be saved

Options:
    --pages      Page range to extract (e.g., "1-3", "2,4,6", or "all").
                 Default: all (splits into individual pages)

Output filenames: page_001.pdf, page_002.pdf, etc.
If --pages is a range that results in one file, saves as extracted.pdf.

Examples:
    split_pdf.py document.pdf ./pages/
    split_pdf.py document.pdf ./output/ --pages 2-5
    split_pdf.py document.pdf ./output/ --pages 1,3,5
"""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def parse_page_range(page_range_str, total_pages):
    """Parse page range string into sorted list of 0-based page indices."""
    if page_range_str.lower() == 'all':
        return list(range(total_pages))

    pages = set()
    for part in page_range_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            pages.update(range(int(start) - 1, int(end)))
        else:
            pages.add(int(part) - 1)

    return sorted(p for p in pages if 0 <= p < total_pages)


def split_pdf(input_path, output_dir, page_range='all'):
    """
    Split a PDF into individual pages or extract a specific page range.

    Args:
        input_path: Path to source PDF
        output_dir: Directory for output files
        page_range: Page range string or 'all'
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    pages_to_extract = parse_page_range(page_range, total_pages)

    if not pages_to_extract:
        print("Error: No valid pages found in the specified range")
        sys.exit(1)

    # If extracting multiple pages, save each as a separate file
    for page_num in pages_to_extract:
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])

        output_filename = f"page_{page_num + 1:03d}.pdf"
        output_path = output_dir / output_filename

        with open(output_path, 'wb') as f:
            writer.write(f)

    print(f"✅ Extracted {len(pages_to_extract)}/{total_pages} page(s)")
    print(f"   Output directory: {output_dir}")


def main():
    args = sys.argv[1:]
    page_range = 'all'

    # Parse --pages option
    if '--pages' in args:
        idx = args.index('--pages')
        page_range = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    if len(args) != 2:
        print("Usage: split_pdf.py <input.pdf> <output_dir> [--pages <page_range>]")
        sys.exit(1)

    input_path, output_dir = args
    split_pdf(input_path, output_dir, page_range)


if __name__ == "__main__":
    main()
