"""Finish a pptxgenjs deck: Morph transitions, auto-playing entrance animations, clickable cards.

usage: python3 finish.py raw.pptx out.pptx
- Every slide gets a Morph transition (fade fallback for old PowerPoint).
- Content animates in by itself when a slide opens: cards float up with everything
  inside them, icon circles zoom in, charts/tables/lines wipe in, loose text floats up,
  each group starting a beat after the one before.
- Shapes named "!!..." (morph motif) and title placeholders are left alone so they morph.
- Shapes named "pulse_..." also get a looping pulse after they appear.
- Shapes named "nav_..." become clickable as a whole (copies their text link onto the shape).
"""
import copy, re, sys, zipfile
from lxml import etree

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
P = "{%s}" % NS["p"]
A = "{%s}" % NS["a"]
EMU = 914400

TRANS = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="1600">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice>'
         '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')

STAGGER = 260   # ms between groups starting
DUR = 550       # ms per entrance


class Ids:
    def __init__(self):
        self.n = 2
    def __call__(self):
        self.n += 1
        return self.n


def tgt(spid):
    return '<p:tgtEl><p:spTgt spid="%s"/></p:tgtEl>' % spid


def show(ids, spid):
    return ('<p:set><p:cBhvr><p:cTn id="%d" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>%s'
            '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
            '<p:to><p:strVal val="visible"/></p:to></p:set>') % (ids(), tgt(spid))


def anim(ids, spid, attr, frm, to, dur):
    return ('<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base"><p:cTn id="%d" dur="%d" fill="hold"/>%s'
            '<p:attrNameLst><p:attrName>%s</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>'
            '<p:tav tm="0"><p:val><p:strVal val="%s"/></p:val></p:tav>'
            '<p:tav tm="100000"><p:val><p:strVal val="%s"/></p:val></p:tav></p:tavLst></p:anim>') % (ids(), dur, tgt(spid), attr, frm, to)


def effect(ids, spid, kind, delay, first, dur=DUR):
    """One entrance effect wrapped in its own p:par. kind: float | zoom | wipe | fade"""
    node = "afterEffect" if first else "withEffect"
    preset = {"float": ("42", "0"), "zoom": ("53", "16"), "wipe": ("22", "8"), "fade": ("10", "0")}[kind]
    inner = show(ids, spid)
    if kind == "float":
        inner += ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>' % (ids(), dur, tgt(spid)))
        inner += anim(ids, spid, "ppt_x", "#ppt_x", "#ppt_x", dur)
        inner += anim(ids, spid, "ppt_y", "#ppt_y+.1", "#ppt_y", dur)
    elif kind == "zoom":
        inner += anim(ids, spid, "ppt_w", "0", "#ppt_w", dur)
        inner += anim(ids, spid, "ppt_h", "0", "#ppt_h", dur)
        inner += ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>' % (ids(), dur, tgt(spid)))
    elif kind == "wipe":
        inner += ('<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>' % (ids(), dur, tgt(spid)))
    else:
        inner += ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="%d" dur="%d"/>%s</p:cBhvr></p:animEffect>' % (ids(), dur, tgt(spid)))
    return ('<p:par><p:cTn id="%d" presetID="%s" presetClass="entr" presetSubtype="%s" fill="hold" grpId="0" nodeType="%s">'
            '<p:stCondLst><p:cond delay="%d"/></p:stCondLst><p:childTnLst>%s</p:childTnLst></p:cTn></p:par>') % (
        ids(), preset[0], preset[1], node, delay, inner)


def pulse(ids, spid, delay):
    return ('<p:par><p:cTn id="%d" presetID="26" presetClass="emph" presetSubtype="0" repeatCount="indefinite" fill="hold" grpId="1" nodeType="withEffect">'
            '<p:stCondLst><p:cond delay="%d"/></p:stCondLst><p:childTnLst>'
            '<p:animScale><p:cBhvr><p:cTn id="%d" dur="700" autoRev="1" fill="hold"/>%s</p:cBhvr><p:by x="107000" y="107000"/></p:animScale>'
            '</p:childTnLst></p:cTn></p:par>') % (ids(), delay, ids(), tgt(spid))


def info(el):
    """id, name, bbox (inches), geometry, is title placeholder, has text"""
    cnv = el.find(".//p:cNvPr", NS)
    sid, name = cnv.get("id"), cnv.get("name", "")
    off = el.find(".//a:xfrm/a:off", NS)
    if off is None:
        off = el.find(".//p:xfrm/a:off", NS)
    ext = el.find(".//a:xfrm/a:ext", NS)
    if ext is None:
        ext = el.find(".//p:xfrm/a:ext", NS)
    box = None
    if off is not None and ext is not None:
        x, y = int(off.get("x")) / EMU, int(off.get("y")) / EMU
        box = (x, y, x + int(ext.get("cx")) / EMU, y + int(ext.get("cy")) / EMU)
    geom = el.find(".//a:prstGeom", NS)
    ph = el.find(".//p:nvPr/p:ph", NS)
    is_title = ph is not None and ph.get("type") in ("title", "ctrTitle")
    has_text = el.find(".//p:txBody//a:t", NS) is not None
    return dict(el=el, id=sid, name=name, box=box, geom=geom.get("prst") if geom is not None else None,
                tag=etree.QName(el).localname, title=is_title, text=has_text, ph=ph is not None)


def build_timing(items):
    """items in z-order. returns timing xml or ''"""
    anim_items = [it for it in items if not it["name"].startswith("!!") and not it["title"]
                  and not it["name"].startswith("nav_menu") and it["box"] is not None]
    if not anim_items:
        return ""
    def area(b):
        return (b[2] - b[0]) * (b[3] - b[1])
    cards = [it for it in anim_items if it["geom"] == "roundRect" and area(it["box"]) > 1.2]
    groups, owner = [], {}
    for it in anim_items:
        if it in cards:
            g = {"lead": it, "members": [it]}
            groups.append(g); owner[it["id"]] = g
            continue
        b = it["box"]; cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        host = None
        for c in cards:
            cb = c["box"]
            if cb[0] <= cx <= cb[2] and cb[1] <= cy <= cb[3] and area(cb) > area(b):
                if host is None or area(cb) < area(host["box"]):
                    host = c
        if host is not None and host["id"] in owner:
            owner[host["id"]]["members"].append(it)
        else:
            groups.append({"lead": it, "members": [it]})
    ids = Ids()
    effects, first = [], True
    pulses = []
    for gi, g in enumerate(groups):
        lead = g["lead"]
        if lead in cards:
            kind = "float"
        elif lead["tag"] == "graphicFrame" or lead["geom"] == "line":
            kind = "wipe"
        elif lead["geom"] == "ellipse" or (lead["tag"] == "pic"):
            kind = "zoom"
        else:
            kind = "float"
        delay = gi * STAGGER
        dur = 900 if kind == "wipe" else DUR
        for m in g["members"]:
            k = kind
            if kind == "float" and m is not lead and m["geom"] == "ellipse":
                k = "float"
            effects.append(effect(ids, m["id"], k, delay, first, dur))
            first = False
            if m["name"].startswith("pulse_"):
                pulses.append((m["id"], delay + dur + 200))
    for spid, d in pulses:
        effects.append(pulse(ids, spid, d))
    body = "".join(effects)
    bld = "".join('<p:bldP spid="%s" grpId="0" animBg="1"/>' % m["id"]
                  for g in groups for m in g["members"] if m["tag"] == "sp" and m["text"])
    bld += "".join('<p:bldP spid="%s" grpId="1" animBg="1"/>' % s for s, _ in pulses)
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
            '<p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>%s</p:childTnLst></p:cTn></p:par>'
            '</p:childTnLst></p:cTn></p:par>'
            '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            '</p:childTnLst></p:cTn></p:par></p:tnLst>%s</p:timing>') % (
        ids(), ids(), body, ("<p:bldLst>%s</p:bldLst>" % bld) if bld else "")


def process(xml):
    root = etree.fromstring(xml)
    tree = root.find("p:cSld/p:spTree", NS)
    # pptxgenjs gives the slide-number placeholder a fixed id that can clash with a real shape:
    # give every duplicate-id shape a fresh id before anything targets it
    seen, max_id = set(), max(int(c.get("id")) for c in tree.iter(P + "cNvPr"))
    for cnv in tree.iter(P + "cNvPr"):
        if cnv.get("id") in seen:
            max_id += 1
            cnv.set("id", str(max_id))
        seen.add(cnv.get("id"))
    items = [info(el) for el in tree if etree.QName(el).localname in ("sp", "pic", "graphicFrame", "cxnSp")]
    items = [it for it in items if not (it["ph"] and it["el"].find(".//p:nvPr/p:ph", NS).get("type") in ("sldNum", "ftr", "dt"))]
    # whole-shape click targets for nav_ shapes
    for it in items:
        if it["name"].startswith("nav_"):
            link = it["el"].find(".//p:txBody//a:hlinkClick", NS)
            cnv = it["el"].find(".//p:cNvPr", NS)
            if link is not None and cnv.find("a:hlinkClick", NS) is None:
                cnv.insert(0, copy.deepcopy(link))
            # drop the run-level links so the text isn't underlined; the shape link covers it
            for run_link in it["el"].findall(".//p:txBody//a:hlinkClick", NS):
                run_link.getparent().remove(run_link)
            for rpr in it["el"].findall(".//p:txBody//a:rPr", NS):
                if rpr.get("u") == "sng":
                    del rpr.attrib["u"]
    for old in root.findall("p:timing", NS) + root.findall("p:transition", NS):
        root.remove(old)
    s = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True).decode("utf-8")
    timing = build_timing(items)
    if "</p:clrMapOvr>" in s:
        s = s.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + TRANS + timing, 1)
    else:
        s = s.replace("</p:cSld>", "</p:cSld>" + TRANS + timing, 1)
    return s.encode("utf-8"), timing.count('presetClass="entr"')


src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
total = 0
for item in zin.infolist():
    data = zin.read(item.filename)
    if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
        data, n = process(data)
        total += n
    zout.writestr(item, data)
zout.close()
print("morph + %d entrance effects written to %s" % (total, dst))
