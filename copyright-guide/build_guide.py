"""Builds copyright-guide/copyright-guide.pdf: an interactive, visual explainer
of the "video copyright dodging" checklist, how Content ID actually works,
and where each tactic stands legally.

Run:  python3 copyright-guide/build_guide.py
"""
import math
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "copyright-guide.pdf")
W, H = letter
M = 40  # page margin

# Palette
BG = HexColor("#FBF8F3")
INK = HexColor("#1E2433")
MUTED = HexColor("#5B6375")
LINE = HexColor("#E3DDD2")
CARD = white
AUDIO = HexColor("#6D4AFF")
AUDIO_L = HexColor("#EEE9FF")
VISUAL = HexColor("#0E9F8E")
VISUAL_L = HexColor("#E2F5F2")
STRAT = HexColor("#F07B1E")
STRAT_L = HexColor("#FDEEDF")
ROBOT = HexColor("#2F6FEB")
ROBOT_L = HexColor("#E5EEFE")
LAW = HexColor("#D23B4F")
LAW_L = HexColor("#FBE6E9")
GOOD = HexColor("#1F9D55")
GOOD_L = HexColor("#E3F4EA")
WARN = HexColor("#D99A00")
WARN_L = HexColor("#FFF4D6")
NIGHT = HexColor("#1B2033")

SECTIONS = [
    ("home", "Start", INK),
    ("robot", "1 The Robot", ROBOT),
    ("law", "2 Robot vs Law", LAW),
    ("audio", "3 Audio", AUDIO),
    ("visual", "4 Visual", VISUAL),
    ("strategy", "5 Strategy", STRAT),
    ("score", "6 Scoreboard", INK),
    ("path", "7 Safe Path", GOOD),
    ("quiz", "Quiz", GOOD),
    ("checklist", "8 Checklist", STRAT),
]


# ---------------------------------------------------------------- helpers
def style(size=10, color=INK, font="Helvetica", leading=None, align=0):
    return ParagraphStyle(
        "s", fontName=font, fontSize=size, textColor=color,
        leading=leading or size * 1.32, alignment=align,
    )


def para(c, text, x, top, w, size=10, color=INK, font="Helvetica", leading=None, align=0):
    """Draw wrapped text with its top edge at `top`; return its height."""
    p = Paragraph(text, style(size, color, font, leading, align))
    _, h = p.wrap(w, 2000)
    p.drawOn(c, x, top - h)
    return h


def rrect(c, x, y, w, h, r=10, fill=CARD, stroke=None, lw=1):
    c.saveState()
    c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1 if stroke is not None else 0)
    c.restoreState()


def pill(c, x, y, text, fill, color=white, size=7.5, pad=6):
    c.saveState()
    c.setFont("Helvetica-Bold", size)
    tw = c.stringWidth(text, "Helvetica-Bold", size)
    c.setFillColor(fill)
    c.roundRect(x, y, tw + pad * 2, size + 7, (size + 7) / 2, fill=1, stroke=0)
    c.setFillColor(color)
    c.drawString(x + pad, y + 4.2, text)
    c.restoreState()
    return tw + pad * 2


def arrow(c, x1, y1, x2, y2, color=INK, lw=2, head=7):
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    c.line(x1, y1, bx, by)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(bx + head * 0.55 * math.sin(ang), by - head * 0.55 * math.cos(ang))
    p.lineTo(bx - head * 0.55 * math.sin(ang), by + head * 0.55 * math.cos(ang))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def circle_num(c, x, y, n, fill, r=11):
    c.saveState()
    c.setFillColor(fill)
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", r)
    c.drawCentredString(x, y - r * 0.36, str(n))
    c.restoreState()


def meter(c, x, y, w, value, color, label):
    """A 5-segment meter, value 0..5."""
    c.saveState()
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(MUTED)
    c.drawString(x, y + 9, label.upper())
    seg = (w - 4 * 3) / 5
    for i in range(5):
        c.setFillColor(color if i < value else LINE)
        c.roundRect(x + i * (seg + 3), y, seg, 6, 3, fill=1, stroke=0)
    c.restoreState()


def page_frame(c, key, title, kicker, accent, pageno):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.bookmarkPage(key)
    # nav tabs
    x = M
    c.setFont("Helvetica-Bold", 6.8)
    for k, label, col in SECTIONS:
        tw = c.stringWidth(label, "Helvetica-Bold", 6.8) + 10
        active = k == key
        c.setFillColor(col if active else HexColor("#EDE8DF"))
        c.roundRect(x, H - 26, tw, 14, 7, fill=1, stroke=0)
        c.setFillColor(white if active else MUTED)
        c.drawString(x + 5, H - 21.5, label)
        c.linkRect("", k, (x, H - 26, x + tw, H - 12), relative=0, thickness=0)
        x += tw + 4
    # title
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M, H - 50, kicker.upper())
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 23)
    c.drawString(M, H - 76, title)
    c.setFillColor(accent)
    c.rect(M, H - 86, 46, 3.5, fill=1, stroke=0)
    # footer
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(M, 30, W - M, 30)
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawString(M, 18, "Copyright & Content ID: a visual guide  |  General education, not legal advice")
    c.drawRightString(W - M, 18, f"Page {pageno}  |  tap the tabs above to jump")


# ---------------------------------------------------------------- mini drawings
def video_frame(c, x, y, w, h, fill=NIGHT):
    c.saveState()
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=0)
    # simple scene: sun + hills + person
    c.setFillColor(HexColor("#F6C35B"))
    c.circle(x + w * 0.78, y + h * 0.72, h * 0.12, fill=1, stroke=0)
    c.setFillColor(HexColor("#3D4A6B"))
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x, y + h * 0.35)
    p.curveTo(x + w * 0.3, y + h * 0.6, x + w * 0.55, y + h * 0.2, x + w, y + h * 0.42)
    p.lineTo(x + w, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(HexColor("#E9E3D8"))
    c.circle(x + w * 0.28, y + h * 0.55, h * 0.08, fill=1, stroke=0)
    c.roundRect(x + w * 0.28 - h * 0.09, y + h * 0.2, h * 0.18, h * 0.27, 3, fill=1, stroke=0)
    c.restoreState()


def wave(c, x, y, w, amp, color, freq=9, lw=1.4, phase=0.0, squeeze=1.0):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    p = c.beginPath()
    n = 80
    for i in range(n + 1):
        t = i / n
        env = math.sin(t * math.pi) ** 0.6
        yy = y + amp * env * math.sin(t * freq * squeeze * math.pi * 2 + phase) * (0.6 + 0.4 * math.sin(t * 23))
        if i == 0:
            p.moveTo(x + t * w, yy)
        else:
            p.lineTo(x + t * w, yy)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


CONSTELLATION = [(0.06, 0.3), (0.14, 0.65), (0.22, 0.45), (0.31, 0.8), (0.38, 0.25),
                 (0.47, 0.55), (0.55, 0.7), (0.63, 0.35), (0.71, 0.6), (0.8, 0.2),
                 (0.87, 0.75), (0.94, 0.48)]


def constellation(c, x, y, w, h, color, dy=0.0, sx=1.0, links=True, grid=True):
    c.saveState()
    if grid:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        for i in range(1, 6):
            c.line(x, y + h * i / 6, x + w, y + h * i / 6)
        for i in range(1, 8):
            c.line(x + w * i / 8, y, x + w * i / 8, y + h)
    pts = [(x + px * w * sx, y + (py + dy) * h) for px, py in CONSTELLATION if px * sx <= 1.0]
    if links:
        c.setStrokeColor(color)
        c.setStrokeAlpha(0.35)
        c.setLineWidth(0.8)
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1])
        c.setStrokeAlpha(1)
    c.setFillColor(color)
    for px, py in pts:
        c.circle(px, py, 2.4, fill=1, stroke=0)
    c.restoreState()


# ---------------------------------------------------------------- pages
def page_cover(c):
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.bookmarkPage("home")
    c.addOutlineEntry("Start here", "home", 0)

    # decorative fingerprint constellation
    c.saveState()
    c.setStrokeColor(HexColor("#2B3350"))
    c.setLineWidth(1)
    for r in range(30, 260, 16):
        c.circle(W - 70, H - 120, r, fill=0, stroke=1)
    c.restoreState()
    constellation(c, W - 250, H - 230, 200, 150, HexColor("#8C7BFF"), grid=False)

    c.setFillColor(HexColor("#F6C35B"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 4, H - 92, "A VISUAL, INTERACTIVE GUIDE FOR YOUTUBE + TIKTOK CREATORS")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 40)
    c.drawString(M, H - 140, "Copyright,")
    c.drawString(M, H - 184, "Content ID")
    c.setFillColor(HexColor("#8C7BFF"))
    c.drawString(M, H - 228, "& Your Checklist")
    para(c, "Every item on your \"copyright dodging\" checklist, explained with pictures: what it does, "
            "<b>why</b> it affects the matching robot, and the part most checklists leave out: "
            "what it does (and doesn't do) for you legally.",
         M, H - 250, 330, 11.5, HexColor("#C9CEDD"))

    # how to use
    rrect(c, M, H - 395, W - 2 * M, 72, 12, HexColor("#252B42"))
    c.setFillColor(HexColor("#F6C35B"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 16, H - 343, "HOW TO USE THIS PDF")
    tips = [("Tap", "any card below or the tabs at the top of every page to jump."),
            ("Tick", "the boxes on the Checklist page; they really check (and save)."),
            ("Type", "your own timestamps and notes into the boxes on page 10.")]
    for i, (a, b) in enumerate(tips):
        xx = M + 16 + i * 178
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(xx, H - 362, a)
        para(c, b, xx, H - 366, 160, 8.5, HexColor("#AEB4C7"))

    # TOC cards
    toc = [
        ("robot", "1", "Meet the Robot", "How Content ID fingerprints your video", ROBOT, 2),
        ("law", "2", "Robot vs. Law", "The most important page in this guide", LAW, 3),
        ("audio", "3", "Audio Tactics", "Pitch, speed, voice-over, music, mute", AUDIO, 4),
        ("visual", "4", "Visual Tactics", "Flip, zoom, picture-in-picture, overlays", VISUAL, 5),
        ("strategy", "5", "Strategy", "Micro-clips, test uploads, re-edits", STRAT, 6),
        ("score", "6", "The Scoreboard", "All 12 tactics compared in one chart", HexColor("#8C7BFF"), 7),
        ("path", "7", "The Safe Path", "Fair use, safe sources, handling claims", GOOD, 8),
        ("checklist", "8", "Your Checklist", "Tickable, fillable, saveable", STRAT, 10),
    ]
    cw, ch = (W - 2 * M - 12) / 2, 64
    for i, (k, n, t, s, col, pg) in enumerate(toc):
        cx = M + (i % 2) * (cw + 12)
        cy = H - 420 - (i // 2 + 1) * (ch + 10)
        rrect(c, cx, cy, cw, ch, 12, HexColor("#252B42"))
        c.setFillColor(col)
        c.roundRect(cx, cy, 8, ch, 4, fill=1, stroke=0)
        circle_num(c, cx + 32, cy + ch / 2, n, col, 13)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 54, cy + ch / 2 + 3, t)
        c.setFillColor(HexColor("#AEB4C7"))
        c.setFont("Helvetica", 8.5)
        c.drawString(cx + 54, cy + ch / 2 - 12, s)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(col)
        c.drawRightString(cx + cw - 14, cy + ch / 2 - 3, f"p.{pg}  >")
        c.linkRect("", k, (cx, cy, cx + cw, cy + ch), relative=0, thickness=0)

    c.setFillColor(HexColor("#7A8197"))
    c.setFont("Helvetica", 7.5)
    c.drawString(M, 24, "General education about how platforms and copyright work. Not legal advice; "
                        "rules differ by country and change over time.")
    c.showPage()


def page_robot(c):
    page_frame(c, "robot", "Meet the Robot: Content ID", "Part 1  |  How the matching works", ROBOT, 2)
    c.addOutlineEntry("1. Meet the Robot (Content ID)", "robot", 0)
    top = H - 100
    para(c, "Before any tactic makes sense, you need to picture what the robot actually does. "
            "YouTube's <b>Content ID</b> (and TikTok's similar system) never \"watches\" your video like a person. "
            "It compares <b>fingerprints</b>. Follow the 4 steps:", M, top, W - 2 * M, 10.5)

    # pipeline
    y0 = H - 270
    bw, bh, gap = 112, 118, 20
    steps = [
        ("Owner uploads", "Record labels, studios and TV networks send YouTube their original files.", HexColor("#7B61FF")),
        ("Reference library", "Each file becomes a fingerprint stored in a giant database.", ROBOT),
        ("You upload", "Your video gets fingerprinted too: its audio and its picture, separately.", STRAT),
        ("Compare", "The robot looks for stretches of your fingerprint that line up with any reference.", LAW),
    ]
    for i, (t, d, col) in enumerate(steps):
        x = M + i * (bw + gap)
        rrect(c, x, y0, bw, bh, 12, CARD, LINE)
        c.setFillColor(col)
        c.roundRect(x, y0 + bh - 26, bw, 26, 12, fill=1, stroke=0)
        c.rect(x, y0 + bh - 26, bw, 12, fill=1, stroke=0)
        circle_num(c, x + 14, y0 + bh - 13, i + 1, HexColor("#00000033", hasAlpha=True), 8)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(x + 27, y0 + bh - 17, t)
        para(c, d, x + 9, y0 + bh - 33, bw - 18, 8.4, MUTED)
        # tiny icon
        if i == 0:
            video_frame(c, x + 30, y0 + 10, 52, 30)
        elif i == 1:
            for r_ in range(3):
                c.setFillColor(ROBOT_L)
                c.setStrokeColor(ROBOT)
                c.ellipse(x + 30, y0 + 10 + r_ * 9, x + 82, y0 + 20 + r_ * 9, fill=1, stroke=1)
        elif i == 2:
            video_frame(c, x + 30, y0 + 10, 52, 30, HexColor("#3A2A1A"))
        else:
            constellation(c, x + 14, y0 + 9, 40, 30, ROBOT, grid=False)
            constellation(c, x + 58, y0 + 9, 40, 30, STRAT, grid=False)
            c.setFillColor(LAW)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x + 56, y0 + 20, "=?")
        if i < 3:
            arrow(c, x + bw + 3, y0 + bh / 2, x + bw + gap - 3, y0 + bh / 2, MUTED, 1.6, 6)

    # outcomes
    y1 = y0 - 30
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y1, "If there is a match, the owner's pre-set rule decides what happens:")
    outs = [("BLOCK", "Your video can't be watched (everywhere or in some countries).", LAW),
            ("MONETIZE", "Ads run, but the money goes to the owner, not you.", WARN),
            ("TRACK", "The owner just watches the view stats.", ROBOT)]
    ow = (W - 2 * M - 20) / 3
    for i, (t, d, col) in enumerate(outs):
        x = M + i * (ow + 10)
        rrect(c, x, y1 - 62, ow, 50, 10, CARD, col, 1.2)
        pill(c, x + 10, y1 - 30, t, col)
        para(c, d, x + 10, y1 - 34, ow - 20, 8.4, INK)

    # fingerprint explainer
    y2 = y1 - 82
    rrect(c, M, y2 - 238, W - 2 * M, 238, 14, CARD, LINE)
    c.setFillColor(ROBOT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M + 18, y2 - 22, "ZOOM IN: WHAT IS A \"FINGERPRINT\"?")
    para(c, "<b>Audio fingerprint.</b> The robot draws your sound as a map: time runs left to right, pitch runs "
            "bottom to top. It keeps only the loudest points (the dots) and remembers the <b>pattern</b> "
            "they make, like a star constellation. It doesn't need the whole song, just a few seconds of matching pattern.",
         M + 18, y2 - 32, 250, 9, INK)
    para(c, "<b>Video fingerprint.</b> Same idea for pictures: it samples frames and records their shapes, "
            "edges and brightness layout.", M + 18, y2 - 128, 250, 9, INK)
    para(c, "<b>Why this matters for your checklist:</b> every audio and visual tactic is an attempt to "
            "<b>move the dots</b> so the pattern no longer lines up. Modern systems are built to "
            "tolerate small changes, so results are unreliable.", M + 18, y2 - 168, 250, 9, ROBOT)

    gx, gy, gw, gh = M + 300, y2 - 205, 210, 150
    c.setFillColor(HexColor("#F7F9FF"))
    c.rect(gx, gy, gw, gh, fill=1, stroke=0)
    constellation(c, gx, gy, gw, gh, ROBOT)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(gx + gw / 2, gy - 12, "TIME  >")
    c.saveState()
    c.translate(gx - 8, gy + gh / 2)
    c.rotate(90)
    c.drawCentredString(0, 0, "PITCH  >")
    c.restoreState()
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(ROBOT)
    c.drawString(gx, gy + gh + 8, "Audio fingerprint = a constellation of loud points")
    c.showPage()


def page_law(c):
    page_frame(c, "law", "Robot vs. Law", "Part 2  |  The most important page", LAW, 3)
    c.addOutlineEntry("2. Robot vs. Law", "law", 0)
    top = H - 100
    # banner
    rrect(c, M, top - 58, W - 2 * M, 58, 14, NIGHT)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 17)
    c.drawCentredString(W / 2, top - 27, "Hiding from the robot  is not  having permission.")
    c.setFillColor(HexColor("#AEB4C7"))
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, top - 45, "There are two separate systems. Your checklist only targets the first one.")

    # two columns
    cy = top - 78
    cw = (W - 2 * M - 16) / 2
    cols = [
        ("THE ROBOT", "Content ID claim", ROBOT, ROBOT_L, [
            "Automatic, triggered by a fingerprint match",
            "Not a strike: no penalty points on your channel",
            "Owner may block, take the ad money, or track",
            "You can dispute it if you believe it's wrong",
            "Editing tricks can sometimes avoid it",
        ]),
        ("THE LAW", "Copyright strike", LAW, LAW_L, [
            "A legal takedown request, often sent by a person",
            "Video is removed and your channel gets a strike",
            "3 active strikes in 90 days = channel deleted",
            "Strikes block live streaming and some features",
            "Editing tricks do nothing here: copying is still copying",
        ]),
    ]
    for i, (k, t, col, light, items) in enumerate(cols):
        x = M + i * (cw + 16)
        rrect(c, x, cy - 200, cw, 200, 14, light)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x + 16, cy - 22, k)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x + 16, cy - 42, t)
        # icon
        if i == 0:
            c.setFillColor(col)
            c.roundRect(x + cw - 50, cy - 46, 32, 26, 6, fill=1, stroke=0)
            c.setFillColor(white)
            c.circle(x + cw - 42, cy - 33, 3.5, fill=1, stroke=0)
            c.circle(x + cw - 26, cy - 33, 3.5, fill=1, stroke=0)
            c.setStrokeColor(col)
            c.setLineWidth(2)
            c.line(x + cw - 34, cy - 20, x + cw - 34, cy - 12)
        else:
            c.setFillColor(col)
            c.rect(x + cw - 48, cy - 46, 28, 6, fill=1, stroke=0)
            c.saveState()
            c.translate(x + cw - 34, cy - 30)
            c.rotate(-35)
            c.roundRect(-14, -5, 28, 10, 2, fill=1, stroke=0)
            c.rect(-2, -16, 4, 12, fill=1, stroke=0)
            c.restoreState()
        yy = cy - 62
        for it in items:
            c.setFillColor(col)
            c.circle(x + 22, yy - 4.5, 3, fill=1, stroke=0)
            h = para(c, it, x + 32, yy, cw - 46, 9, INK)
            yy -= h + 9

    # timeline: the "later" problem
    ty = cy - 228
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, ty, "The \"it passed the check, so I'm safe\" trap")
    para(c, "Passing the automatic check on upload day only means the robot didn't see a match <i>that day</i>. "
            "Owners keep adding references and can search manually, so a claim or strike can arrive weeks or months later.",
         M, ty - 8, W - 2 * M, 9, MUTED)
    lx, ly, lw_ = M + 10, ty - 95, W - 2 * M - 20
    c.setStrokeColor(LINE)
    c.setLineWidth(4)
    c.line(lx, ly, lx + lw_, ly)
    events = [(0.02, "Day 0", "You upload.\nCheck: no issues", GOOD),
              (0.3, "Week 3", "Video grows,\ngets noticed", WARN),
              (0.6, "Week 5", "Owner reviews it\nmanually", STRAT),
              (0.94, "Week 6", "Takedown =\ncopyright strike", LAW)]
    for fx, d, txt, col in events:
        ex = lx + lw_ * fx
        c.setFillColor(col)
        c.circle(ex, ly, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.circle(ex, ly, 3, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(ex, ly + 16, d)
        c.setFillColor(INK)
        c.setFont("Helvetica", 8)
        for j, line in enumerate(txt.split("\n")):
            c.drawCentredString(ex, ly - 22 - j * 10, line)

    # reused content box
    by = ly - 60
    rrect(c, M, by - 104, W - 2 * M, 104, 14, WARN_L)
    c.setFillColor(WARN)
    c.circle(M + 28, by - 30, 13, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(M + 28, by - 36, "$")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M + 52, by - 24, "A third system: the money rules (\"reused content\")")
    para(c, "Even with zero claims, the YouTube Partner Program can refuse or remove monetization if a channel "
            "mostly reuses other people's clips without <b>significant original commentary or value</b>. "
            "Flipping or pitch-shifting doesn't count as original value; your voice, ideas, story and editing do. "
            "For a faceless channel that wants to earn, this rule matters as much as Content ID.",
         M + 52, by - 34, W - 2 * M - 70, 9, INK)
    c.showPage()


def tactic_card(c, x, y, w, h, num, title, accent, light, draw, do, effect, reality, tag, tag_col, value):
    rrect(c, x, y, w, h, 12, CARD, LINE)
    # illustration panel
    rrect(c, x + 8, y + 8, 128, h - 16, 9, light)
    draw(c, x + 8, y + 8, 128, h - 16)
    circle_num(c, x + 22, y + h - 22, num, accent, 10)
    tx = x + 148
    tw = w - 158
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(tx, y + h - 22, title)
    tagw = c.stringWidth(tag, "Helvetica-Bold", 7) + 12
    pill(c, x + w - tagw - 10, y + h - 26, tag, tag_col, size=7)
    yy = y + h - 32
    for lab, txt, col in (("DO", do, accent), ("WHY IT AFFECTS THE ROBOT", effect, INK),
                          ("REALITY CHECK", reality, LAW)):
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(tx, yy - 6, lab)
        hh = para(c, txt, tx, yy - 9, tw - 110 if lab == "DO" else tw, 8.2, INK, leading=10.3)
        yy -= hh + 13
    meter(c, x + w - 110, y + h - 52, 98, value, GOOD, "Adds original value")


# audio drawings
def d_pitch(c, x, y, w, h):
    constellation(c, x + 8, y + 10, w - 16, h - 30, LINE, links=False, grid=False)
    constellation(c, x + 8, y + 10, w - 16, h - 30, AUDIO, dy=0.12, grid=False)
    arrow(c, x + w - 12, y + 18, x + w - 12, y + h - 26, AUDIO, 1.5, 5)
    c.setFillColor(AUDIO)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "dots shift UP  1-3%")


def d_speed(c, x, y, w, h):
    constellation(c, x + 8, y + 12, w - 16, h - 32, LINE, links=False, grid=False)
    constellation(c, x + 8, y + 12, (w - 16), h - 32, AUDIO, sx=0.9, grid=False)
    arrow(c, x + w - 14, y + 8, x + w * 0.62, y + 8, AUDIO, 1.5, 5)
    c.setFillColor(AUDIO)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "dots SQUEEZE together")


def d_voice(c, x, y, w, h):
    wave(c, x + 10, y + h * 0.36, w - 20, 9, HexColor("#B8AEE8"), freq=7)
    wave(c, x + 10, y + h * 0.36, w - 20, 22, AUDIO, freq=4, lw=2, phase=1.3)
    c.setFillColor(AUDIO)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "YOUR voice on top")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawString(x + 10, y + 8, "faint = original clip")


def d_music(c, x, y, w, h):
    wave(c, x + 10, y + h * 0.5, w - 20, 18, AUDIO, freq=6, lw=1.8)
    wave(c, x + 10, y + h * 0.22, w - 20, 5, HexColor("#3BB5A5"), freq=14, lw=1.2)
    c.setFillColor(AUDIO)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "quiet music layer below")


def d_mute(c, x, y, w, h):
    c.setStrokeColor(HexColor("#C9C2E8"))
    c.setLineWidth(2)
    c.line(x + 14, y + h * 0.42, x + w - 14, y + h * 0.42)
    cx, cy = x + w / 2, y + h * 0.42
    c.setFillColor(AUDIO)
    p = c.beginPath()
    p.moveTo(cx - 18, cy - 7)
    p.lineTo(cx - 10, cy - 7)
    p.lineTo(cx, cy - 15)
    p.lineTo(cx, cy + 15)
    p.lineTo(cx - 10, cy + 7)
    p.lineTo(cx - 18, cy + 7)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(LAW)
    c.setLineWidth(2.5)
    c.line(cx + 6, cy - 9, cx + 20, cy + 9)
    c.line(cx + 6, cy + 9, cx + 20, cy - 9)
    c.setFillColor(AUDIO)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "no audio = no audio match")


def page_audio(c):
    page_frame(c, "audio", "Audio Tactics", "Part 3  |  Moving the sound dots", AUDIO, 4)
    c.addOutlineEntry("3. Audio tactics", "audio", 0)
    para(c, "Audio is matched <b>most often</b> because music is the most fingerprinted content on the planet. "
            "The green meter on each card shows how much the tactic adds <b>real originality</b> "
            "(the thing that helps with fair use and monetization).", M, H - 98, W - 2 * M, 9.5, MUTED)
    cards = [
        ("Pitch modification", d_pitch, "Shift the audio pitch up or down by 1% to 3%.",
         "Moves every dot up or down on the pitch map, so the constellation sits in a slightly different place.",
         "Matching systems are designed to handle small shifts, and viewers may hear it sounds \"off\". Legally it's the same copied audio.",
         "FILTER TRICK", WARN, 0),
        ("Speed tweak", d_speed, "Speed the audio up slightly, e.g. to 1.05x.",
         "Squeezes the dots closer together in time, so the spacing between them changes.",
         "Also commonly tolerated by matchers. Same legal status as the original: still the owner's recording.",
         "FILTER TRICK", WARN, 0),
        ("Voice-over / commentary", d_voice, "Talk over the clip: explain, react, critique, teach.",
         "Your louder voice adds new dots and covers some of the original ones, so there's less clean pattern to match.",
         "The only audio tactic that is real transformation, IF you actually comment on the clip. "
         "Commentary and criticism are core fair-use purposes.",
         "REAL VALUE", GOOD, 4),
        ("Background music", d_music, "Layer a low-volume, royalty-free track under the clip.",
         "Adds a second set of dots that muddies the pattern of the original.",
         "Read the music's license: \"royalty-free\" isn't always \"claim-free\". Unlicensed music causes its own claims.",
         "FILTER TRICK", WARN, 1),
        ("Total mute", d_mute, "Delete the clip's original audio completely.",
         "No original audio means there is nothing for the audio matcher to compare. Video can still match.",
         "Simple and very effective at removing the riskiest layer (music). Doesn't make the picture yours.",
         "SAFE MOVE", ROBOT, 1),
    ]
    ch, gap = 114, 7
    for i, (t, d, do, ef, re, tag, tc, v) in enumerate(cards):
        y = H - 140 - (i + 1) * ch - i * gap
        tactic_card(c, M, y, W - 2 * M, ch, i + 1, t, AUDIO, AUDIO_L, d, do, ef, re, tag, tc, v)
    c.showPage()


# visual drawings
def d_flip(c, x, y, w, h):
    fw, fh = 50, 34
    video_frame(c, x + 8, y + h / 2 - 22, fw, fh)
    c.saveState()
    c.translate(x + w - 8, 0)
    c.scale(-1, 1)
    video_frame(c, 0, y + h / 2 - 22, fw, fh, HexColor("#23485A"))
    c.restoreState()
    arrow(c, x + 62, y + h / 2 - 5, x + w - 62, y + h / 2 - 5, VISUAL, 1.4, 5)
    c.setFillColor(VISUAL)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "mirror left <> right")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 14, y + 12, "TEXT")
    c.saveState()
    c.translate(x + w - 14, y + 12)
    c.scale(-1, 1)
    c.setFillColor(LAW)
    c.drawString(0, 0, "TEXT")
    c.restoreState()


def d_zoom(c, x, y, w, h):
    fx, fy, fw, fh = x + 18, y + 14, w - 36, h - 42
    video_frame(c, fx, fy, fw, fh)
    c.saveState()
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFillAlpha(0.55)
    ix, iy = fw * 0.065, fh * 0.065
    c.rect(fx, fy, fw, iy, fill=1, stroke=0)
    c.rect(fx, fy + fh - iy, fw, iy, fill=1, stroke=0)
    c.rect(fx, fy, ix, fh, fill=1, stroke=0)
    c.rect(fx + fw - ix, fy, ix, fh, fill=1, stroke=0)
    c.restoreState()
    c.setStrokeColor(VISUAL)
    c.setDash(3, 2)
    c.setLineWidth(1.4)
    c.rect(fx + ix, fy + iy, fw - 2 * ix, fh - 2 * iy, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(VISUAL)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "scale up 10-15%, edges cut")


def d_pip(c, x, y, w, h):
    fx, fy, fw, fh = x + 12, y + 12, w - 24, h - 40
    c.setFillColor(HexColor("#2E8F83"))
    c.roundRect(fx, fy, fw, fh, 4, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(fx + 8, fy + fh - 14, 40, 5, fill=1, stroke=0)
    c.rect(fx + 8, fy + fh - 24, 28, 4, fill=1, stroke=0)
    video_frame(c, fx + fw * 0.42, fy + 8, fw * 0.52, fh * 0.55)
    c.setFillColor(HexColor("#F6C35B"))
    c.circle(fx + 20, fy + 16, 8, fill=1, stroke=0)
    c.setFillColor(VISUAL)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "clip in a small window")


def d_overlay(c, x, y, w, h):
    fx, fy, fw, fh = x + 18, y + 14, w - 36, h - 42
    video_frame(c, fx, fy, fw, fh)
    c.saveState()
    c.setFillColor(VISUAL)
    c.setFillAlpha(0.35)
    c.rect(fx, fy, fw, fh, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(HexColor("#000000"))
    c.rect(fx, fy, fw, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(fx + 4, fy + 3.5, "WHY THIS MATTERS...")
    c.setFillColor(VISUAL)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2 + 8, y + h - 18, "tint + text on top")


def page_visual(c):
    page_frame(c, "visual", "Visual Tactics", "Part 4  |  Changing what the picture looks like", VISUAL, 5)
    c.addOutlineEntry("4. Visual tactics", "visual", 0)
    para(c, "Video matching samples frames and compares shapes and brightness layout. These tactics change "
            "the frame's geometry or cover parts of it.", M, H - 98, W - 2 * M, 9.5, MUTED)
    cards = [
        ("Horizontal flip", d_flip, "Mirror the frame left-to-right (not if there's text).",
         "Every shape's position is reversed, so the frame layout no longer lines up directly.",
         "Mirrored text and logos look obviously wrong (see the red TEXT). A flipped copy is legally still a copy.",
         "FILTER TRICK", WARN, 0),
        ("Zoom & crop", d_zoom, "Scale the video up 10% to 15% so the edges get cut off.",
         "Changes the framing and removes the edge details the matcher sampled.",
         "Most of the original picture is still there. Little effect on how the law sees it.",
         "FILTER TRICK", WARN, 0),
        ("Picture-in-picture", d_pip, "Shrink the clip into a smaller window over your own background.",
         "The clip becomes a smaller part of a new, different frame.",
         "Genuinely useful when the rest of the frame is YOUR content: notes, arrows, your character, "
         "your analysis. Without that, it's just a smaller copy.",
         "CAN BE REAL", GOOD, 3),
        ("Blurs & overlays", d_overlay, "Place text, filters, watermarks or color tints over the clip.",
         "Changes colors and covers part of the image, adding new shapes to each frame.",
         "Text that explains or critiques adds value; a random tint or watermark doesn't. "
         "Never add your watermark to someone else's footage as if it were yours.",
         "DEPENDS", ROBOT, 2),
    ]
    ch, gap = 140, 10
    for i, (t, d, do, ef, re, tag, tc, v) in enumerate(cards):
        y = H - 130 - (i + 1) * ch - i * gap
        tactic_card(c, M, y, W - 2 * M, ch, i + 6, t, VISUAL, VISUAL_L, d, do, ef, re, tag, tc, v)
    c.showPage()


def page_strategy(c):
    page_frame(c, "strategy", "Strategy Moves", "Part 5  |  Timing, testing, fixing", STRAT, 6)
    c.addOutlineEntry("5. Strategy", "strategy", 0)
    top = H - 100

    # A) micro short
    rrect(c, M, top - 212, W - 2 * M, 212, 14, CARD, LINE)
    circle_num(c, M + 24, top - 24, 10, STRAT)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 42, top - 29, "Keep it micro-short: clips under 5 seconds")
    para(c, "The robot needs a long enough stretch of matching pattern. Short clips broken up by your own "
            "material give it less to work with, and \"using only what you need\" is also one of the fair-use questions.",
         M + 18, top - 44, W - 2 * M - 36, 9, MUTED)
    # timeline comparison
    tx, tw_ = M + 110, W - 2 * M - 130
    rows = [("RISKY", [(0, 1, "one 45-second continuous clip", LAW)]),
            ("BETTER", [(0, 0.08, "", STRAT), (0.08, 0.3, "you explaining", GOOD), (0.3, 0.37, "", STRAT),
                        (0.37, 0.62, "your visuals", GOOD), (0.62, 0.69, "", STRAT), (0.69, 1, "your take", GOOD)])]
    for i, (lab, segs) in enumerate(rows):
        ry = top - 100 - i * 44
        c.setFillColor(LAW if i == 0 else GOOD)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M + 20, ry + 6, lab)
        for a, b, txt, col in segs:
            c.setFillColor(col)
            c.roundRect(tx + tw_ * a + 1, ry, tw_ * (b - a) - 2, 22, 5, fill=1, stroke=0)
            if txt:
                c.setFillColor(white)
                c.setFont("Helvetica-Bold", 7.5)
                c.drawCentredString(tx + tw_ * (a + b) / 2, ry + 8, txt)
    c.setFillColor(STRAT)
    c.roundRect(tx, top - 170, 10, 10, 2, fill=1, stroke=0)
    c.setFillColor(GOOD)
    c.roundRect(tx + 120, top - 170, 10, 10, 2, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(tx + 14, top - 168, "borrowed clip (<5s)")
    c.drawString(tx + 134, top - 168, "your original content")
    para(c, "<b>Reality check:</b> there is no \"safe number of seconds\" in law. A 3-second clip can still be infringing; "
            "a longer one can be fair use. Short helps, but purpose matters more.",
         M + 18, top - 178, W - 2 * M - 36, 8.2, LAW)

    # B + C) test upload loop
    ly = top - 230
    rrect(c, M, ly - 330, W - 2 * M, 330, 14, CARD, LINE)
    circle_num(c, M + 24, ly - 24, 11, STRAT)
    circle_num(c, M + 50, ly - 24, 12, STRAT)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 68, ly - 29, "Test upload + wait & re-edit: the check loop")
    para(c, "YouTube runs a built-in <b>Checks</b> step on upload (copyright + ad-suitability). "
            "Uploading as <b>Private/Unlisted</b> first lets you see results before anyone watches.",
         M + 18, ly - 44, W - 2 * M - 36, 9, MUTED)

    nodes = {
        "edit": (M + 90, ly - 120, "Finish your edit", INK),
        "up": (M + 266, ly - 120, "Upload as PRIVATE", STRAT),
        "wait": (M + 442, ly - 120, "Wait for Checks", ROBOT),
        "clear": (M + 442, ly - 220, "No issues found", GOOD),
        "flag": (M + 266, ly - 220, "Claim found", LAW),
        "fix": (M + 90, ly - 220, "Read the timestamp", WARN),
    }
    nw, nh = 132, 40
    for k, (nx, ny, t, col) in nodes.items():
        rrect(c, nx - nw / 2, ny - nh / 2, nw, nh, 10, col)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawCentredString(nx, ny - 3.5, t)
    arrow(c, M + 156, ly - 120, M + 200, ly - 120, MUTED, 1.6)
    arrow(c, M + 332, ly - 120, M + 376, ly - 120, MUTED, 1.6)
    arrow(c, M + 442, ly - 140, M + 442, ly - 200, GOOD, 1.6)
    arrow(c, M + 400, ly - 140, M + 300, ly - 200, LAW, 1.6)
    arrow(c, M + 200, ly - 220, M + 156, ly - 220, MUTED, 1.6)
    arrow(c, M + 90, ly - 200, M + 90, ly - 140, WARN, 1.6)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(GOOD)
    c.drawString(M + 448, ly - 172, "clear")
    c.setFillColor(LAW)
    c.drawString(M + 328, ly - 165, "match")
    c.setFillColor(WARN)
    c.drawString(M + 96, ly - 172, "fix, then re-upload")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(M + 442, ly - 250, "then publish")
    c.drawCentredString(M + 266, ly - 250, "often within minutes; long videos can take longer")

    para(c, "<b>What a claim on the Checks screen tells you:</b> the exact timestamp and which owner matched. "
            "In YouTube Studio you can usually <b>trim out the segment</b>, <b>mute the song</b>, or "
            "<b>replace the song</b> with a library track, without re-uploading. "
            "<font color='#D23B4F'><b>Remember:</b></font> \"no issues\" only means no automatic match today (see page 3).",
         M + 18, ly - 268, W - 2 * M - 36, 8.8, INK)
    c.showPage()


def page_score(c):
    page_frame(c, "score", "The Scoreboard", "Part 6  |  All 12 tactics side by side", INK, 7)
    c.addOutlineEntry("6. Scoreboard", "score", 0)
    para(c, "Each bar shows how much a tactic adds <b>real originality</b> to your video: the thing that helps "
            "with fair use and with the monetization rules. Colors show the category.",
         M, H - 98, W - 2 * M, 9.5, MUTED)
    data = [
        ("Voice-over / commentary", 4, AUDIO, "Strongest: your ideas about the clip"),
        ("Picture-in-picture (with your content)", 3, VISUAL, "When the frame around it is yours"),
        ("Micro-short clips", 3, STRAT, "Uses only what you need"),
        ("Text overlays that explain", 2, VISUAL, "Adds context, not just a tint"),
        ("Total mute", 1, AUDIO, "Removes risk, adds little"),
        ("Royalty-free background music", 1, AUDIO, "Mood only; check the license"),
        ("Test upload (private)", 1, STRAT, "Information, not originality"),
        ("Wait & re-edit", 1, STRAT, "Fixes what's found"),
        ("Zoom & crop", 0, VISUAL, "Still the same picture"),
        ("Horizontal flip", 0, VISUAL, "Still the same picture"),
        ("Pitch modification", 0, AUDIO, "Still the same recording"),
        ("Speed tweak", 0, AUDIO, "Still the same recording"),
    ]
    lx = M + 175
    bw_ = 210
    top = H - 140
    rh = 30
    # scale
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MUTED)
    for i, lab in enumerate(["none", "", "some", "", "a lot"]):
        if lab:
            c.drawCentredString(lx + bw_ * i / 4, top + 6, lab.upper())
    for i, (name, v, col, note) in enumerate(data):
        y = top - (i + 1) * rh
        if i % 2 == 0:
            c.setFillColor(HexColor("#F3EEE6"))
            c.rect(M, y - 6, W - 2 * M, rh, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(lx - 10, y + 5, name)
        c.setFillColor(LINE)
        c.roundRect(lx, y + 2, bw_, 12, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(lx, y + 2, max(12, bw_ * v / 4), 12, 6, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.8)
        c.drawString(lx + bw_ + 10, y + 5, note)
    ly = top - len(data) * rh - 30
    xx = M
    for lab, col in (("Audio", AUDIO), ("Visual", VISUAL), ("Strategy", STRAT)):
        c.setFillColor(col)
        c.circle(xx + 5, ly + 3, 5, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica", 8.5)
        c.drawString(xx + 14, ly, lab)
        xx += 80

    # takeaway
    ty = ly - 24
    rrect(c, M, ty - 120, W - 2 * M, 120, 14, NIGHT)
    c.setFillColor(HexColor("#F6C35B"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 18, ty - 24, "THE BIG IDEA")
    para(c, "The tactics at the bottom try to make a copy <b>look different to a robot</b>. "
            "The tactics at the top make the video <b>actually different</b> because you added something. "
            "Only the top kind protects you from the law, keeps your channel monetizable, "
            "and makes viewers want to watch <i>you</i>.",
         M + 18, ty - 34, W - 2 * M - 36, 11, white, leading=15)
    c.showPage()


def page_path(c):
    page_frame(c, "path", "The Safe Path", "Part 7  |  What actually protects you", GOOD, 8)
    c.addOutlineEntry("7. The safe path", "path", 0)
    top = H - 100
    para(c, "In the US, using someone's clip without permission can be <b>fair use</b>. A judge weighs four "
            "questions together (no single one decides it). Other countries have similar \"fair dealing\" rules.",
         M, top, W - 2 * M, 9.5, MUTED)
    qs = [
        ("1", "Purpose", "Are you commenting, criticizing, teaching or parodying, or just re-showing it?",
         "Commentary  >  re-upload"),
        ("2", "Nature", "Is the original factual (news, a speech) or highly creative (a movie, a song)?",
         "Facts  >  creative works"),
        ("3", "Amount", "Did you use only what your point needed, or the best/biggest part?",
         "Small, needed  >  the highlight"),
        ("4", "Market", "Could your video replace the original, so people skip buying/watching it?",
         "Adds to it  >  replaces it"),
    ]
    qw = (W - 2 * M - 30) / 4
    for i, (n, t, q, a) in enumerate(qs):
        x = M + i * (qw + 10)
        y = top - 200
        rrect(c, x, y, qw, 160, 12, GOOD_L)
        circle_num(c, x + 20, y + 140, n, GOOD, 11)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 38, y + 136, t)
        para(c, q, x + 12, y + 118, qw - 24, 8.6, INK)
        rrect(c, x + 8, y + 8, qw - 16, 30, 8, CARD)
        para(c, f"<b>{a}</b>", x + 12, y + 30, qw - 24, 7.6, GOOD, align=1)

    # sources
    sy = top - 222
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, sy, "Green-light sources: no dodging needed")
    srcs = [
        ("Your own visuals", "Your AI-generated beat images and animated clips are already original. This is your channel's biggest advantage."),
        ("Platform music libraries", "YouTube Audio Library and TikTok's Commercial Music Library are cleared for use on that platform."),
        ("Licensed stock", "Free or paid stock sites with clear licenses. Save a copy or screenshot of the license."),
        ("Public domain & permission", "Very old works, many government works, or written permission from the owner."),
    ]
    sw = (W - 2 * M - 10) / 2
    for i, (t, d) in enumerate(srcs):
        x = M + (i % 2) * (sw + 10)
        y = sy - 16 - (i // 2 + 1) * 62
        rrect(c, x, y, sw, 56, 10, CARD, LINE)
        c.setFillColor(GOOD)
        c.circle(x + 18, y + 38, 8, fill=1, stroke=0)
        c.setStrokeColor(white)
        c.setLineWidth(2)
        c.line(x + 14, y + 38, x + 17, y + 35)
        c.line(x + 17, y + 35, x + 22, y + 41)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 32, y + 35, t)
        para(c, d, x + 32, y + 30, sw - 42, 7.8, MUTED)

    # claim decision tree
    dy = sy - 170
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, dy, "Got a claim anyway? Follow the arrows")
    nodes = [
        (W / 2, dy - 40, 200, "Claim appears", INK),
        (M + 85, dy - 110, 160, "Content is yours or licensed", GOOD),
        (W / 2, dy - 110, 160, "Clear fair use (real commentary)", ROBOT),
        (W - M - 85, dy - 110, 160, "You just copied it", LAW),
        (M + 85, dy - 175, 160, "Dispute + show license", GOOD),
        (W / 2, dy - 175, 160, "Dispute, explain your use", ROBOT),
        (W - M - 85, dy - 175, 160, "Trim / mute / replace it", LAW),
    ]
    for nx, ny, nw, t, col in nodes:
        rrect(c, nx - nw / 2, ny - 14, nw, 28, 8, col)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(nx, ny - 3, t)
    for (ax, ay, *_), (bx, by, *_) in [(nodes[0], nodes[1]), (nodes[0], nodes[2]), (nodes[0], nodes[3])]:
        arrow(c, ax, ay - 14, bx, by + 14, MUTED, 1.4, 6)
    for a, b in [(1, 4), (2, 5), (3, 6)]:
        arrow(c, nodes[a][0], nodes[a][1] - 14, nodes[b][0], nodes[b][1] + 14, MUTED, 1.4, 6)
    para(c, "<b>Only dispute when you honestly believe you're right.</b> If an owner rejects a dispute and you appeal, "
            "they can respond with a takedown, which is a strike. A wrongful dispute can turn a harmless claim into a strike.",
         M, dy - 200, W - 2 * M, 8.6, LAW)
    c.showPage()


def page_quiz(c):
    page_frame(c, "quiz", "Test Yourself", "Part 7b  |  Do you really get it?", GOOD, 9)
    c.addOutlineEntry("7b. Test yourself", "quiz", 0)
    para(c, "Answer each one in your head, then look at the answer in the green box. Tick the box when you got it right.",
         M, H - 98, W - 2 * M, 9.5, MUTED)
    qa = [
        ("I flipped the clip and pitched the audio 2%. Check said \"no issues\". Is my video now legal?",
         "No. You only avoided an automatic match that day. Legally it's still the owner's footage and audio, and a "
         "manual claim or strike can come later (page 3)."),
        ("Which ONE audio tactic actually strengthens a fair-use argument?",
         "Voice-over commentary, when you're genuinely commenting on, critiquing or teaching about the clip (page 4)."),
        ("What's the difference between a Content ID claim and a copyright strike?",
         "A claim is automatic and isn't a penalty; the owner takes ads, blocks or tracks. A strike comes from a legal "
         "takedown; three active strikes in 90 days deletes the channel."),
        ("My clip is only 4 seconds long. Am I automatically safe?",
         "No. There's no magic length in law. Short helps with the \"amount\" question, but purpose matters most (page 6)."),
        ("Why does the robot find my song even though only a few seconds of it play?",
         "It matches a pattern of loud points (the constellation), and a few seconds of matching pattern is enough (page 2)."),
        ("My channel has no claims but monetization was rejected for \"reused content\". Why?",
         "The money rules need significant original value: your voice, story and editing. Visual tricks don't count."),
    ]
    y = H - 122
    for i, (q, a) in enumerate(qa):
        bh = 94
        rrect(c, M, y - bh, W - 2 * M, bh, 12, CARD, LINE)
        circle_num(c, M + 20, y - 20, i + 1, GOOD, 10)
        para(c, f"<b>{q}</b>", M + 38, y - 12, W - 2 * M - 90, 9.5, INK)
        rrect(c, M + 38, y - bh + 8, W - 2 * M - 90, 44, 8, GOOD_L)
        para(c, a, M + 46, y - bh + 46, W - 2 * M - 106, 8.4, INK)
        c.setFillColor(MUTED)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(W - M - 26, y - 22, "GOT IT")
        c.acroForm.checkbox(name=f"quiz_{i+1}", x=W - M - 36, y=y - 48, size=20, buttonStyle="check",
                            borderColor=GOOD, fillColor=GOOD_L, textColor=GOOD, forceBorder=True)
        y -= bh + 10
    c.showPage()


def page_checklist(c):
    page_frame(c, "checklist", "Your Interactive Checklist", "Part 8  |  Tick it, type in it, save it", STRAT, 10)
    c.addOutlineEntry("8. Interactive checklist", "checklist", 0)
    para(c, "Your original 12 items, now with what each really does. Tick the boxes, type timestamps or notes, "
            "then save the PDF. Tap a page number to jump back to its explanation.",
         M, H - 98, W - 2 * M, 9, MUTED)
    items = [
        ("AUDIO", "Pitch modification (1-3%)", "filter trick", WARN, "audio", AUDIO),
        ("AUDIO", "Speed tweak (~1.05x)", "filter trick", WARN, "audio", AUDIO),
        ("AUDIO", "Voice-over / commentary", "real value", GOOD, "audio", AUDIO),
        ("AUDIO", "Low royalty-free background music", "check license", WARN, "audio", AUDIO),
        ("AUDIO", "Total mute of original audio", "safe move", ROBOT, "audio", AUDIO),
        ("VISUAL", "Horizontal flip (no text)", "filter trick", WARN, "visual", VISUAL),
        ("VISUAL", "Zoom & crop 10-15%", "filter trick", WARN, "visual", VISUAL),
        ("VISUAL", "Picture-in-picture over my content", "can be real", GOOD, "visual", VISUAL),
        ("VISUAL", "Text / filters / overlays", "depends", ROBOT, "visual", VISUAL),
        ("STRATEGY", "Continuous clips under 5 seconds", "helps", GOOD, "strategy", STRAT),
        ("STRATEGY", "Test upload as Private/Unlisted", "info", ROBOT, "strategy", STRAT),
        ("STRATEGY", "Wait for Checks, fix flagged timestamp", "info", ROBOT, "strategy", STRAT),
    ]
    top = H - 142
    rh = 30
    # header
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(MUTED)
    c.drawString(M + 4, top + 4, "DONE")
    c.drawString(M + 40, top + 4, "ITEM")
    c.drawString(M + 300, top + 4, "WHAT IT REALLY IS")
    c.drawString(M + 395, top + 4, "TIMESTAMP / NOTE")
    for i, (cat, name, tag, tc, link, col) in enumerate(items):
        y = top - (i + 1) * rh
        if i % 2 == 0:
            c.setFillColor(HexColor("#F3EEE6"))
            c.rect(M, y - 4, W - 2 * M, rh, fill=1, stroke=0)
        c.setFillColor(col)
        c.rect(M, y - 4, 3, rh, fill=1, stroke=0)
        c.acroForm.checkbox(name=f"item_{i+1}", x=M + 8, y=y + 1, size=17, buttonStyle="check",
                            borderColor=col, fillColor=white, textColor=col, forceBorder=True)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(M + 40, y + 13, cat)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M + 40, y + 2, name)
        pg = {"audio": 4, "visual": 5, "strategy": 6}[link]
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(M + 250, y + 5, f"p.{pg} >")
        c.linkRect("", link, (M + 246, y, M + 285, y + 16), relative=0, thickness=0)
        pill(c, M + 300, y + 2, tag.upper(), tc, size=6.5)
        c.acroForm.textfield(name=f"note_{i+1}", x=M + 395, y=y, width=W - 2 * M - 400, height=18,
                             fontSize=8, borderColor=LINE, fillColor=white, textColor=INK,
                             forceBorder=True, borderWidth=0.8)

    # safety checks
    sy = top - len(items) * rh - 26
    rrect(c, M, sy - 150, W - 2 * M, 150, 14, GOOD_L)
    c.setFillColor(GOOD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 16, sy - 20, "BEFORE YOU HIT PUBLISH: THE CHECKS THAT ACTUALLY PROTECT YOU")
    safe = [
        "Every borrowed clip is there because I'm commenting on it, not as filler",
        "Most of the video is my own voice, visuals and story",
        "I saved the license for every music track and stock clip",
        "Checks show no issues AND I'd be comfortable defending this use",
    ]
    for i, s in enumerate(safe):
        y = sy - 46 - i * 24
        c.acroForm.checkbox(name=f"safe_{i+1}", x=M + 16, y=y - 3, size=16, buttonStyle="check",
                            borderColor=GOOD, fillColor=white, textColor=GOOD, forceBorder=True)
        c.setFillColor(INK)
        c.setFont("Helvetica", 9)
        c.drawString(M + 42, y + 2, s)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(M, 46, "VIDEO TITLE")
    c.acroForm.textfield(name="video_title", x=M + 60, y=40, width=W - 2 * M - 60, height=18, fontSize=9,
                         borderColor=LINE, fillColor=white, textColor=INK, forceBorder=True, borderWidth=0.8)
    c.showPage()


def build():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Copyright, Content ID & Your Checklist")
    c.setAuthor("Faith YouTube Research")
    c.setSubject("A visual, interactive explainer of Content ID and common copyright-avoidance tactics")
    c.showOutline()
    page_cover(c)
    page_robot(c)
    page_law(c)
    page_audio(c)
    page_visual(c)
    page_strategy(c)
    page_score(c)
    page_path(c)
    page_quiz(c)
    page_checklist(c)
    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    build()
