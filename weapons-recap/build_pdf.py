"""Build the WEAPONS recap script PDF. Run: python3 build_pdf.py"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)
from script_content import TITLE, SUBTITLE, SECTIONS, PRODUCTION_NOTES, TITLE_IDEAS

RED = colors.HexColor("#B3121D")
INK = colors.HexColor("#1A1A1A")
GREY = colors.HexColor("#5A5A5A")
CUE_BG = colors.HexColor("#F1F1F1")
CTA_BG = colors.HexColor("#FFF1E6")

title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=44, leading=50, textColor=RED, alignment=1)
sub = ParagraphStyle("s", fontName="Helvetica", fontSize=14, leading=20, textColor=GREY, alignment=1)
h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=4)
ts = ParagraphStyle("ts", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=RED)
cue = ParagraphStyle("c", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=GREY)
body = ParagraphStyle("b", fontName="Helvetica", fontSize=11.5, leading=17, textColor=INK, spaceAfter=7)
cta = ParagraphStyle("cta", fontName="Helvetica-Bold", fontSize=10.5, leading=15, textColor=INK)
small = ParagraphStyle("sm", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK, spaceAfter=5)


def box(par, bg, border):
    t = Table([[par]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 8.5)
    c.setFillColor(GREY)
    c.drawString(inch, 0.55 * inch, "WEAPONS | Movie Recap Script | Contains full spoilers")
    c.drawRightString(7.5 * inch, 0.55 * inch, f"Page {doc.page}")
    c.restoreState()


story = [Spacer(1, 1.6 * inch), Paragraph(TITLE, title), Spacer(1, 8),
         Paragraph(SUBTITLE, sub), Spacer(1, 6),
         Paragraph("Runtime: 15:00  |  About 2,280 words of narration  |  Full spoilers", sub),
         Spacer(1, 0.5 * inch)]

legend = [
    ["HOW TO READ THIS SCRIPT"],
    ["Red text: the timestamp where each section starts and ends."],
    ["Grey box: what to show on screen (B-roll and visual cues). Do not read it aloud."],
    ["Plain text: the narration. Read every word of it."],
    ["Orange box: an engagement prompt. Read it aloud. It asks viewers to comment, like or subscribe."],
]
lt = Table([[Paragraph(r[0], cta if i == 0 else small)] for i, r in enumerate(legend)], colWidths=[5.5 * inch])
lt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, RED), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
story += [lt, Spacer(1, 0.4 * inch), Paragraph("<b>Title ideas:</b>", small)]
story += [Paragraph(f"&bull; {t}", small) for t in TITLE_IDEAS]
story.append(PageBreak())

for stamp, name, visual, paras, engage in SECTIONS:
    story.append(KeepTogether([Paragraph(stamp, ts), Paragraph(name, h), Spacer(1, 5),
                               box(Paragraph("ON SCREEN: " + visual, cue), CUE_BG, GREY), Spacer(1, 9),
                               Paragraph(paras[0], body)]))
    story += [Paragraph(p, body) for p in paras[1:]]
    if engage:
        story += [Spacer(1, 3), box(Paragraph("ENGAGEMENT PROMPT: " + engage, cta), CTA_BG, RED)]
    story.append(Spacer(1, 16))

story += [PageBreak(), Paragraph("PRODUCTION NOTES (for editing, not narration)", h), Spacer(1, 8)]
story += [Paragraph(f"&bull; {n}", small) for n in PRODUCTION_NOTES]

doc = SimpleDocTemplate("Weapons_Movie_Recap_Script.pdf", pagesize=letter, title="Weapons Movie Recap Script",
                        leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch, bottomMargin=0.9 * inch)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("built")
