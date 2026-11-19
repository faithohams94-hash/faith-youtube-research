"""Turn CHK markers in a rendered PDF into real tickable checkboxes.

Usage: python3 tools/add_checkboxes.py RAW.pdf OUT.pdf "PDF Title"
Needs pdftotext (poppler). Three markers per scene become
scene_NN_images / scene_NN_voice / scene_NN_edited fields.
"""
import re
import subprocess
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject, FloatObject,
                           NameObject, NumberObject, StreamObject, TextStringObject)

raw, out, title = sys.argv[1:4]
bbox = subprocess.run(['pdftotext', '-bbox', raw, '-'], capture_output=True, text=True).stdout
pages = re.split(r'<page ', bbox)[1:]
w = PdfWriter(clone_from=PdfReader(raw))
labels = ['images', 'voice', 'edited']


def ap(sz, on):
    s = StreamObject()
    d = "1 1 1 rg 0 0 %.2f %.2f re f 0.64 0.21 0.23 RG 1.2 w 0.6 0.6 %.2f %.2f re S" % (sz, sz, sz - 1.2, sz - 1.2)
    if on:
        d += " 0.64 0.21 0.23 rg 2.4 2.4 %.2f %.2f re f" % (sz - 4.8, sz - 4.8)
    s.set_data(d.encode())
    s.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Form'),
              NameObject('/BBox'): ArrayObject([FloatObject(0), FloatObject(0), FloatObject(sz), FloatObject(sz)])})
    return w._add_object(s)


fields = ArrayObject()
k = 0
for pi, pg in enumerate(pages):
    ph = float(re.search(r'height="([\d.]+)"', pg).group(1))
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>CHK[^<]*</word>', pg):
        x, y = float(m.group(1)), float(m.group(2))
        name = f"scene_{k // 3 + 1:02d}_{labels[k % 3]}"
        k += 1
        sz, top = 11.9, ph - y + 1.2
        f = DictionaryObject({
            NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
            NameObject('/FT'): NameObject('/Btn'), NameObject('/T'): TextStringObject(name),
            NameObject('/TU'): TextStringObject('Tick when done'),
            NameObject('/Rect'): ArrayObject([FloatObject(v) for v in [x - 0.4, top - sz, x - 0.4 + sz, top]]),
            NameObject('/F'): NumberObject(4), NameObject('/V'): NameObject('/Off'), NameObject('/AS'): NameObject('/Off'),
            NameObject('/AP'): DictionaryObject({NameObject('/N'): DictionaryObject({NameObject('/Yes'): ap(sz, True), NameObject('/Off'): ap(sz, False)})}),
            NameObject('/P'): w.pages[pi].indirect_reference})
        ref = w._add_object(f)
        if '/Annots' not in w.pages[pi]:
            w.pages[pi][NameObject('/Annots')] = ArrayObject()
        w.pages[pi]['/Annots'].append(ref)
        fields.append(ref)
w._root_object[NameObject('/AcroForm')] = DictionaryObject({NameObject('/Fields'): fields, NameObject('/NeedAppearances'): BooleanObject(False)})
w.add_metadata({'/Title': title})
w.write(out)
print('checkboxes', k)
