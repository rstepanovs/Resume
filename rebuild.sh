#!/usr/bin/env bash
# Rebuild PDFs and HTMLs from Markdown resume files
set -e
cd "$(dirname "$0")"

echo "=== Generating PDFs ==="
python3 md2pdf.py

echo ""
echo "=== Generating HTMLs ==="
python3 md2html.py

echo ""
echo "Done! Check the output files."
