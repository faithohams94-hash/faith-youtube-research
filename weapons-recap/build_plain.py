"""Build a plain voice-over script (TXT + PDF): narration only, no cues or timestamps."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from script_content import SECTIONS

paras = []
for _, _, _, ps, engage in SECTIONS:
    paras += ps
    if engage:
        paras.append(engage)

open("Weapons_Voiceover_Script.txt", "w").write("\n\n".join(paras) + "\n")

body = ParagraphStyle("b", fontName="Helvetica", fontSize=12, leading=19, spaceAfter=10)
head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=16, leading=20, spaceAfter=14)
story = [Paragraph("Weapons - Voice-Over Script", head)] + [Paragraph(p, body) for p in paras]
SimpleDocTemplate("Weapons_Voiceover_Script.pdf", pagesize=letter, title="Weapons Voice-Over Script",
                  leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch).build(story)
print(len(" ".join(paras).split()), "words")
