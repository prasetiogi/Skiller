---
name: pdf-editor
description: This skill guides a complete, efficient PDF editing workflow from receiving a PDF manipulation request, through selecting and running the right bundled script, to delivering the processed output file. This skill must be loaded (NON NEGOTIABLE) whenever user asks to rotate, merge, split, extract, compress a PDF, or any PDF editing task.
metadata:
  version: 1.0.0
  changelog: pdf-editor/CHANGELOG.md
---
# PDF Editor

## Overview

Provides deterministic PDF manipulation through bundled Python scripts powered by `pypdf`. Covers the most common PDF operations: rotating pages, merging files, splitting or extracting pages, and compressing file size.

**Prerequisite:** `pip install pypdf`

## Quick Reference

| Task | Script | Key Arguments |
|------|--------|---------------|
| Rotate pages | `scripts/rotate_pdf.py` | `<input> <output> <angle> [--pages]` |
| Merge files | `scripts/merge_pdf.py` | `<output> <input1> <input2> ...` |
| Split / extract pages | `scripts/split_pdf.py` | `<input> <output_dir> [--pages]` |
| Compress | `scripts/compress_pdf.py` | `<input> <output>` |

Load `references/pdf-libraries.md` for library selection, API reference, and troubleshooting.

---

## Task 1: Rotate Pages

**When to use:** User wants to rotate one or more pages by 90°, 180°, or 270°.

```bash
python scripts/rotate_pdf.py <input.pdf> <output.pdf> <angle> [--pages <range>]
```

- `angle`: `90`, `180`, or `270` (clockwise)
- `--pages`: optional — e.g., `1-3`, `1,3,5`, or `all` (default: all)

**Examples:**
```bash
# Rotate all pages 90° clockwise
python scripts/rotate_pdf.py scan.pdf fixed.pdf 90

# Rotate only pages 1-3 by 180°
python scripts/rotate_pdf.py document.pdf document_fixed.pdf 180 --pages 1-3
```

---

## Task 2: Merge PDFs

**When to use:** User wants to combine multiple PDF files into one, in a specific order.

```bash
python scripts/merge_pdf.py <output.pdf> <input1.pdf> <input2.pdf> [<input3.pdf> ...]
```

- Output path comes **first**, then input files in merge order
- Minimum 2 input files required

**Example:**
```bash
python scripts/merge_pdf.py report.pdf cover.pdf chapter1.pdf chapter2.pdf appendix.pdf
```

> **Tip:** If the merged file is unexpectedly large, run `compress_pdf.py` on the output.

---

## Task 3: Split / Extract Pages

**When to use:** User wants to split a PDF into individual pages, or extract specific pages into separate files.

```bash
python scripts/split_pdf.py <input.pdf> <output_dir> [--pages <range>]
```

- `output_dir`: directory where extracted pages are saved (created if not exists)
- `--pages`: optional — e.g., `2-5`, `1,3,5`, or `all` (default: all)
- Output filenames: `page_001.pdf`, `page_002.pdf`, etc.

**Examples:**
```bash
# Split entire PDF into individual pages
python scripts/split_pdf.py document.pdf ./pages/

# Extract pages 3 through 7
python scripts/split_pdf.py document.pdf ./extracted/ --pages 3-7
```

---

## Task 4: Compress

**When to use:** User wants to reduce PDF file size.

```bash
python scripts/compress_pdf.py <input.pdf> <output.pdf>
```

Applies stream compression and object deduplication. Outputs compression ratio.

**Example:**
```bash
python scripts/compress_pdf.py large_report.pdf compressed_report.pdf
```

> **Note:** Results vary. PDFs dominated by images benefit most from Ghostscript (see `references/pdf-libraries.md`).

---

## References

- **[`references/pdf-libraries.md`](references/pdf-libraries.md)** — Library selection guide, `pypdf` API quick reference, alternative libraries (pdfplumber, pikepdf, Ghostscript), and troubleshooting table
