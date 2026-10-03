"""Builds the Somber Code channel vision board PDF (with fillable approval/feedback form)."""
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
OUT = HERE / "Somber-Code-Vision-Board-Dr-Mary-Akinlade.pdf"

FONT_DIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Sans", f"{FONT_DIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FONT_DIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", f"{FONT_DIR}/LiberationSans-Italic.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic")

W, H = A4
M = 40  # page margin

BG = HexColor("#0E0E0F")
PANEL = HexColor("#1A1A1C")
PANEL_2 = HexColor("#232326")
LINE = HexColor("#34343A")
TEXT = HexColor("#F2F2F2")
MUTED = HexColor("#A3A3A8")
DIM = HexColor("#6E6E74")
RED = HexColor("#E62117")

CLIENT = "Dr Mary Akinlade"
DATE = "2/10/26"
CHANNEL = "Somber Code"
TAGLINE = "stories that reveal how money shapes real lives"

STORY_BLOCKS = [
    ("Every Level of Wealth",
     "Put the viewer in the same situation at different wealth levels and show how their experience changes.",
     "How Hospitals Treat You at Every Level of Wealth: $0 to $50M"),
    ("The Road to Wealth",
     "Follow someone from struggling → stable → comfortable → wealthy, including the sacrifices and turning points.",
     "POV: You Built $1M While Everyone Thought You Were Broke"),
    ("Wealth Changes You",
     "Explore how someone's behavior, standards, fears and priorities gradually change after becoming wealthy.",
     "POV: You Got Rich — Then You Slowly Stopped Doing These Things"),
    ("People Change Around You",
     "The protagonist stays relatively similar, but friends, family, coworkers or strangers behave differently once money enters the picture.",
     "POV: Your Family Found Out You're a Millionaire"),
    ("One Decision, Two Lives",
     "Take one financial choice and show the radically different lives it can create over 10–30 years.",
     "You Bought the Dream Car. Your Friend Invested the Money. 20 Years Later…"),
    ("The Invisible Cost",
     "Start with something people desperately want — salary, house, business, status — then reveal what was sacrificed to obtain it.",
     "POV: You Finally Made $500K a Year. Nobody Told You the Price."),
    ("Quiet Wealth",
     "Explore the difference between looking wealthy and actually having financial freedom. Great for expectation reversals.",
     "POV: Everyone at the Reunion Thought You Were the Least Successful"),
    ("Money vs. Time",
     "Show how small financial decisions become enormous when you let 10, 20 or 40 years pass.",
     "POV: You Kept Saying “It's Only $300” for 25 Years"),
    ("Money Can't Fix It",
     "Give the protagonist enough money to solve almost anything, then confront them with something money can't restore or control.",
     "You Finally Became Rich Enough to Stop Working. Your Kids Were Already Grown."),
    ("Rise, Fall & Rebuild",
     "Wealth isn't always an upward staircase. Explore what happens when someone gets rich, loses it, and has to discover who they are without it.",
     "POV: You Went From $10M to $10,000 — And Learned Who Actually Knew You"),
]

TOOLS = [
    ("Google Flow", "AI video generation", "Provided by client"),
    ("ChatGPT", "Scripting, ideation & image prompts", "Editor's account — in place"),
    ("Claude AI", "Script writing & story structure", "Already acquired"),
    ("ElevenLabs", "AI voiceover / narration", "Already acquired"),
    ("YouTube Music", "Background music & audio", "Already acquired"),
]


def style(size, color=TEXT, font="Sans", leading=None, align=0):
    return ParagraphStyle("s", fontName=font, fontSize=size, textColor=color,
                          leading=leading or size * 1.32, alignment=align)


def para(c, text, x, y_top, width, st):
    """Draw a paragraph with its top at y_top; return its height."""
    p = Paragraph(text, st)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return h


def background(c, page_no, total):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # soft corner glow, echoing the banner
    for i in range(14):
        r = 240 - i * 15
        c.setFillColor(Color(1, 1, 1, alpha=0.012))
        c.circle(0, 0, r, stroke=0, fill=1)
    # footer
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, 30, W - M, 30)
    c.setFont("Sans", 7.5)
    c.setFillColor(DIM)
    c.drawString(M, 18, f"SOMBER CODE  ·  CHANNEL VISION BOARD  ·  {CLIENT.upper()}")
    c.drawRightString(W - M, 18, f"{page_no:02d} / {total:02d}")


def eyebrow(c, x, y, text):
    c.setFillColor(RED)
    c.rect(x, y - 1, 14, 2.2, stroke=0, fill=1)
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(x + 20, y - 3, " ".join(text.upper()))


def heading(c, x, y, text, size=24):
    c.setFont("Sans-Bold", size)
    c.setFillColor(TEXT)
    c.drawString(x, y, text)


def panel(c, x, y, w, h, fill=PANEL, radius=8, stroke=True):
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, radius, stroke=1 if stroke else 0, fill=1)


def load_image(name):
    path = ASSETS / name
    return ImageReader(Image.open(path).convert("RGBA"))


# ---------------------------------------------------------------- page 1
def page_cover(c, total):
    background(c, 1, total)

    banner = load_image("banner.webp")
    bw = W - 2 * M
    bh = bw * 793 / 1983
    by = H - M - bh
    c.saveState()
    p = c.beginPath()
    p.roundRect(M, by, bw, bh, 10)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(banner, M, by, bw, bh, mask="auto")
    c.restoreState()
    c.setStrokeColor(LINE)
    c.roundRect(M, by, bw, bh, 10, stroke=1, fill=0)
    c.setFont("Sans", 7)
    c.setFillColor(DIM)
    c.drawString(M, by - 11, "CHANNEL BANNER")

    y = by - 46
    eyebrow(c, M, y, "Channel Vision Board")
    c.setFont("Sans-Bold", 34)
    c.setFillColor(TEXT)
    c.drawString(M, y - 40, "somber")
    sw = c.stringWidth("somber ", "Sans-Bold", 34)
    c.setFont("Sans", 34)
    c.drawString(M + sw, y - 40, "code")
    c.setFont("Sans-Italic", 11)
    c.setFillColor(MUTED)
    c.drawString(M, y - 60, TAGLINE)

    # profile picture
    pfp = load_image("profile.webp")
    ps = 104
    px, py = W - M - ps, y - 72
    c.saveState()
    cp = c.beginPath()
    cp.circle(px + ps / 2, py + ps / 2, ps / 2 - 1)
    c.clipPath(cp, stroke=0, fill=0)
    c.drawImage(pfp, px, py, ps, ps, mask="auto")
    c.restoreState()
    c.setFont("Sans", 7)
    c.setFillColor(DIM)
    c.drawCentredString(px + ps / 2, py - 11, "PROFILE PICTURE")

    # detail grid
    details = [
        ("Client", CLIENT),
        ("Date", DATE),
        ("Channel name", CHANNEL),
        ("Channel type", "Finance POV"),
        ("Upload plan", "8 videos / month"),
        ("Mode of content", "AI-generated images & video"),
    ]
    gy = y - 112
    cols, gap = 3, 10
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    ch = 56
    for i, (label, value) in enumerate(details):
        col, row = i % cols, i // cols
        x = M + col * (cw + gap)
        top = gy - row * (ch + gap)
        panel(c, x, top - ch, cw, ch)
        c.setFont("Sans-Bold", 7)
        c.setFillColor(DIM)
        c.drawString(x + 12, top - 18, " ".join(label.upper()))
        para(c, value, x + 12, top - 25, cw - 24, style(11.5, TEXT, "Sans-Bold", 14))

    # goal strip
    gy2 = gy - 2 * (ch + gap) - 6
    gh = 92
    panel(c, M, gy2 - gh, W - 2 * M, gh, fill=PANEL_2)
    c.setFillColor(RED)
    c.roundRect(M, gy2 - gh, 4, gh, 2, stroke=0, fill=1)
    c.setFont("Sans-Bold", 7.5)
    c.setFillColor(RED)
    c.drawString(M + 18, gy2 - 20, "T H E   G O A L")
    c.setFont("Sans-Bold", 19)
    c.setFillColor(TEXT)
    c.drawString(M + 18, gy2 - 44, "Monetized before the new year.")
    para(c,
         "Hard deadline: <b>February 2027 at the latest</b>. Target the YouTube Partner Program "
         "threshold — <b>1,000 subscribers</b> plus <b>4,000 public watch hours</b> in the last 12 months "
         "(or 10M Shorts views in 90 days).",
         M + 18, gy2 - 54, W - 2 * M - 36, style(9.5, MUTED, leading=13))

    # brand identity
    btop = gy2 - gh - 30
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, btop, "B R A N D   I D E N T I T Y")
    btop -= 10
    bh_ = 128
    panel(c, M, btop - bh_, W - 2 * M, bh_)
    swatches = [("#0E0E0F", "Somber Black"), ("#3A3A3D", "Charcoal"), ("#9A9A9E", "Ash Grey"),
                ("#F2F2F2", "Paper White"), ("#E62117", "Subscribe Red")]
    sx = M + 16
    for hexv, name in swatches:
        c.setFillColor(HexColor(hexv))
        c.setStrokeColor(LINE)
        c.roundRect(sx, btop - 62, 40, 40, 6, stroke=1, fill=1)
        c.setFont("Sans-Bold", 7.5)
        c.setFillColor(TEXT)
        c.drawString(sx, btop - 76, name)
        c.setFont("Sans", 7)
        c.setFillColor(DIM)
        c.drawString(sx, btop - 86, hexv)
        sx += 66
    tx_ = M + 16 + 66 * 5 + 6
    para(c, "<b>Look &amp; feel</b><br/>Monochrome, moody and cinematic. A hooded, hand-drawn narrator "
            "character guides every story — calm, observant, a little tired of the world.",
         tx_, btop - 18, W - M - 16 - tx_, style(8.8, MUTED, leading=12))
    para(c, "<b>Voice</b>  Second-person POV (\u201cYou\u2026\u201d), quiet and reflective — the story does the "
            "teaching, never a lecture.  <b>Thumbnails</b>  High contrast black &amp; white, one red accent, "
            "a single bold idea or number.",
         M + 16, btop - 100, W - 2 * M - 32, style(8.8, MUTED, leading=12))


# ---------------------------------------------------------------- page 2
def page_backbone(c, total):
    background(c, 2, total)
    y = H - M - 6
    eyebrow(c, M, y, "Content Backbone")
    heading(c, M, y - 30, "Ten story blocks")
    para(c, "Every upload is built on one of these ten repeatable story engines. Rotate them across the "
            "month so the channel stays consistent but never repetitive.",
         M, y - 40, W - 2 * M, style(9.5, MUTED, leading=13))

    top = y - 74
    avail = top - 44
    gap = 6
    rh = (avail - gap * 9) / 10
    num_w = 34
    name_w = 128
    tx = M + num_w + name_w
    tw = W - M - tx - 12
    for i, (name, what, example) in enumerate(STORY_BLOCKS):
        rt = top - i * (rh + gap)
        panel(c, M, rt - rh, W - 2 * M, rh, radius=6)
        c.setFont("Sans-Bold", 15)
        c.setFillColor(RED)
        c.drawString(M + 12, rt - rh / 2 - 5, f"{i + 1:02d}")
        para(c, name, M + num_w + 4, rt - 12, name_w - 14, style(10.5, TEXT, "Sans-Bold", 13))
        para(c, what, tx, rt - 10, tw, style(8.2, MUTED, leading=10.8))
        c.setFont("Sans-Italic", 8.2)
        c.setFillColor(TEXT)
        ex = f"▶  {example}"
        while c.stringWidth(ex, "Sans-Italic", 8.2) > tw and len(ex) > 10:
            ex = ex[:-2]
        c.drawString(tx, rt - rh + 9, ex)


# ---------------------------------------------------------------- page 3
def page_plan(c, total):
    background(c, 3, total)
    y = H - M - 6
    eyebrow(c, M, y, "Production Plan")
    heading(c, M, y - 30, "Tools & monthly rhythm")

    # tools
    top = y - 52
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, top, "T O O L S   U S E D")
    top -= 10
    rh, gap = 36, 6
    for i, (tool, role, status) in enumerate(TOOLS):
        rt = top - i * (rh + gap)
        panel(c, M, rt - rh, W - 2 * M, rh, radius=6)
        c.setFont("Sans-Bold", 11)
        c.setFillColor(TEXT)
        c.drawString(M + 14, rt - rh / 2 - 4, tool)
        c.setFont("Sans", 9)
        c.setFillColor(MUTED)
        c.drawString(M + 130, rt - rh / 2 - 3.5, role)
        pill_w = c.stringWidth(status, "Sans-Bold", 7.5) + 18
        px = W - M - 12 - pill_w
        c.setFillColor(PANEL_2)
        c.setStrokeColor(LINE)
        c.roundRect(px, rt - rh / 2 - 8, pill_w, 16, 8, stroke=1, fill=1)
        c.setFillColor(RED if "client" in status.lower() else TEXT)
        c.setFont("Sans-Bold", 7.5)
        c.drawString(px + 9, rt - rh / 2 - 2.8, status)

    # monthly rhythm
    top = top - len(TOOLS) * (rh + gap) - 22
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, top, "U P L O A D   P L A N   —   8   V I D E O S   /   M O N T H")
    top -= 10
    cw = (W - 2 * M - 3 * 8) / 4
    chh = 78
    for wk in range(4):
        x = M + wk * (cw + 8)
        panel(c, x, top - chh, cw, chh, radius=6)
        c.setFont("Sans-Bold", 7.5)
        c.setFillColor(DIM)
        c.drawString(x + 12, top - 18, f"W E E K   {wk + 1}")
        for v in range(2):
            vy = top - 38 - v * 20
            c.setFillColor(RED)
            c.circle(x + 16, vy + 3, 3, stroke=0, fill=1)
            c.setFont("Sans", 9.5)
            c.setFillColor(TEXT)
            c.drawString(x + 26, vy, f"Video {wk * 2 + v + 1}")

    # roadmap
    top = top - chh - 26
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, top, "R O A D   T O   M O N E T I Z A T I O N")
    top -= 14
    steps = [
        ("Oct 2026", "Launch & first 8", "Lock style, voice and thumbnails"),
        ("Nov 2026", "16 videos live", "Double down on best-performing blocks"),
        ("Dec 2026", "24 videos live", "Push watch time with longer stories"),
        ("Jan 2027", "32 videos live", "Close the gap to 1K subs / 4K hrs"),
        ("Feb 2027", "Monetized", "Latest deadline — apply to YPP"),
    ]
    sw_ = (W - 2 * M) / len(steps)
    line_y = top - 6
    c.setStrokeColor(LINE)
    c.setLineWidth(1.2)
    c.line(M + 6, line_y, W - M - 6, line_y)
    for i, (when, what, note) in enumerate(steps):
        x = M + i * sw_
        last = i == len(steps) - 1
        c.setFillColor(RED if last else TEXT)
        c.circle(x + 6, line_y, 5 if last else 3.5, stroke=0, fill=1)
        c.setFont("Sans-Bold", 8)
        c.setFillColor(RED if last else MUTED)
        c.drawString(x, line_y - 20, when.upper())
        para(c, what, x, line_y - 26, sw_ - 8, style(10, TEXT, "Sans-Bold", 12))
        para(c, note, x, line_y - 42, sw_ - 10, style(8, MUTED, leading=10.5))

    # per-video workflow
    wtop = line_y - 98
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, wtop, "W O R K F L O W   P E R   V I D E O")
    wtop -= 10
    flow = [("Idea", "Pick a story block"), ("Script", "Claude / ChatGPT"), ("Voice", "ElevenLabs"),
            ("Visuals", "Google Flow"), ("Music", "YouTube Music"), ("Edit", "Cut & thumbnail"),
            ("Review", "Client sign-off")]
    fw = (W - 2 * M - 6 * 6) / len(flow)
    for i, (step, tool) in enumerate(flow):
        x = M + i * (fw + 6)
        panel(c, x, wtop - 52, fw, 52, radius=6, fill=PANEL_2 if i == len(flow) - 1 else PANEL)
        c.setFont("Sans-Bold", 7)
        c.setFillColor(RED)
        c.drawString(x + 8, wtop - 14, f"{i + 1:02d}")
        c.setFont("Sans-Bold", 9.5)
        c.setFillColor(TEXT)
        c.drawString(x + 8, wtop - 29, step)
        c.setFont("Sans", 7)
        c.setFillColor(MUTED)
        c.drawString(x + 8, wtop - 42, tool)

    # collaboration note
    nh = 74
    ny = wtop - 52 - 26 - nh
    panel(c, M, ny, W - 2 * M, nh, fill=PANEL_2)
    c.setFillColor(RED)
    c.roundRect(M, ny, 4, nh, 2, stroke=0, fill=1)
    c.setFont("Sans-Bold", 7.5)
    c.setFillColor(RED)
    c.drawString(M + 18, ny + nh - 18, "N O T E")
    para(c,
         "For the best possible delivery, the client should <b>cooperate and communicate effectively with "
         "the editor</b> — sharing feedback promptly, approving scripts and drafts on time, and keeping "
         "one clear line of communication open throughout production.",
         M + 18, ny + nh - 26, W - 2 * M - 36, style(9.5, TEXT, leading=13))


# ---------------------------------------------------------------- page 4
def page_approval(c, total):
    background(c, 4, total)
    form = c.acroForm
    y = H - M - 6
    eyebrow(c, M, y, "Client Approval & Feedback")
    heading(c, M, y - 30, "Your decision")
    para(c, f"{CLIENT}, please review this vision board, select your decision below and share your thoughts "
            "in the feedback box. This PDF is fillable — click a box to tick it or type directly into the fields.",
         M, y - 40, W - 2 * M, style(9.5, MUTED, leading=13))

    field_kw = dict(borderColor=LINE, fillColor=HexColor("#F4F4F5"), textColor=HexColor("#111111"),
                    borderWidth=1, forceBorder=True)

    # decision options
    top = y - 86
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, top, "D E C I S I O N")
    options = [
        ("approved", "Approved", "Go ahead as planned."),
        ("approved_changes", "Approved with changes", "Proceed after the edits noted below."),
        ("not_approved", "Not approved", "Let's discuss and revise."),
    ]
    ow = (W - 2 * M - 2 * 10) / 3
    oh = 60
    otop = top - 10
    for i, (fid, label, sub) in enumerate(options):
        x = M + i * (ow + 10)
        panel(c, x, otop - oh, ow, oh, radius=6)
        form.checkbox(name=f"decision_{fid}", tooltip=label, x=x + 12, y=otop - 30, size=16,
                      buttonStyle="check", checked=False, **field_kw)
        c.setFont("Sans-Bold", 10)
        c.setFillColor(TEXT)
        c.drawString(x + 36, otop - 26, label)
        c.setFont("Sans", 8)
        c.setFillColor(MUTED)
        c.drawString(x + 12, otop - 48, sub)

    # feedback box
    ftop = otop - oh - 26
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, ftop, "Y O U R   O P I N I O N   &   F E E D B A C K")
    c.setFont("Sans", 8)
    c.setFillColor(DIM)
    c.drawRightString(W - M, ftop, "Anything you love, want changed, or want added")
    fh = 360
    form.textfield(name="client_feedback", tooltip="Your opinion & feedback", x=M, y=ftop - 10 - fh,
                   width=W - 2 * M, height=fh, fontName="Helvetica", fontSize=11,
                   fieldFlags="multiline", value="", **field_kw)

    # priorities
    ptop = ftop - 10 - fh - 24
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, ptop, "S T O R Y   B L O C K S   Y O U   W A N T   F I R S T   ( O P T I O N A L )")
    form.textfield(name="priority_blocks", tooltip="Story blocks to prioritise", x=M, y=ptop - 34,
                   width=W - 2 * M, height=24, fontName="Helvetica", fontSize=10, value="", **field_kw)

    # sign-off
    stop = ptop - 58
    c.setFont("Sans-Bold", 8)
    c.setFillColor(MUTED)
    c.drawString(M, stop, "S I G N - O F F")
    cols = [("Client name", "client_name", CLIENT, 0.42), ("Signature", "client_signature", "", 0.34),
            ("Date", "approval_date", "", 0.24)]
    x = M
    gap = 10
    total_w = W - 2 * M - gap * 2
    for label, fid, val, frac in cols:
        w = total_w * frac
        form.textfield(name=fid, tooltip=label, x=x, y=stop - 38, width=w, height=26,
                       fontName="Helvetica", fontSize=11, value=val, **field_kw)
        c.setFont("Sans", 7.5)
        c.setFillColor(DIM)
        c.drawString(x, stop - 50, label.upper())
        x += w + gap


def build():
    total = 4
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Somber Code — Channel Vision Board")
    c.setAuthor("Somber Code")
    c.setSubject(f"Channel vision board for {CLIENT}")
    for fn in (page_cover, page_backbone, page_plan, page_approval):
        fn(c, total)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
