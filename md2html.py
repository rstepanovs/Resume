#!/usr/bin/env python3
"""Convert resume Markdown files to styled HTML for browser preview."""

import sys
import markdown
from pathlib import Path

CSS = """
@page {
    size: A4;
    margin: 15mm 20mm;
}

@media print {
    body { margin: 0; }
    .page { box-shadow: none; padding: 15mm 20mm; }
}

* { box-sizing: border-box; }

body {
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.45;
    color: #2c3e50;
    background: #e8ecf1;
    margin: 0;
    padding: 20px 0;
    display: flex;
    justify-content: center;
}

.page {
    background: #fff;
    max-width: 210mm;
    min-height: 297mm;
    padding: 18mm 22mm;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

h1 {
    font-size: 22pt;
    color: #1a1a2e;
    margin: 0 0 4px 0;
    letter-spacing: 0.5px;
    font-weight: 700;
}

h2 {
    font-size: 11.5pt;
    color: #1a5276;
    border-bottom: 2.5px solid #2980b9;
    padding-bottom: 3px;
    margin-top: 16px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
}

h3 {
    font-size: 10.5pt;
    color: #2c3e50;
    margin-top: 10px;
    margin-bottom: 2px;
    font-weight: 600;
}

p {
    margin: 3px 0;
}

a {
    color: #2471a3;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
    color: #1a5276;
}

hr {
    border: none;
    border-top: 1px solid #d5dbdf;
    margin: 10px 0;
}

ul {
    margin: 4px 0;
    padding-left: 18px;
}

li {
    margin-bottom: 2px;
}

li::marker {
    color: #2980b9;
}

strong {
    color: #2c3e50;
    font-weight: 600;
}

em {
    color: #717d7e;
    font-style: italic;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 4px;
}

td {
    vertical-align: top;
    padding: 4px 8px;
}

img {
    border-radius: 6px;
    border: 1px solid #dce1e6;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
"""


def convert(md_path: str) -> str:
    md_text = Path(md_path).read_text(encoding="utf-8")
    html_body = markdown.markdown(md_text, extensions=["tables", "extra"])

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Resume</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">
{html_body}
</div>
</body>
</html>"""

    html_path = str(Path(md_path).with_suffix(".html"))
    Path(html_path).write_text(html_doc, encoding="utf-8")
    return html_path


if __name__ == "__main__":
    files = sys.argv[1:] or [
        "Roman_Stepanov_resume.md",
        "Roman_Stepanov_resume_short.md",
    ]
    for f in files:
        out = convert(f)
        print(f"  {f} -> {out}")
