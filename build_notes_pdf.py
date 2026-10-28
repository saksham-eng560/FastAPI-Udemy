"""Build FastAPI_Notes.pdf from notes/fastapi_notes.md.

Usage: python3 build_notes_pdf.py   (requires reportlab)

Supported markdown subset: # chapter, ## section, ### subsection, "- " bullets,
| tables |, ``` code fences, **bold**, `inline code`, plain paragraphs.
"""
import re
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak,
                                Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ROOT = Path(__file__).parent
SRC = ROOT / "notes" / "fastapi_notes.md"
OUT = ROOT / "FastAPI_Notes.pdf"

ACCENT = colors.HexColor("#059669")
base = getSampleStyleSheet()
S = {
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=10.5, leading=15, spaceAfter=6),
    "h1": ParagraphStyle("h1", parent=base["Heading1"], fontSize=20, textColor=ACCENT, spaceBefore=6, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontSize=14, spaceBefore=12, spaceAfter=6),
    "h3": ParagraphStyle("h3", parent=base["Heading3"], fontSize=11.5, spaceBefore=8, spaceAfter=4),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=8.8, leading=11.5,
                           backColor=colors.HexColor("#f3f4f6"), borderPadding=6,
                           spaceBefore=4, spaceAfter=10),
    "cell": ParagraphStyle("cell", parent=base["Normal"], fontSize=9.5, leading=12),
    "title": ParagraphStyle("title", parent=base["Title"], fontSize=32, textColor=ACCENT, alignment=TA_CENTER),
    "sub": ParagraphStyle("sub", parent=base["Normal"], fontSize=13, alignment=TA_CENTER, leading=18),
}


def inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`(.+?)`", r'<font face="Courier" color="#b91c1c">\1</font>', text)


def table(rows):
    data = [[Paragraph(inline(c), S["cell"]) for c in r] for r in rows]
    t = Table(data, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d1fae5")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9ca3af")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [t, Spacer(1, 10)]


def parse(lines):
    """Return (flowables, chapter titles)."""
    story, chapters = [], []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("```"):
            i += 1
            block = []
            while not lines[i].startswith("```"):
                block.append(lines[i].rstrip("\n"))
                i += 1
            story.append(Preformatted("\n".join(block), S["code"]))
        elif line.startswith("# "):
            if chapters:
                story.append(PageBreak())
            chapters.append(line[2:])
            story.append(Paragraph(inline(line[2:]), S["h1"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), S["h2"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), S["h3"]))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            i -= 1
            story.extend(table(rows))
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(ListItem(Paragraph(inline(lines[i][2:].rstrip()), S["body"])))
                i += 1
            i -= 1
            story.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=14))
        elif line.strip():
            story.append(Paragraph(inline(line), S["body"]))
        i += 1
    return story, chapters


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"FastAPI Notes  -  page {doc.page}")
    canvas.restoreState()


def main():
    body, chapters = parse(SRC.read_text().splitlines())
    toc = [Paragraph("Contents", S["h1"])] + [
        Paragraph(inline(c), S["body"]) for c in chapters
    ]
    cover = [
        Spacer(1, 7 * cm),
        Paragraph("FastAPI Notes", S["title"]),
        Spacer(1, 12),
        Paragraph("Personal study notes - FastAPI-Udemy", S["sub"]),
        Paragraph(f"Last updated: {date.today():%d %B %Y}", S["sub"]),
        PageBreak(),
    ]
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, title="FastAPI Notes",
                            author="Saksham", leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    doc.build(cover + toc + [PageBreak()] + body, onLaterPages=footer)
    print(f"Wrote {OUT.name}")


if __name__ == "__main__":
    main()
