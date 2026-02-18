#!/usr/bin/env python3
"""
Rotate PDF pages

Usage:
    rotate_pdf.py <input.pdf> <output.pdf> <angle> [--pages <page_range>]

Arguments:
    input.pdf    Path to the source PDF file
    output.pdf   Path for the rotated output PDF
    angle        Rotation angle: 90, 180, or 270 (clockwise)

Options:
    --pages      Page range to rotate (e.g., "1-3,5" or "all"). Default: all

Examples:
    rotate_pdf.py document.pdf rotated.pdf 90
    rotate_pdf.py document.pdf rotated.pdf 180 --pages 1-3
    rotate_pdf.py document.pdf rotated.pdf 270 --pages 1,3,5
"""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def parse_page_range(page_range_str, total_pages):
    """Parse page range string into list of 0-based page indices."""
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


def rotate_pdf(input_path, output_path, angle, page_range='all'):
    """
    Rotate PDF pages by the specified angle.

    Args:
        input_path: Path to source PDF
        output_path: Path for output PDF
        angle: Rotation angle (90, 180, or 270)
        page_range: Page range string or 'all'
    """
    if angle not in (90, 180, 270):
        print(f"Error: Angle must be 90, 180, or 270. Got: {angle}")
        sys.exit(1)

    reader = PdfReader(input_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)

    pages_to_rotate = parse_page_range(page_range, total_pages)

    for i, page in enumerate(reader.pages):
        if i in pages_to_rotate:
            page.rotate(angle)
        writer.add_page(page)

    with open(output_path, 'wb') as f:
        writer.write(f)

    rotated_count = len(pages_to_rotate)
    print(f"✅ Rotated {rotated_count}/{total_pages} page(s) by {angle}°")
    print(f"   Output: {output_path}")


def main():
    args = sys.argv[1:]
    page_range = 'all'

    # Parse --pages option
    if '--pages' in args:
        idx = args.index('--pages')
        page_range = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    if len(args) != 3:
        print("Usage: rotate_pdf.py <input.pdf> <output.pdf> <angle> [--pages <page_range>]")
        sys.exit(1)

    input_path, output_path, angle_str = args

    try:
        angle = int(angle_str)
    except ValueError:
        print(f"Error: Angle must be an integer. Got: {angle_str}")
        sys.exit(1)

    rotate_pdf(input_path, output_path, angle, page_range)


if __name__ == "__main__":
    main()
