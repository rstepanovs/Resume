#!/usr/bin/env python3
"""Convert resume Markdown files to beautifully styled PDFs."""

import sys
import os
import base64
import markdown
from pathlib import Path
from xhtml2pdf import pisa


def image_to_data_uri(match_or_path, base_dir):
    """Convert local image src to data URI for embedding in PDF."""
    img_path = Path(base_dir) / match_or_path
    if img_path.exists():
        data = img_path.read_bytes()
        b64 = base64.b64encode(data).decode()
        return f"data:image/png;base64,{b64}"
    return match_or_path


CSS = """
@page {
    size: A4;
    margin: 15mm 18mm 15mm 18mm;
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 9pt;
    line-height: 1.4;
    color: #2c3e50;
}

h1 {
    font-size: 20pt;
    color: #1a1a2e;
    margin: 0 0 2px 0;
}

h2 {
    font-size: 11pt;
    color: #1a5276;
    border-bottom: 2px solid #2980b9;
    padding-bottom: 2px;
    margin-top: 12px;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

h3 {
    font-size: 10pt;
    color: #2c3e50;
    margin-top: 8px;
    margin-bottom: 1px;
}

p {
    margin: 2px 0;
}

a {
    color: #2471a3;
    text-decoration: none;
}

hr {
    border: none;
    border-top: 1px solid #d5dbdf;
    margin: 8px 0;
}

ul {
    margin: 3px 0;
    padding-left: 16px;
}

li {
    margin-bottom: 1px;
}

strong {
    color: #2c3e50;
}

em {
    color: #717d7e;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 2px;
}

td {
    vertical-align: top;
    padding: 3px 6px;
}

img {
    border-radius: 4px;
}
"""


def convert(md_path: str) -> str:
    base_dir = Path(md_path).parent.resolve()
    md_text = Path(md_path).read_text(encoding="utf-8")

    # Embed images as data URIs
    import re
    def replace_img(match):
        full = match.group(0)
        src_match = re.search(r'src="([^"]+)"', full)
        if src_match:
            src = src_match.group(1)
            if not src.startswith(("http://", "https://", "data:")):
                data_uri = image_to_data_uri(src, base_dir)
                full = full.replace(f'src="{src}"', f'src="{data_uri}"')
        return full

    md_text = re.sub(r'<img[^>]+>', replace_img, md_text)

    html_body = markdown.markdown(md_text, extensions=["tables", "extra"])

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    pdf_path = str(Path(md_path).with_suffix(".pdf"))
    with open(pdf_path, "wb") as out_f:
        status = pisa.CreatePDF(html_doc, dest=out_f, encoding="utf-8")

    if status.err:
        print(f"  ERROR converting {md_path}: {status.err}")
        return ""

    return pdf_path


if __name__ == "__main__":
    files = sys.argv[1:] or [
        "Roman_Stepanov_resume.md",
        "Roman_Stepanov_resume_short.md",
    ]
    for f in files:
        out = convert(f)
        if out:
            size_kb = os.path.getsize(out) / 1024
            print(f"  {f} -> {out} ({size_kb:.0f} KB)")
