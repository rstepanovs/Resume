#!/usr/bin/env bash
# Rebuild PDFs and HTMLs from Markdown resume files
set -e
cd "$(dirname "$0")"

echo "=== Generating PDFs ==="
python md2pdf.py

echo ""
echo "=== Generating HTMLs ==="
python md2html.py

echo ""
echo "Done! Check the output files."
