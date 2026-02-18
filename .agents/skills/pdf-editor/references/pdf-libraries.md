# PDF Libraries Reference

Load this reference when selecting a library or troubleshooting PDF operations.

## Recommended Library: `pypdf`

**Install:** `pip install pypdf`

`pypdf` is the actively maintained successor to PyPDF2. All bundled scripts use `pypdf`.

### Core Capabilities

| Operation | pypdf Support |
|-----------|--------------|
| Read/write pages | ✅ |
| Rotate pages | ✅ |
| Merge PDFs | ✅ |
| Split/extract pages | ✅ |
| Compress streams | ✅ |
| Read metadata | ✅ |
| Encrypt/decrypt | ✅ |
| Fill form fields | ⚠️ Partial |
| Extract text | ✅ |
| Extract images | ⚠️ Limited |

### Quick API Reference

```python
from pypdf import PdfReader, PdfWriter

# Read
reader = PdfReader("input.pdf")
total_pages = len(reader.pages)
page = reader.pages[0]  # 0-based index

# Write
writer = PdfWriter()
writer.add_page(page)
writer.append("another.pdf")  # merge entire file
with open("output.pdf", "wb") as f:
    writer.write(f)

# Rotate (clockwise)
page.rotate(90)   # or 180, 270

# Compress
page.compress_content_streams()
writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
```

---

## Alternative Libraries

### `pdfplumber` — Best for text/table extraction
```
pip install pdfplumber
```
- Superior text extraction with layout awareness
- Table detection and extraction
- Not suitable for writing/modifying PDFs
- Use when: extracting structured text or tables

### `pikepdf` — Best for advanced editing
```
pip install pikepdf
```
- Built on QPDF (C++ library) — very robust
- Handles encrypted/corrupted PDFs better
- Better image extraction and replacement
- Use when: dealing with complex or encrypted PDFs

### Ghostscript (external CLI) — Best for aggressive compression
```
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```
- `-dPDFSETTINGS` options: `/screen` (72dpi), `/ebook` (150dpi), `/printer` (300dpi), `/prepress` (300dpi+)
- Use when: pypdf compression is insufficient (image-heavy PDFs)
- Requires Ghostscript installed separately

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `PdfReadError: EOF marker not found` | Corrupted PDF | Try pikepdf — more tolerant of corruption |
| Encrypted PDF | Password protected | `reader = PdfReader("file.pdf", password="secret")` |
| Large file after merge | Embedded resources duplicated | Run `compress_pdf.py` after merging |
| Text extraction garbled | Non-standard encoding | Switch to pdfplumber |
| Rotation not visible | Page has both rotate + transform | Use pikepdf for this edge case |
