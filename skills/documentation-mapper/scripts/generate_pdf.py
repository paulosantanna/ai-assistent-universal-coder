#!/usr/bin/env python3
"""Generate PDF documentation and improvement plan from HTML and Markdown sources."""

import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./output/pdf")
    html_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./output/html")
    base_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("./output")
    docs_dir = output_dir

    docs_dir.mkdir(parents=True, exist_ok=True)

    html_file = html_dir / "documentacao.html"
    pdf_full = docs_dir / "documentacao_completa.pdf"
    pdf_improvements = docs_dir / "plano_de_melhorias.pdf"

    if html_file.exists():
        print(f"Generating full documentation PDF: {pdf_full}")
        generate_pdf_from_html(str(html_file), str(pdf_full))

    improvement_file = base_dir / "improvement" / "plano_de_melhorias.md"
    if improvement_file.exists():
        print(f"Generating improvement plan PDF: {pdf_improvements}")
        improvement_html = convert_md_to_html(improvement_file)
        if improvement_html:
            temp_html = docs_dir / "_improvements_temp.html"
            temp_html.write_text(improvement_html, encoding="utf-8")
            generate_pdf_from_html(str(temp_html), str(pdf_improvements))
            temp_html.unlink()

    print("PDF generation complete.")


def generate_pdf_from_html(html_path: str, pdf_path: str):
    """Convert HTML to PDF using available tools."""
    # Try playwright (most reliable for modern HTML)
    try:
        subprocess.run(
            [
                sys.executable, "-m", "playwright", "install", "chromium"
            ],
            capture_output=True, timeout=120
        )
        script = f"""
import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("file:///{html_path.replace(chr(92), '/')}")
    page.wait_for_load_state("networkidle")
    page.pdf(path=r"{pdf_path}", format="A4", print_background=True)
    browser.close()
"""
        subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, timeout=60
        )
        print(f"  PDF generated via Playwright: {pdf_path}")
        return
    except Exception as e:
        print(f"  Playwright not available ({e}), trying alternatives...")

    # Fallback: try weasyprint
    try:
        import weasyprint
        weasyprint.HTML(filename=html_path).write_pdf(pdf_path)
        print(f"  PDF generated via WeasyPrint: {pdf_path}")
        return
    except ImportError:
        pass

    # Fallback: try pdfkit (wkhtmltopdf wrapper)
    try:
        import pdfkit
        pdfkit.from_file(html_path, pdf_path)
        print(f"  PDF generated via pdfkit: {pdf_path}")
        return
    except Exception:
        pass

    print("  ERROR: No PDF generator available. Install: pip install playwright weasyprint pdfkit")
    print("  Or use: playwright install chromium")


def convert_md_to_html(md_path: Path) -> str | None:
    """Convert Markdown to simple HTML."""
    try:
        import markdown
        md_content = md_path.read_text(encoding="utf-8")
        html_body = markdown.markdown(
            md_content,
            extensions=["extra", "codehilite", "tables"]
        )
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Plano de Melhorias</title>
<style>
body {{ font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }}
h1, h2, h3 {{ color: #1a1a2e; }}
pre {{ background: #f4f4f4; padding: 15px; border-radius: 8px; overflow-x: auto; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
th {{ background: #1a1a2e; color: #fff; }}
</style></head><body>{html_body}</body></html>"""
    except ImportError:
        print("  markdown package not available, using raw text fallback")
        return None


if __name__ == "__main__":
    main()
