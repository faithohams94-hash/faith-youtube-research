"""Render the course deck to PDF, then add bookmarks, tickable checkboxes and a notes field.

Run from movie-recap-course/:  python3 build/build_pdf.py
"""
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject, FloatObject, NameObject,
                           NumberObject, StreamObject, TextStringObject)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import slides as deck  # noqa: E402

OUT = HERE.parent / "movie-recap-course.pdf"
html_path = HERE / "deck.html"
html_path.write_text(deck.render())

PX = 0.75  # CSS px -> PDF pt
PAGE_H = 720 * PX

fields_path = HERE / "fields.json"
subprocess.run(["node", str(HERE / "render.js"), str(html_path), str(OUT), str(fields_path)], check=True)
fields = json.loads(fields_path.read_text())
fields_path.unlink()

reader = PdfReader(str(OUT))
w = PdfWriter(clone_from=reader)


def stream(writer, content, bbox):
    s = StreamObject()
    s.set_data(content.encode())
    s.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Form"),
              NameObject("/BBox"): ArrayObject([FloatObject(v) for v in bbox])})
    return writer._add_object(s)


acro_fields = ArrayObject()
for f in fields:
    page = w.pages[f["page"]]
    x0, y1 = f["x"] * PX, PAGE_H - f["y"] * PX
    x1, y0 = x0 + f["w"] * PX, y1 - f["h"] * PX
    rect = ArrayObject([FloatObject(v) for v in (x0, y0, x1, y1)])
    bw, bh = x1 - x0, y1 - y0
    field = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Widget"),
        NameObject("/Rect"): rect, NameObject("/F"): NumberObject(4),
        NameObject("/T"): TextStringObject(f["name"]), NameObject("/P"): page.indirect_reference,
    })
    if f["kind"] == "cb":
        on = stream(w, f"q 0.18 0.8 0.44 rg 2 2 {bw - 4:.2f} {bh - 4:.2f} re f "
                       f"1 1 1 RG 2.4 w 1 J 1 j {bw * .25:.2f} {bh * .52:.2f} m {bw * .43:.2f} {bh * .3:.2f} l "
                       f"{bw * .76:.2f} {bh * .72:.2f} l S Q", (0, 0, bw, bh))
        off = stream(w, "", (0, 0, bw, bh))
        field.update({
            NameObject("/FT"): NameObject("/Btn"), NameObject("/V"): NameObject("/Off"),
            NameObject("/AS"): NameObject("/Off"),
            NameObject("/MK"): DictionaryObject({NameObject("/CA"): TextStringObject("4")}),
            NameObject("/AP"): DictionaryObject({NameObject("/N"): DictionaryObject({
                NameObject("/Yes"): on, NameObject("/Off"): off})}),
        })
    else:
        field.update({
            NameObject("/FT"): NameObject("/Tx"), NameObject("/Ff"): NumberObject(4096),  # multiline
            NameObject("/DA"): TextStringObject("/Helv 13 Tf 1 1 1 rg"), NameObject("/V"): TextStringObject(""),
        })
    ref = w._add_object(field)
    page.setdefault(NameObject("/Annots"), ArrayObject()).append(ref)
    acro_fields.append(ref)

helv = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
                         NameObject("/BaseFont"): NameObject("/Helvetica"),
                         NameObject("/Encoding"): NameObject("/WinAnsiEncoding")})
w._root_object[NameObject("/AcroForm")] = DictionaryObject({
    NameObject("/Fields"): acro_fields, NameObject("/NeedAppearances"): BooleanObject(True),
    NameObject("/DA"): TextStringObject("/Helv 13 Tf 1 1 1 rg"),
    NameObject("/DR"): DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/Helv"): w._add_object(helv)})}),
})

# Bookmarks (sidebar outline)
ids = [s[0] for s in deck.slides]
w.add_outline_item("Cover", ids.index("cover"))
w.add_outline_item("Course Roadmap", ids.index("roadmap"))
for i, (mid, title) in enumerate(deck.MODULES):
    parent = w.add_outline_item(f"{i + 1:02d}  {title}", ids.index(mid))
    for j, s in enumerate(deck.slides):
        if s[1] == i and s[0] != mid:
            w.add_outline_item(f"Page {j + 1}", j, parent=parent)
w.add_outline_item("Your Action Plan", ids.index("close"))
w.page_mode = "/UseOutlines"
w.add_metadata({"/Title": "Movie Recap Course", "/Subject": "Start a profitable YouTube movie recap channel"})

with open(OUT, "wb") as fh:
    w.write(fh)
html_path.unlink()
print(f"wrote {OUT} ({len(w.pages)} pages, {len(fields)} form fields)")
