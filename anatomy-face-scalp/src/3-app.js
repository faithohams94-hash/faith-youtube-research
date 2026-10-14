document.documentElement.classList.add("js");
// remove the no-JavaScript fallback (still picture, notes, banner) once scripts run
["#nojs", "#static-plate", "#static-notes"].forEach(sel => { const e = document.querySelector(sel); if (e) e.remove(); });
// ================= utilities =================
const NS = "http://www.w3.org/2000/svg";
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
function sv(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) {
    if (k === "style") Object.assign(e.style, attrs.style);
    else if (k === "text") e.textContent = attrs.text;
    else e.setAttribute(k, attrs[k]);
  }
  if (parent) parent.appendChild(e);
  return e;
}
function h(tag, attrs = {}, html) {
  const e = document.createElement(tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (html != null) e.innerHTML = html;
  return e;
}
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const store = {
  get(k, d) { try { const v = localStorage.getItem("fst:" + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem("fst:" + k, JSON.stringify(v)); } catch (e) {} }
};
const reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

// mirror an absolute path (M L C A Z) across x = 300
function mirrorPath(d, W = 600) {
  const toks = d.match(/[MLCAZ]|-?\d*\.?\d+/g);
  const out = []; let cmd = null, args = [];
  const counts = { M: 2, L: 2, C: 6, A: 7, Z: 0 };
  const flush = () => {
    if (!cmd || !args.length) return;
    if (cmd === "A") { args[4] = 1 - +args[4]; args[5] = W - args[5]; }
    else if (cmd !== "Z") for (let i = 0; i < args.length; i += 2) args[i] = W - args[i];
    out.push(cmd + args.join(" "));
  };
  for (const t of toks) {
    if (/[MLCAZ]/.test(t)) { flush(); cmd = t; args = []; if (t === "Z") { out.push("Z"); cmd = null; } }
    else { args.push(+t); if (args.length === counts[cmd]) { flush(); args = []; } }
  }
  return out.join(" ");
}

const SYS = {
  artery: { label: "Artery", col: "var(--artery)", dk: "var(--artery-dk)" },
  vein: { label: "Vein", col: "var(--vein)", dk: "var(--vein-dk)" },
  nerve: { label: "Nerve", col: "var(--nerve)", dk: "var(--nerve-dk)" },
  muscle: { label: "Muscle of facial expression", col: "var(--muscle)", dk: "var(--muscle-dk)" },
  ref: { label: "Landmark muscle / gland", col: "var(--gland)", dk: "var(--bone-dk)" },
  bone: { label: "Bone / foramen", col: "var(--bone)", dk: "var(--bone-dk)" },
  derm: { label: "Sensory territory", col: "var(--accent)", dk: "var(--accent)" }
};
const FIELD = {
  o: "Origin", c: "Course", r: "Relations", b: "Branches", e: "Termination", s: "Supplies",
  p: "Palpate / surface marking", i: "Insertion", a: "Action", n: "Nerve supply", t: "Test it at the bedside", k: "Clinical"
};
function fieldLabel(key, sys) {
  if (sys === "vein") return { b: "Tributaries / connections", s: "Drains", e: "Ends in", o: "Formed by" }[key] || FIELD[key];
  if (sys === "nerve") return { s: "Innervates / skin supplied", o: "Arises from" }[key] || FIELD[key];
  if (sys === "derm") return { b: "Nerves" }[key] || FIELD[key];
  return FIELD[key];
}

// ================= head drawings (skin layer) =================
const LAT_HEAD = "M330 58 C 230 55, 160 100, 145 170 C 138 205, 130 235, 122 255 C 118 262, 120 268, 118 272 C 110 300, 90 325, 70 345 C 64 352, 68 362, 80 365 C 90 368, 100 372, 104 378 C 100 390, 98 398, 100 405 C 104 412, 110 415, 108 420 C 104 428, 100 436, 104 444 C 110 452, 116 458, 114 466 C 110 480, 116 500, 132 512 C 150 524, 180 520, 205 515 C 235 510, 250 520, 255 540 C 262 580, 262 640, 258 720 L 478 720 C 470 640, 468 580, 476 520 C 486 470, 520 430, 535 370 C 552 300, 545 220, 505 150 C 470 90, 410 58, 330 58 Z";
const LAT_EAR = "M386 274 C 412 262, 440 282, 438 322 C 436 356, 422 376, 412 396 C 405 410, 391 411, 386 399 C 382 386, 383 370, 380 360 C 372 345, 375 300, 386 274 Z";
const LAT_HAIR = "M150 172 C 166 110, 240 60, 330 58 C 410 58, 470 90, 505 150 C 545 220, 552 300, 535 370 C 526 400, 512 420, 500 440 L 472 420 C 482 360, 470 300, 442 272 L 410 262 C 392 242, 372 232, 352 228 L 334 232 C 302 202, 262 184, 222 176 C 196 172, 172 170, 150 172 Z";
const ANT_HALF = "M301 62 C 225 62, 170 110, 163 200 C 160 240, 158 280, 162 320 C 166 380, 185 440, 215 480 C 225 495, 232 505, 234 520 C 236 580, 232 650, 222 720 L 301 720 Z";
const ANT_EAR = "M165 298 C 150 292, 140 308, 142 334 C 144 360, 150 380, 163 386 Z";
const ANT_HAIR = "M301 62 C 225 62, 170 110, 163 200 L 171 206 C 186 150, 232 120, 301 118 Z";

function drawSkin(g, view) {
  if (view === "lat") {
    sv("path", { d: LAT_HEAD, fill: "url(#skinGrad)" }, g);
    sv("path", { d: LAT_HAIR, style: { fill: "var(--hair)", opacity: .82 } }, g);
    sv("path", { d: LAT_EAR, fill: "url(#skinGrad)", style: { stroke: "var(--skin-dk)", strokeWidth: 1.2 } }, g);
    sv("path", { d: "M394 300 C 412 294, 422 316, 414 340 C 407 356, 393 352, 389 340 C 386 326, 388 308, 394 300 Z", style: { fill: "var(--skin-dk)", opacity: .55 } }, g);
    sv("ellipse", { cx: 392, cy: 336, rx: 5, ry: 6, style: { fill: "var(--hair)", opacity: .6 } }, g);
    sv("path", { d: "M168 280 C 178 272, 195 274, 206 282 C 195 290, 178 290, 168 284 Z", style: { fill: "#F4EEE8", stroke: "var(--skin-dk)", strokeWidth: 1 } }, g);
    sv("ellipse", { cx: 176, cy: 281, rx: 4.5, ry: 6, style: { fill: "#3B2A20" } }, g);
    sv("path", { d: "M150 256 C 175 244, 205 247, 226 258", style: { fill: "none", stroke: "var(--hair)", strokeWidth: 5, strokeLinecap: "round", opacity: .8 } }, g);
    sv("path", { d: "M100 405 C 112 400, 128 410, 140 420 C 126 418, 113 416, 107 420 Z", style: { fill: "#B5615A", opacity: .85 } }, g);
    sv("path", { d: "M107 420 C 113 424, 126 424, 140 420 C 128 432, 113 440, 103 440 Z", style: { fill: "#C0706A", opacity: .85 } }, g);
    sv("path", { d: "M94 360 C 100 355, 110 355, 113 362 C 108 367, 100 367, 94 360 Z", style: { fill: "var(--skin-dk)" } }, g);
    sv("path", { d: "M113 338 C 124 347, 126 362, 113 369", style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.5 } }, g);
    sv("path", { d: "M118 372 C 128 385, 135 400, 140 418", style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.2, opacity: .7 } }, g);
  } else {
    for (const flip of [false, true]) {
      const m = d => flip ? mirrorPath(d) : d;
      sv("path", { d: m(ANT_HALF), fill: "url(#skinGradA)" }, g);
      sv("path", { d: m(ANT_HAIR), style: { fill: "var(--hair)", opacity: .82 } }, g);
      sv("path", { d: m(ANT_EAR), fill: "url(#skinGradA)", style: { stroke: "var(--skin-dk)", strokeWidth: 1.2 } }, g);
      sv("path", { d: m("M215 291 C 230 276, 260 276, 276 292 C 260 303, 230 303, 215 291 Z"), style: { fill: "#F4EEE8", stroke: "var(--skin-dk)", strokeWidth: 1 } }, g);
      sv("circle", { cx: flip ? 355 : 245, cy: 290, r: 9, style: { fill: "#4A3326" } }, g);
      sv("circle", { cx: flip ? 355 : 245, cy: 290, r: 4, style: { fill: "#140C08" } }, g);
      sv("path", { d: m("M206 262 C 228 249, 264 251, 287 261"), style: { fill: "none", stroke: "var(--hair)", strokeWidth: 6, strokeLinecap: "round", opacity: .8 } }, g);
      sv("path", { d: m("M290 292 C 288 330, 283 360, 275 380"), style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.3, opacity: .7 } }, g);
      sv("path", { d: m("M272 372 C 260 380, 264 396, 282 397 C 290 398, 296 398, 301 397"), style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.6 } }, g);
      sv("path", { d: m("M252 446 C 268 434, 286 430, 301 436 L 301 447 C 285 446, 268 446, 252 446 Z"), style: { fill: "#B5615A", opacity: .85 } }, g);
      sv("path", { d: m("M252 446 C 268 448, 285 448, 301 447 L 301 463 C 282 463, 265 457, 252 446 Z"), style: { fill: "#C0706A", opacity: .85 } }, g);
      sv("path", { d: m("M268 392 C 258 410, 252 425, 250 440"), style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.2, opacity: .6 } }, g);
    }
  }
}

// ================= stage construction =================
const state = { view: "lat", sel: null, hide: new Set(["derm"]), labels: false, skin: 30, trace: null, quiz: null };
const stages = {};

function buildDefs(svg, view) {
  const defs = sv("defs", {}, svg);
  const rg = (id, cx, cy, stops) => {
    const g = sv("radialGradient", { id, cx, cy, r: "75%" }, defs);
    stops.forEach(([o, c, op]) => sv("stop", { offset: o, style: { stopColor: c, stopOpacity: op ?? 1 } }, g));
  };
  rg("skinGrad", "35%", "40%", [["0%", "var(--skin)"], ["70%", "var(--skin)"], ["100%", "var(--skin-dk)"]]);
  rg("skinGradA", "50%", "40%", [["0%", "var(--skin)"], ["65%", "var(--skin)"], ["100%", "var(--skin-dk)"]]);
  rg("fasciaGrad", "40%", "40%", [["0%", "var(--fascia)"], ["100%", "var(--skin-dk)"]]);
  rg("shade", "35%", "30%", [["0%", "#FFFFFF", .32], ["60%", "#FFFFFF", 0], ["100%", "#000000", .28]]);
  const f = sv("filter", { id: "glow", x: "-50%", y: "-50%", width: "200%", height: "200%" }, defs);
  sv("feGaussianBlur", { stdDeviation: 2.5, result: "b" }, f);
  const mg = sv("feMerge", {}, f);
  sv("feMergeNode", { in: "b" }, mg); sv("feMergeNode", { in: "SourceGraphic" }, mg);
  // gland lobules
  const p = sv("pattern", { id: "lobule-" + view, width: 9, height: 9, patternUnits: "userSpaceOnUse" }, defs);
  sv("rect", { width: 9, height: 9, style: { fill: "var(--gland)" } }, p);
  sv("circle", { cx: 4.5, cy: 4.5, r: 3.4, style: { fill: "none", stroke: "var(--bone-dk)", strokeWidth: .6, opacity: .55 } }, p);
  // bone texture
  const bp = sv("pattern", { id: "bonetex-" + view, width: 14, height: 14, patternUnits: "userSpaceOnUse" }, defs);
  sv("rect", { width: 14, height: 14, style: { fill: "var(--bone)" } }, bp);
  sv("circle", { cx: 3, cy: 4, r: .8, style: { fill: "var(--bone-dk)", opacity: .35 } }, bp);
  sv("circle", { cx: 10, cy: 11, r: .6, style: { fill: "var(--bone-dk)", opacity: .3 } }, bp);
  const cp = sv("clipPath", { id: "headclip-" + view }, defs);
  if (view === "lat") sv("path", { d: LAT_HEAD }, cp);
  else { sv("path", { d: ANT_HALF }, cp); sv("path", { d: mirrorPath(ANT_HALF) }, cp); }
  return defs;
}

function fiberPattern(defs, view, id, ang, sys) {
  const pid = `fib-${view}-${id}`;
  const p = sv("pattern", { id: pid, width: 5, height: 5, patternUnits: "userSpaceOnUse", patternTransform: `rotate(${ang || 0})` }, defs);
  sv("rect", { width: 5, height: 5, style: { fill: sys === "ref" ? "var(--muscle)" : "var(--muscle)", opacity: sys === "ref" ? .55 : 1 } }, p);
  sv("rect", { y: 0, width: 5, height: 1.3, style: { fill: "var(--muscle-dk)", opacity: .55 } }, p);
  sv("rect", { y: 2.8, width: 5, height: .7, style: { fill: "#FFFFFF", opacity: .16 } }, p);
  return pid;
}

function buildStage(view) {
  const svg = sv("svg", { viewBox: "0 0 600 720", role: "img", "aria-label": view === "lat" ? "Lateral view of head and neck" : "Anterior view of face" });
  const defs = buildDefs(svg, view);
  const L = {};
  ["base", "bone", "refdeep", "musdeep", "ref", "mus", "skin", "vein", "artery", "nerve", "derm", "pts", "labels", "trace"].forEach(k => L[k] = sv("g", { "data-layer": k }, svg));
  // base tissue
  if (view === "lat") sv("path", { d: LAT_HEAD, fill: "url(#fasciaGrad)" }, L.base);
  else { sv("path", { d: ANT_HALF, fill: "url(#fasciaGrad)" }, L.base); sv("path", { d: mirrorPath(ANT_HALF), fill: "url(#fasciaGrad)" }, L.base); }
  // skin
  drawSkin(L.skin, view);
  L.skin.style.opacity = state.skin / 100;
  L.skin.style.pointerEvents = "none";
  L.derm.setAttribute("clip-path", `url(#headclip-${view})`);

  for (const id in S) {
    const o = S[id];
    const paths = o[view];
    if (!paths) continue;
    const both = view === "ant" && !o.mid && o.sys !== "derm" ? [false, true] : [false];
    if (view === "ant" && o.sys === "derm") both.push(true);
    for (const flip of both) {
      const list = paths.map(d => flip ? (d[0] === "~" ? "~" + mirrorPath(d.slice(1)) : mirrorPath(d)) : d);
      drawStructure(id, o, list, view, L, defs);
    }
  }
  // head outline always visible
  const outline = view === "lat" ? [LAT_HEAD] : [ANT_HALF, mirrorPath(ANT_HALF)];
  outline.forEach(d => sv("path", { d, style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.4, opacity: .8, pointerEvents: "none" } }, L.skin.parentNode.insertBefore(sv("g"), L.vein)));
  // trace overlay
  stages[view] = { svg, L, defs, vb: { x: 0, y: 0, w: 600, h: 720 } };
  return svg;
}

function drawStructure(id, o, list, view, L, defs) {
  const sys = o.sys;
  let layer;
  if (sys === "muscle") layer = o.deep ? L.musdeep : L.mus;
  else if (sys === "ref") layer = o.deep ? L.refdeep : L.ref;
  else if (sys === "bone") layer = o.pt ? L.pts : L.bone;
  else layer = L[sys];
  const g = sv("g", { class: "s", "data-id": id, "data-sys": sys, tabindex: "-1" }, layer);
  const w = o.wd || 2.4;
  g.style.setProperty("--w", w);
  g.style.setProperty("--wsel", (w * 1.7) + "px");
  if (sys === "artery" || sys === "vein" || sys === "nerve" || (sys === "ref" && o.line)) {
    const col = sys === "ref" ? "var(--gland)" : SYS[sys].col, dk = sys === "ref" ? "var(--bone-dk)" : SYS[sys].dk;
    for (const raw of list) {
      const deep = raw[0] === "~", d = deep ? raw.slice(1) : raw;
      const isClosed = /Z\s*$/.test(d);
      const sub = sv("g", { class: deep ? "deepseg" : "" }, g);
      sv("path", { d, class: "hit", style: { strokeWidth: 14, fill: isClosed ? "transparent" : "none" } }, sub);
      const dash = deep ? (sys === "nerve" ? "5 4" : "7 4") : null;
      sv("path", { d, class: "case", style: { fill: isClosed ? (sys === "vein" ? "var(--vein)" : "none") : "none", fillOpacity: isClosed ? .25 : 0, stroke: dk, strokeWidth: w + 2.2, strokeLinecap: "round", strokeLinejoin: "round", strokeDasharray: dash, opacity: deep ? .7 : 1 } }, sub);
      sv("path", { d, class: "core", style: { fill: "none", stroke: col, strokeWidth: w, strokeLinecap: "round", strokeLinejoin: "round", strokeDasharray: dash } }, sub);
      if (!deep) sv("path", { d, style: { fill: "none", stroke: "#FFFFFF", strokeOpacity: .35, strokeWidth: Math.max(.6, w * .28), strokeLinecap: "round", pointerEvents: "none" } }, sub);
    }
    if (list.some(r => r[0] === "~") && list.every(r => r[0] === "~")) g.classList.add("deep");
  } else if (sys === "muscle" || sys === "ref") {
    g.classList.add("musc");
    let fill;
    if (id === "parotid" || id === "submand_gland") fill = `url(#lobule-${view})`;
    else if (o.flat) fill = null;
    else fill = `url(#${fiberPattern(defs, view, id, o.ang, sys)})`;
    for (const d of list) {
      const p = sv("path", { d, class: "fill core", "fill-rule": "evenodd", style: { stroke: sys === "ref" && !fill?.includes("lobule") ? "var(--muscle-dk)" : "var(--muscle-dk)", strokeWidth: .8, strokeOpacity: .7 } }, g);
      if (fill) p.setAttribute("fill", fill);
      else Object.assign(p.style, { fill: id === "galea" ? "var(--bone)" : "var(--muscle)", fillOpacity: id === "galea" ? .55 : .35 });
      if (id === "parotid" || id === "submand_gland") Object.assign(p.style, { stroke: "var(--bone-dk)", strokeWidth: 1 });
      if (sys === "ref" && id !== "parotid" && id !== "submand_gland") p.style.opacity = .78;
      sv("path", { d, "fill-rule": "evenodd", fill: "url(#shade)", style: { pointerEvents: "none" } }, g);
    }
    if (o.deep) g.classList.add("deep");
  } else if (sys === "bone") {
    for (const d of list) {
      if (o.pt) {
        sv("path", { d, class: "core", style: { fill: "var(--ink)", stroke: "var(--bone)", strokeWidth: 2 } }, g);
        sv("path", { d, class: "hit", style: { strokeWidth: 12, fill: "transparent" } }, g);
      } else sv("path", { d, class: "core fill", fill: `url(#bonetex-${view})`, style: { stroke: "var(--bone-dk)", strokeWidth: 1.2, opacity: .9 } }, g);
    }
  } else if (sys === "derm") {
    for (const d of list) sv("path", { d, class: "fill core", style: { fill: o.col, fillOpacity: .38, stroke: o.col, strokeWidth: 1.5 } }, g);
  }
}

// ================= stage view & interaction =================
const stageEl = $("#stage"), tip = $("#tip");
function applyHide() {
  for (const v in stages) {
    const { svg, L } = stages[v];
    svg.setAttribute("data-hide", [...state.hide].join(" "));
    L.skin.style.opacity = state.skin / 100;
  }
}
// css for hiding layers (ctx/sel exempt)
(function () {
  const st = document.createElement("style");
  st.textContent = ["artery", "vein", "nerve", "muscle", "ref", "bone", "derm"].map(s => `svg[data-hide~="${s}"] .s[data-sys="${s}"]:not(.ctx):not(.sel){display:none}`).join("\n");
  document.head.appendChild(st);
})();

function setView(v) {
  state.view = v;
  $("#v-lat").setAttribute("aria-pressed", v === "lat");
  $("#v-ant").setAttribute("aria-pressed", v === "ant");
  if (!stages[v]) buildStage(v);
  $$("svg", stageEl).forEach(s => s.remove());
  stageEl.insertBefore(stages[v].svg, stageEl.firstChild);
  applyHide(); renderLabels(); applySelection();
}

const LAYERS = [["artery", "Arteries", "var(--artery)"], ["vein", "Veins", "var(--vein)"], ["nerve", "Nerves", "var(--nerve)"], ["muscle", "Expression muscles", "var(--muscle)"], ["ref", "Glands & landmarks", "var(--gland)"], ["bone", "Bone", "var(--bone-dk)"]];
function buildLayerChips() {
  const box = $("#layers");
  for (const [k, lab, col] of LAYERS) {
    const b = h("button", { class: "chip", "aria-pressed": "true", "data-layer": k }, `<i style="background:${col}"></i>${lab}`);
    b.onclick = () => {
      state.hide.has(k) ? state.hide.delete(k) : state.hide.add(k);
      b.setAttribute("aria-pressed", !state.hide.has(k));
      applyHide(); renderLabels();
    };
    box.appendChild(b);
  }
}

function svgPoint(svg, evt) {
  const pt = svg.createSVGPoint(); pt.x = evt.clientX; pt.y = evt.clientY;
  return pt.matrixTransform(svg.getScreenCTM().inverse());
}
// ---------- zoom / pan / tap (mouse + touch) ----------
function setVB(v, nb) {
  const st = stages[v]; if (!st) return;
  const w = Math.max(140, Math.min(600, nb.w)), h = w * 1.2;
  const x = Math.max(0, Math.min(600 - w, nb.x)), y = Math.max(0, Math.min(720 - h, nb.y));
  st.vb = { x, y, w, h };
  st.svg.setAttribute("viewBox", `${x} ${y} ${w} ${h}`);
}
function zoomAt(f, sx, sy) {
  const st = stages[state.view]; const vb = st.vb;
  let px = vb.x + vb.w / 2, py = vb.y + vb.h / 2;
  if (sx != null) { const m = st.svg.getScreenCTM(); px = (sx - m.e) / m.a; py = (sy - m.f) / m.d; }
  const nw = vb.w / f;
  setVB(state.view, { x: px - (px - vb.x) * (nw / vb.w), y: py - (py - vb.y) * (nw / vb.w), w: nw });
}
const ptrs = new Map(); let gest = null, lastTap = { t: 0, x: 0, y: 0 };
stageEl.addEventListener("pointerdown", e => {
  if (e.target.closest("button")) return;
  ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY, x0: e.clientX, y0: e.clientY });
  tip.style.opacity = 0;
  if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; gest = { type: "pinch", d: Math.hypot(a.x - b.x, a.y - b.y), mx: (a.x + b.x) / 2, my: (a.y + b.y) / 2 }; }
  else if (ptrs.size === 1) gest = { type: "tap", t: Date.now() };
});
stageEl.addEventListener("pointermove", e => {
  const p = ptrs.get(e.pointerId);
  if (!p) {
    if (e.pointerType !== "mouse") return;
    const g = e.target.closest && e.target.closest(".s");
    if (!g || state.quiz) { tip.style.opacity = 0; return; }
    const r = stageEl.getBoundingClientRect();
    tip.textContent = S[g.dataset.id].n;
    tip.style.left = (e.clientX - r.left) + "px"; tip.style.top = (e.clientY - r.top) + "px";
    tip.style.opacity = 1; return;
  }
  const dx = e.clientX - p.x, dy = e.clientY - p.y;
  p.x = e.clientX; p.y = e.clientY;
  const st = stages[state.view];
  if (gest && gest.type === "pinch" && ptrs.size >= 2) {
    const [a, b] = [...ptrs.values()];
    const d = Math.hypot(a.x - b.x, a.y - b.y), mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
    if (gest.d > 0) zoomAt(d / gest.d, mx, my);
    const m = st.svg.getScreenCTM();
    setVB(state.view, { x: st.vb.x - (mx - gest.mx) / m.a, y: st.vb.y - (my - gest.my) / m.d, w: st.vb.w });
    gest.d = d; gest.mx = mx; gest.my = my;
  } else if (gest && (gest.type === "pan" || Math.hypot(p.x - p.x0, p.y - p.y0) > 8)) {
    gest.type = "pan";
    const m = st.svg.getScreenCTM();
    setVB(state.view, { x: st.vb.x - dx / m.a, y: st.vb.y - dy / m.d, w: st.vb.w });
  }
});
function endPtr(e) {
  const p = ptrs.get(e.pointerId); if (!p) return;
  ptrs.delete(e.pointerId);
  if (e.type === "pointerup" && gest && gest.type === "tap" && ptrs.size === 0 && Date.now() - gest.t < 600) {
    const now = Date.now();
    if (now - lastTap.t < 320 && Math.hypot(e.clientX - lastTap.x, e.clientY - lastTap.y) < 30) {
      stages[state.view].vb.w < 599 ? setVB(state.view, { x: 0, y: 0, w: 600 }) : zoomAt(2.2, e.clientX, e.clientY);
      lastTap.t = 0;
    } else { lastTap = { t: now, x: e.clientX, y: e.clientY }; handleTap(e.clientX, e.clientY); }
  }
  if (ptrs.size === 0) gest = null;
  else if (ptrs.size === 1) gest = { type: "pan" };
}
stageEl.addEventListener("pointerup", endPtr);
stageEl.addEventListener("pointercancel", endPtr);
stageEl.addEventListener("pointerleave", e => { if (e.pointerType === "mouse") tip.style.opacity = 0; });
stageEl.addEventListener("wheel", e => {
  if (!e.ctrlKey && !e.metaKey) return;
  e.preventDefault(); zoomAt(Math.exp(-e.deltaY * 0.01), e.clientX, e.clientY);
}, { passive: false });
// iOS Safari page-zoom gesture events: keep them on the plate
["gesturestart", "gesturechange"].forEach(t => stageEl.addEventListener(t, e => e.preventDefault()));

function idsAt(cx, cy) {
  const ids = [];
  const offs = [[0, 0], [-12, 0], [12, 0], [0, -12], [0, 12], [-9, -9], [9, 9], [-9, 9], [9, -9]];
  for (const [dx, dy] of offs) {
    const els = document.elementsFromPoint ? document.elementsFromPoint(cx + dx, cy + dy) : [document.elementFromPoint(cx + dx, cy + dy)];
    for (const el of els) {
      const g = el && el.closest && el.closest(".s");
      if (g && stageEl.contains(g) && g.dataset.id !== "skull" && !ids.includes(g.dataset.id)) ids.push(g.dataset.id);
    }
  }
  return ids;
}
function showAlso(ids) {
  const box = $("#also");
  if (!ids.length) { box.hidden = true; box.innerHTML = ""; return; }
  box.innerHTML = "<span>Also here:</span>" + ids.slice(0, 6).map(k => `<button data-id="${k}">${esc(S[k].n.replace(/ \(.*\)$/, ""))}</button>`).join("");
  box.hidden = false;
  $$("button", box).forEach(b => b.onclick = ev => { ev.stopPropagation(); select(b.dataset.id, { trace: !!S[b.dataset.id].steps, keepAlso: true }); });
}
function handleTap(cx, cy) {
  const ids = idsAt(cx, cy);
  if (state.quiz) { quizAnswer(ids.includes(state.quiz.target) ? state.quiz.target : (ids[0] || null)); return; }
  if (!ids.length) { showAlso([]); select(null); return; }
  select(ids[0], { scroll: true });
  showAlso(ids.slice(1));
}
function bindZoomButtons() {
  $("#z-in").onclick = () => zoomAt(1.5);
  $("#z-out").onclick = () => zoomAt(1 / 1.5);
  $("#z-reset").onclick = () => setVB(state.view, { x: 0, y: 0, w: 600 });
}
const isPhone = () => window.matchMedia("(max-width: 820px)").matches;
function scrollToInfo() {
  if (!isPhone()) return;
  const sc = $(".stagecol").getBoundingClientRect();
  const stuckBottom = 52 + sc.height;
  const y = info.getBoundingClientRect().top + window.scrollY - stuckBottom - 8;
  window.scrollTo({ top: Math.max(0, y), behavior: reduceMotion ? "auto" : "smooth" });
}

function applySelection() {
  const st = stages[state.view]; if (!st) return;
  const { svg } = st;
  $$(".s.sel", svg).forEach(e => e.classList.remove("sel"));
  svg.classList.toggle("has-sel", !!state.sel);
  if (state.sel) $$(`.s[data-id="${state.sel}"]`, svg).forEach(e => { e.classList.add("sel"); e.parentNode.appendChild(e); });
  renderLabels();
}

function select(id, opts = {}) {
  stopTrace();
  if (!opts.keepAlso) showAlso([]);
  state.sel = id;
  if (id) {
    const o = S[id];
    if (!o[state.view]) setView(state.view === "lat" ? "ant" : "lat");
    if (state.hide.has(o.sys)) {
      state.hide.delete(o.sys);
      const chip = $(`#layers [data-layer="${o.sys}"]`); if (chip) chip.setAttribute("aria-pressed", "true");
      if (o.sys === "derm") $("#t-derm").setAttribute("aria-pressed", "true");
      applyHide();
    }
    try { history.replaceState(null, "", "#" + id); } catch (e) {}
  }
  applySelection();
  renderInfo(id);
  $$("#list li button").forEach(b => b.classList.toggle("on", b.dataset.id === id));
  if (opts.trace && id && S[id].steps) startTrace(id);
  if (id && (opts.scroll || opts.fromList)) scrollToInfo();
}

// ---------- labels ----------
function labelPoint(g) {
  try {
    const p = g.querySelector(".core");
    if (!p) return null;
    if (g.classList.contains("musc") || g.dataset.sys === "derm" || g.dataset.sys === "bone") {
      const b = p.getBBox(); return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
    }
    const len = p.getTotalLength(); return p.getPointAtLength(len * .55);
  } catch (e) { return null; }
}
function renderLabels() {
  const st = stages[state.view]; if (!st) return;
  const lg = st.L.labels; lg.innerHTML = "";
  const want = new Set();
  if (state.labels) $$(".s", st.svg).forEach(g => { if (!state.hide.has(g.dataset.sys) || g.classList.contains("ctx")) want.add(g); });
  if (state.sel) $$(`.s[data-id="${state.sel}"]`, st.svg).forEach(g => want.add(g));
  $$(".s.ctx", st.svg).forEach(g => want.add(g));
  const seen = new Set();
  for (const g of want) {
    const id = g.dataset.id;
    if (seen.has(id) && !state.labels) continue;
    seen.add(id);
    const pt = labelPoint(g); if (!pt) continue;
    if (state.view === "ant" && pt.x > 300 && !state.sel) continue;
    const name = S[id].n.replace(/ \((mastication|V1|V2|V3|C2|C3|C2, C3)\)$/, "");
    sv("text", { x: pt.x + 6, y: pt.y - 6, class: "lbl", text: name.length > 34 ? name.slice(0, 32) + "…" : name }, lg);
  }
}

// ================= info panel =================
const info = $("#info");
function wikiLink(o) { return `https://en.wikipedia.org/wiki/${o.w}`; }
function photoLink(o) {
  const q = o.n.replace(/\(.*?\)/g, "").replace(/[:,]/g, " ").trim();
  return `https://commons.wikimedia.org/w/index.php?search=${encodeURIComponent(q + " dissection")}&title=Special:MediaSearch&type=image`;
}
function cadaverLink(o) {
  const q = o.n.replace(/\(.*?\)/g, "").replace(/[:,]/g, " ").trim();
  return `https://www.google.com/search?tbm=isch&q=${encodeURIComponent(q + " cadaver dissection")}`;
}
function renderInfo(id) {
  if (!id) {
    info.innerHTML = `<div class="empty">
      <span class="kind">Start here</span>
      <h2>Click any structure on the plate</h2>
      <p class="sum">Each one opens its origin, course, relations, branches, termination and clinical notes. Arteries, veins and nerves have a <b>Trace course</b> button that walks a marker along the structure, step by step, lighting up everything it passes.</p>
      <ol>
        <li>Turn layers on and off with the chips. Drag the <b>Skin</b> slider to peel the face.</li>
        <li>Switch to <b>Anterior</b> for the muscles of facial expression and the V1/V2/V3 map.</li>
        <li>Use <b>Quiz: find it</b> once a system feels familiar.</li>
      </ol>
      <p class="note" style="margin-top:12px">Suggested first traces:</p>
      <div class="btnrow">${["facial_a", "sta", "facial_v", "cn7", "infraorbital_n", "occipital_a"].map(k => `<button class="btn" data-go="${k}">${esc(S[k].n)}</button>`).join("")}</div>
    </div>`;
    $$("[data-go]", info).forEach(b => b.onclick = () => select(b.dataset.go, { trace: true }));
    return;
  }
  const o = S[id], sy = SYS[o.sys];
  const dot = o.sys === "derm" ? o.col : sy.col;
  let html = `<span class="kind"><i style="background:${dot}"></i>${sy.label}${o.grp ? " · " + esc(o.grp) : ""}${o.br ? " · " + esc(o.br) : ""}</span>
    <h2>${esc(o.n)}</h2><p class="sum">${esc(o.sum || "")}</p>`;
  if (o.steps) html += `<div class="trace" id="tracebox">
      <div class="bar"><b>Trace the course</b>
        <button id="tr-prev" aria-label="Previous step">◀</button>
        <button id="tr-play" class="play">▶ Play</button>
        <button id="tr-next" aria-label="Next step">▶|</button></div>
      <ol>${o.steps.map((s, i) => `<li data-i="${i}">${esc(s[2])}</li>`).join("")}</ol></div>`;
  const keys = o.sys === "muscle" || (o.sys === "ref" && o.f && o.f.i) ? ["o", "i", "a", "n", "t", "r", "k"] : ["o", "c", "r", "b", "e", "s", "n", "p", "t", "k"];
  const f = o.f || {};
  const rows = keys.filter(k => f[k]).map(k => `<div><dt>${fieldLabel(k, o.sys)}</dt><dd class="${k === "k" ? "clin" : ""}">${esc(f[k])}</dd></div>`).join("");
  if (rows) html += `<dl>${rows}</dl>`;
  html += `<div class="links">
    <a href="${photoLink(o)}" target="_blank" rel="noopener">Real dissection photos ↗</a>
    <a href="${cadaverLink(o)}" target="_blank" rel="noopener">Cadaver images ↗</a>
    <a href="${wikiLink(o)}" target="_blank" rel="noopener">Gray's plates (Wikipedia) ↗</a></div>`;
  info.innerHTML = html;
  if (o.steps) {
    $("#tr-play").onclick = () => state.trace && state.trace.playing ? pauseTrace() : (state.trace ? playTrace() : startTrace(id, true));
    $("#tr-next").onclick = () => { if (!state.trace) startTrace(id); else gotoStep(state.trace.i + 1); };
    $("#tr-prev").onclick = () => { if (state.trace) gotoStep(state.trace.i - 1); };
    $$("#tracebox li").forEach(li => li.onclick = () => { if (!state.trace) startTrace(id); gotoStep(+li.dataset.i); });
  }
}

// ================= trace engine =================
function tracePathEl(id) {
  const svg = stages[state.view].svg;
  const g = svg.querySelector(`.s[data-id="${id}"]`);
  return g ? g.querySelector(".core") : null;
}
function lenAt(path, x, y) {
  const total = path.getTotalLength(); let best = 0, bd = Infinity;
  for (let i = 0; i <= 400; i++) {
    const l = total * i / 400, p = path.getPointAtLength(l), d = (p.x - x) ** 2 + (p.y - y) ** 2;
    if (d < bd) { bd = d; best = l; }
  }
  return best;
}
function startTrace(id, autoplay = false) {
  stopTrace();
  if (S[id].lat && state.view !== "lat") setView("lat");
  if (state.sel !== id) { state.sel = id; applySelection(); }
  const path = tracePathEl(id); if (!path) return;
  const st = stages[state.view], tg = st.L.trace;
  const total = path.getTotalLength();
  const col = SYS[S[id].sys].col;
  const trail = sv("path", { d: path.getAttribute("d"), class: "trail", style: { stroke: col, strokeWidth: (S[id].wd || 2.4) + 7, strokeOpacity: .35, strokeDasharray: `0 ${total}` } }, tg);
  const marker = sv("g", { class: "marker" }, tg);
  sv("circle", { r: 11, style: { fill: "none", stroke: "var(--ink)", strokeWidth: 2 } }, marker);
  sv("circle", { r: 4.5, style: { fill: "var(--ink)" } }, marker);
  const steps = S[id].steps.map(s => ({ len: lenAt(path, s[0], s[1]), s }));
  state.trace = { id, path, total, trail, marker, steps, i: -1, cur: 0, playing: false, timer: null, raf: null };
  gotoStep(0);
  if (autoplay) playTrace();
}
function gotoStep(i) {
  const t = state.trace; if (!t) return;
  i = Math.max(0, Math.min(t.steps.length - 1, i));
  t.i = i;
  const target = t.steps[i].len, from = t.cur;
  const animate = (now0) => {
    const dur = reduceMotion ? 1 : 900;
    const tick = now => {
      const k = Math.min(1, (now - now0) / dur), e = k < .5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
      const l = from + (target - from) * e;
      setMarker(l);
      if (k < 1) t.raf = requestAnimationFrame(tick); else t.cur = target;
    };
    t.raf = requestAnimationFrame(tick);
  };
  cancelAnimationFrame(t.raf);
  animate(performance.now());
  // context highlight
  const svg = stages[state.view].svg;
  $$(".s.ctx", svg).forEach(e => e.classList.remove("ctx"));
  (t.steps[i].s[3] || []).forEach(h => $$(`.s[data-id="${h}"]`, svg).forEach(e => e.classList.add("ctx")));
  renderLabels();
  $$("#tracebox li").forEach((li, k) => { li.classList.toggle("cur", k === i); li.classList.toggle("done", k < i); });
  document.body.classList.add("tracing");
  $("#tb-c").textContent = `${S[t.id].n} · step ${i + 1} of ${t.steps.length}`;
  $("#tb-t").textContent = t.steps[i].s[2];
  const cur = $(`#tracebox li[data-i="${i}"]`);
  if (cur) cur.scrollIntoView({ block: "nearest", behavior: reduceMotion ? "auto" : "smooth" });
}
function setMarker(l) {
  const t = state.trace; if (!t) return;
  const p = t.path.getPointAtLength(l);
  t.marker.setAttribute("transform", `translate(${p.x} ${p.y})`);
  t.trail.style.strokeDasharray = `${l} ${t.total}`;
  const vb = stages[state.view].vb;
  if (vb.w < 599) setVB(state.view, { x: p.x - vb.w / 2, y: p.y - vb.h / 2, w: vb.w });
}
function playTrace() {
  const t = state.trace; if (!t) return;
  t.playing = true; $("#tr-play") && ($("#tr-play").textContent = "❚❚ Pause"); $("#tb-play").textContent = "❚❚";
  if (t.i >= t.steps.length - 1) gotoStep(0);
  clearInterval(t.timer);
  t.timer = setInterval(() => {
    if (t.i >= t.steps.length - 1) { pauseTrace(); return; }
    gotoStep(t.i + 1);
  }, 4200);
}
function pauseTrace() {
  const t = state.trace; if (!t) return;
  t.playing = false; clearInterval(t.timer);
  $("#tr-play") && ($("#tr-play").textContent = "▶ Play"); $("#tb-play").textContent = "▶";
}
function stopTrace() {
  const t = state.trace; if (!t) return;
  clearInterval(t.timer); cancelAnimationFrame(t.raf);
  t.trail.remove(); t.marker.remove();
  for (const v in stages) $$(".s.ctx", stages[v].svg).forEach(e => e.classList.remove("ctx"));
  state.trace = null;
  document.body.classList.remove("tracing");
}

// ================= side list =================
const GROUP_ORDER = ["Carotid system", "Facial artery & branches", "Maxillary artery", "Scalp arteries", "Veins of the face", "Veins of the scalp", "Facial nerve (motor)", "Trigeminal (sensory)", "Cervical nerves (scalp)", "Scalp", "Orbit", "Nose", "Mouth", "Ear", "Neck", "Landmarks", "Bone & foramina", "Sensory territories"];
const GROUP_TITLE = { Scalp: "Muscles: scalp", Orbit: "Muscles: around the eye", Nose: "Muscles: nose", Mouth: "Muscles: mouth", Ear: "Muscles: ear", Neck: "Muscles: neck" };
function buildList() {
  const box = $("#list"); box.innerHTML = "";
  const q = ($("#filter").value || "").toLowerCase();
  for (const grp of GROUP_ORDER) {
    const ids = Object.keys(S).filter(k => S[k].grp === grp && (!q || S[k].n.toLowerCase().includes(q)));
    if (!ids.length) continue;
    const sys = S[ids[0]].sys;
    const d = h("details", q || ["Facial artery & branches", "Facial nerve (motor)"].includes(grp) ? { open: "" } : {});
    d.innerHTML = `<summary><i style="background:${SYS[sys].col}"></i>${esc(GROUP_TITLE[grp] || grp)}</summary>`;
    const ul = h("ul");
    ids.forEach(k => {
      const li = h("li"); const b = h("button", { "data-id": k }, esc(S[k].n));
      b.onclick = () => select(k, { trace: !!S[k].steps, fromList: true });
      if (k === state.sel) b.classList.add("on");
      li.appendChild(b); ul.appendChild(li);
    });
    d.appendChild(ul); box.appendChild(d);
  }
}

// ================= find-it quiz =================
function quizPool() {
  const svg = stages[state.view].svg;
  const ids = new Set();
  $$(".s", svg).forEach(g => { if (!state.hide.has(g.dataset.sys) && !["skull"].includes(g.dataset.id)) ids.add(g.dataset.id); });
  return [...ids];
}
function quizNext() {
  const pool = quizPool();
  if (!pool.length) { $("#q-target").textContent = "Turn on a layer first"; return; }
  let id; do { id = pool[Math.floor(Math.random() * pool.length)]; } while (pool.length > 1 && id === state.quiz.last);
  state.quiz.target = id; state.quiz.last = id;
  $("#q-target").textContent = S[id].n;
}
function quizStart() {
  select(null);
  state.quiz = { right: 0, total: 0, target: null };
  $("#quizbar").hidden = false; $("#t-quiz").setAttribute("aria-pressed", "true");
  quizUpdate(); quizNext();
}
function quizStop() {
  state.quiz = null; $("#quizbar").hidden = true; $("#t-quiz").setAttribute("aria-pressed", "false");
}
function quizUpdate() { $("#q-score").textContent = `${state.quiz.right} / ${state.quiz.total}`; }
function flash(id) {
  const svg = stages[state.view].svg;
  $$(`.s[data-id="${id}"]`, svg).forEach(e => { e.classList.remove("flash"); void e.getBBox(); e.classList.add("flash"); setTimeout(() => e.classList.remove("flash"), 2100); });
}
function quizAnswer(id) {
  const q = state.quiz; if (!q || !q.target || q.lock) return;
  q.total++;
  const ok = id === q.target;
  if (ok) q.right++;
  quizUpdate();
  $("#q-target").textContent = ok ? `Correct: ${S[q.target].n}` : `That was ${id ? S[id].n : "nothing"}. Here is ${S[q.target].n}`;
  flash(q.target);
  q.lock = true;
  setTimeout(() => { if (state.quiz) { state.quiz.lock = false; quizNext(); } }, ok ? 1100 : 2300);
}

// ================= init atlas =================
function initAtlas() {
  buildLayerChips();
  buildStage("lat");
  setView("lat");
  buildList();
  $("#filter").addEventListener("input", buildList);
  $("#v-lat").onclick = () => { stopTrace(); setView("lat"); };
  $("#v-ant").onclick = () => { stopTrace(); setView("ant"); };
  $("#skin").addEventListener("input", e => { state.skin = +e.target.value; applyHide(); });
  $("#t-derm").onclick = () => {
    const on = state.hide.has("derm");
    on ? state.hide.delete("derm") : state.hide.add("derm");
    $("#t-derm").setAttribute("aria-pressed", on); applyHide(); renderLabels();
  };
  $("#t-lbl").onclick = () => { state.labels = !state.labels; $("#t-lbl").setAttribute("aria-pressed", state.labels); renderLabels(); };
  $("#t-quiz").onclick = () => state.quiz ? quizStop() : quizStart();
  $("#q-skip").onclick = () => { if (state.quiz) { flash(state.quiz.target); quizNext(); } };
  $("#q-stop").onclick = quizStop;
  bindZoomButtons();
  $("#tb-prev").onclick = () => state.trace && gotoStep(state.trace.i - 1);
  $("#tb-next").onclick = () => state.trace && gotoStep(state.trace.i + 1);
  $("#tb-play").onclick = () => state.trace && (state.trace.playing ? pauseTrace() : playTrace());
  $("#tb-x").onclick = () => stopTrace();
  let sw = null;
  const tb = $("#tbar");
  tb.addEventListener("touchstart", e => { sw = { x: e.touches[0].clientX, y: e.touches[0].clientY }; }, { passive: true });
  tb.addEventListener("touchend", e => {
    if (!sw || !state.trace) return;
    const dx = e.changedTouches[0].clientX - sw.x, dy = e.changedTouches[0].clientY - sw.y; sw = null;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.5) gotoStep(state.trace.i + (dx < 0 ? 1 : -1));
  }, { passive: true });
  const hash = location.hash.slice(1);
  if (S[hash]) select(hash); else renderInfo(null);
}

// ================= tabs =================
function showTab(name) {
  $$("nav.tabs button").forEach(b => b.setAttribute("aria-selected", b.dataset.tab === name));
  $$("section.tab").forEach(s => s.hidden = s.id !== "tab-" + name);
  store.set("tab", name);
  if (name !== "explore") { stopTrace(); }
}
$$("nav.tabs button").forEach(b => b.onclick = () => showTab(b.dataset.tab));

// ================= facial nerve lesion tab =================
const CN7_ST = [
  { id: "umn", x: 70, y: 52, n: "Upper motor neuron (cortex / corticobulbar tract)", ex: "Stroke, tumour in the motor cortex or internal capsule. Deficit is on the OPPOSITE side." },
  { id: "nuc", x: 70, y: 150, n: "Facial motor nucleus (pons)", ex: "Pontine infarct or demyelination. Fibres loop round the abducens nucleus (facial colliculus), so a lateral gaze palsy often comes with it. Taste and secretomotor nuclei are separate, so they are spared." },
  { id: "cpa", x: 175, y: 168, n: "Cerebellopontine angle / internal acoustic meatus", ex: "Vestibular schwannoma (acoustic neuroma), meningioma. CN VIII travels with it: hearing loss, tinnitus, imbalance." },
  { id: "lab", x: 268, y: 150, n: "Labyrinthine segment (narrowest part of the canal)", ex: "The canal is tightest here: inflammatory swelling in Bell's palsy is thought to compress the nerve at this point. Everything distal is affected." },
  { id: "gen", x: 320, y: 120, n: "Geniculate ganglion", ex: "Ramsay Hunt syndrome (herpes zoster oticus): vesicles in the ear canal and auricle, severe pain, often with vertigo and hearing loss. GSPN leaves here." },
  { id: "tym", x: 405, y: 140, n: "Tympanic segment (after GSPN, before nerve to stapedius)", ex: "Middle ear disease (cholesteatoma, otitis media with a dehiscent canal), middle ear surgery, temporal bone fracture." },
  { id: "mas", x: 472, y: 258, n: "Mastoid segment (between nerve to stapedius and chorda tympani)", ex: "Mastoid surgery, longitudinal temporal bone fracture." },
  { id: "sty", x: 472, y: 342, n: "Stylomastoid foramen (distal to chorda tympani)", ex: "Trauma, forceps delivery (no mastoid process in the newborn), deep facial lacerations. Pure motor palsy of the whole half of the face." },
  { id: "par", x: 472, y: 418, n: "Within the parotid / terminal branches", ex: "Parotid malignancy, parotidectomy, facial lacerations. Only the muscles of the injured branches are weak." }
];
const CN7_FX = [
  ["Forehead (frontalis)", { umn: "spared", nuc: "lost", cpa: "lost", lab: "lost", gen: "lost", tym: "lost", mas: "lost", sty: "lost", par: "var" }],
  ["Eye closure, lower face", { umn: "lost*", nuc: "lost", cpa: "lost", lab: "lost", gen: "lost", tym: "lost", mas: "lost", sty: "lost", par: "var" }],
  ["Tear secretion (GSPN)", { umn: "spared", nuc: "spared", cpa: "lost", lab: "lost", gen: "lost", tym: "spared", mas: "spared", sty: "spared", par: "spared" }],
  ["Stapedius: hyperacusis if lost", { umn: "spared", nuc: "spared", cpa: "lost", lab: "lost", gen: "lost", tym: "lost", mas: "spared", sty: "spared", par: "spared" }],
  ["Taste, anterior 2/3 tongue (chorda)", { umn: "spared", nuc: "spared", cpa: "lost", lab: "lost", gen: "lost", tym: "lost", mas: "lost", sty: "spared", par: "spared" }],
  ["Submandibular & sublingual saliva", { umn: "spared", nuc: "spared", cpa: "lost", lab: "lost", gen: "lost", tym: "lost", mas: "lost", sty: "spared", par: "spared" }],
  ["Hearing (CN VIII)", { umn: "spared", nuc: "spared", cpa: "lost", lab: "spared", gen: "var", tym: "spared", mas: "spared", sty: "spared", par: "spared" }],
  ["Lateral gaze (CN VI)", { umn: "spared", nuc: "lost", cpa: "spared", lab: "spared", gen: "spared", tym: "spared", mas: "spared", sty: "spared", par: "spared" }]
];
function buildCN7() {
  const svg = sv("svg", { viewBox: "0 0 640 560", role: "img", "aria-label": "Course of the facial nerve" });
  const defs = sv("defs", {}, svg);
  const mk = sv("marker", { id: "arr7", viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, defs);
  sv("path", { d: "M0 0 L10 5 L0 10 Z", style: { fill: "var(--nerve-dk)" } }, mk);
  const T = (x, y, t, o = {}) => sv("text", { x, y, text: t, style: Object.assign({ fontFamily: "var(--f-body)", fontSize: "12.5px", fill: "var(--ink)", fontWeight: 700 }, o) }, svg);
  const tm = (x, y, t, o = {}) => T(x, y, t, Object.assign({ fontWeight: 400, fill: "var(--muted)", fontSize: "11.5px" }, o));
  // regions
  sv("rect", { x: 20, y: 95, width: 120, height: 85, rx: 14, style: { fill: "var(--stage2)", stroke: "var(--line)" } }, svg);
  tm(30, 112, "Brainstem (pons)");
  sv("rect", { x: 225, y: 82, width: 280, height: 290, rx: 14, style: { fill: "var(--bone)", fillOpacity: .28, stroke: "var(--bone-dk)", strokeDasharray: "4 4" } }, svg);
  tm(400, 365, "Facial canal, temporal bone");
  sv("ellipse", { cx: 472, cy: 470, rx: 120, ry: 66, style: { fill: "var(--gland)", fillOpacity: .3, stroke: "var(--bone-dk)" } }, svg);
  tm(372, 455, "Parotid gland");
  // CN VIII
  sv("path", { d: "M90 172 C 130 185, 170 188, 240 186", style: { fill: "none", stroke: "var(--muted)", strokeWidth: 3, strokeDasharray: "6 4" } }, svg);
  tm(150, 200, "CN VIII alongside");
  // UMN
  sv("path", { d: "M70 52 L 70 150", style: { fill: "none", stroke: "var(--nerve-dk)", strokeWidth: 2.5, strokeDasharray: "5 5" } }, svg);
  tm(84, 98, "corticobulbar fibres");
  // main nerve
  const main = "M70 150 C 110 152, 140 164, 175 168 L 240 168 C 252 166, 262 158, 268 150 C 282 136, 300 124, 320 120 C 360 125, 405 140, 440 150 C 462 158, 472 172, 472 192 L 472 342 L 472 418";
  sv("path", { d: main, style: { fill: "none", stroke: "var(--nerve-dk)", strokeWidth: 9, strokeLinecap: "round", strokeLinejoin: "round" } }, svg);
  sv("path", { d: main, style: { fill: "none", stroke: "var(--nerve)", strokeWidth: 6, strokeLinecap: "round", strokeLinejoin: "round" } }, svg);
  // branches
  const br = (d, label, lx, ly, lines) => {
    sv("path", { d, "marker-end": "url(#arr7)", style: { fill: "none", stroke: "var(--nerve-dk)", strokeWidth: 3 } }, svg);
    sv("path", { d, style: { fill: "none", stroke: "var(--nerve)", strokeWidth: 1.6 } }, svg);
    T(lx, ly, label); (lines || []).forEach((l, i) => tm(lx, ly + 15 + i * 14, l));
  };
  br("M320 120 C 300 90, 270 60, 230 44", "Greater petrosal n.", 92, 24, ["→ pterygopalatine ganglion → lacrimal,", "nasal & palatine glands"]);
  br("M472 215 L 560 215", "Nerve to stapedius", 520, 200, []);
  br("M472 298 C 515 292, 552 278, 590 262", "Chorda tympani", 520, 244, []);
  tm(500, 318, "→ lingual n.: taste ant. 2/3,");
  tm(500, 332, "submandibular & sublingual glands");
  br("M472 360 C 500 360, 525 352, 548 340", "Post. auricular, digastric, stylohyoid", 430, 382, []);
  const fan = [["Temporal", 370], ["Zygomatic", 420], ["Buccal", 472], ["Marg. mand.", 524], ["Cervical", 586]];
  fan.forEach(([n, x]) => { sv("path", { d: `M472 418 C 472 455, ${x} 470, ${x} 515`, style: { fill: "none", stroke: "var(--nerve-dk)", strokeWidth: 3 } }, svg); sv("path", { d: `M472 418 C 472 455, ${x} 470, ${x} 515`, style: { fill: "none", stroke: "var(--nerve)", strokeWidth: 1.6 } }, svg); T(x - 28, 533, n, { fontSize: "11px" }); });
  // station labels
  const lbl = { umn: [84, 40, "Motor cortex"], nuc: [84, 140, "Nucleus"], cpa: [150, 158, "CPA"], lab: [232, 142, ""], gen: [330, 108, "Geniculate"], tym: [385, 128, "Tympanic"], mas: [482, 262, "Mastoid"], sty: [482, 346, "Stylomastoid foramen"], par: [486, 410, ""] };
  CN7_ST.forEach(s => {
    const g = sv("g", { class: "st", "data-st": s.id, tabindex: "0", role: "button", "aria-label": s.n, style: { cursor: "pointer" } }, svg);
    sv("circle", { cx: s.x, cy: s.y, r: 15, style: { fill: "transparent" } }, g);
    sv("circle", { cx: s.x, cy: s.y, r: 8, class: "dot", style: { fill: "var(--panel)", stroke: "var(--ink)", strokeWidth: 2 } }, g);
    const L = lbl[s.id]; if (L[2]) T(L[0], L[1], L[2], { fontSize: "11.5px" });
    g.onclick = () => setLesion(s.id);
    g.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setLesion(s.id); } };
  });
  const x = sv("g", { id: "lesionX", style: { pointerEvents: "none" } }, svg);
  sv("path", { d: "M-11 -11 L11 11 M11 -11 L-11 11", style: { stroke: "var(--bad)", strokeWidth: 5, strokeLinecap: "round" } }, x);
  $("#cn7diagram").appendChild(svg);
  setLesion("sty");
}
function setLesion(id) {
  const s = CN7_ST.find(z => z.id === id);
  $("#lesionX").setAttribute("transform", `translate(${s.x} ${s.y})`);
  $$("#cn7diagram .dot").forEach(d => d.style.fill = d.parentNode.dataset.st === id ? "var(--bad)" : "var(--panel)");
  const pill = v => v === "var" ? `<span class="pill var">depends on branch</span>` : v.startsWith("lost") ? `<span class="pill lost">${id === "umn" && v === "lost*" ? "weak (opposite side)" : "lost"}</span>` : `<span class="pill spared">spared</span>`;
  $("#cn7out").innerHTML = `<span class="note" style="font-family:var(--f-mono);text-transform:uppercase;letter-spacing:.1em;font-size:11px">Lesion at</span>
   <h3>${esc(s.n)}</h3><p style="margin-top:0">${esc(s.ex)}</p>
   <div class="tablewrap"><table class="deficit"><thead><tr><th>Function</th><th>Result</th></tr></thead><tbody>
   ${CN7_FX.map(([n, m]) => `<tr><td>${esc(n)}</td><td>${pill(m[id])}</td></tr>`).join("")}</tbody></table></div>
   <p class="note" style="margin-bottom:0"><b>Rule:</b> a function is lost only if its branch leaves the nerve <i>distal</i> to the lesion. Order of branches: GSPN (geniculate) → nerve to stapedius → chorda tympani → stylomastoid foramen → 5 motor branches. ${id === "umn" ? "UMN lesions spare the forehead because the upper face receives cortical input from both hemispheres." : ""}</p>`;
}

// ================= scalp tab =================
const SCALP_L = [
  { id: "S", y: 30, h: 50, n: "Skin", col: "var(--skin)", t: "Thick, hair-bearing, rich in sebaceous and sweat glands.", k: "The commonest site of sebaceous cysts. Hair follicles extend into layer C." },
  { id: "C", y: 80, h: 64, n: "Connective tissue (dense)", col: "var(--fascia)", t: "Dense fibro-fatty tissue with fibrous septa binding skin to the galea. Carries the arteries, veins, nerves and lymphatics of the scalp.", k: "Vessel walls are anchored to the septa, so cut vessels cannot retract or constrict: scalp wounds bleed profusely. Infection here stays localised and is very painful (tension in the septa). Layers S, C and A move together as one: the 'scalp proper'." },
  { id: "A", y: 144, h: 30, n: "Aponeurosis (galea aponeurotica)", col: "var(--bone)", t: "Tough tendinous sheet joining frontalis and occipitalis; laterally becomes the temporal fascia.", k: "A wound gapes only if the galea is divided (especially transversely), because frontalis and occipitalis pull the edges apart. Suture the galea in deep wounds to stop bleeding and close dead space." },
  { id: "L", y: 174, h: 52, n: "Loose areolar tissue: the 'danger area'", col: "var(--stage2)", t: "Loose, spongy tissue that lets the scalp proper slide over the pericranium. Crossed by the emissary veins.", k: "Infection spreads easily here and can reach the dural venous sinuses through valveless emissary veins (meningitis, sinus thrombosis). Blood collects here in a subgaleal haemorrhage, which crosses sutures and can track forward into the eyelids (frontalis inserts into skin, not bone) → 'black eyes'. Scalping injuries tear through this plane." },
  { id: "P", y: 226, h: 18, n: "Pericranium", col: "var(--muscle)", t: "Periosteum of the skull bones. Dips into the sutures to become continuous with the endosteal dura.", k: "Because it is fixed at the sutures, a subperiosteal collection (cephalhaematoma in the newborn) is limited to one bone and does not cross suture lines." }
];
const SCALP_X = [
  { id: "bone", y: 244, h: 80, n: "Skull: outer table, diploë, inner table", col: "var(--bone)", t: "The diploë between the tables holds red marrow and valveless diploic veins that connect scalp veins with the dural sinuses.", k: "Diploic veins are another route for infection to spread inward (osteomyelitis of the skull)." },
  { id: "dura", y: 324, h: 16, n: "Dura mater & superior sagittal sinus", col: "var(--vein)", t: "Endosteal and meningeal layers separate in the midline to enclose the superior sagittal sinus, which receives emissary veins from the scalp.", k: "Scalp infection → emissary vein → superior sagittal sinus thrombosis." }
];
const FLUID = {
  caput: { n: "Caput succedaneum", d: "M90 112 C 170 92, 520 92, 610 112 C 520 140, 170 140, 90 112 Z", col: "var(--warn)", t: "Serosanguineous oedema of the skin and subcutaneous tissue (layers S–C) from pressure during delivery. Crosses sutures; present at birth; resolves in days." },
  subgaleal: { n: "Subgaleal haemorrhage", d: "M50 200 C 150 168, 550 168, 650 200 C 550 232, 150 232, 50 200 Z", col: "var(--bad)", t: "Bleeding into the loose areolar layer (L). Not limited by sutures; can hold a large blood volume and cause shock in a newborn (e.g. after vacuum delivery). Fluctuant, shifts with position." },
  cephal: { n: "Cephalhaematoma", d: "M140 244 C 200 214, 300 214, 345 244 Z", col: "var(--artery)", t: "Subperiosteal bleed, between pericranium and bone. Limited by suture lines because the pericranium is attached there. Appears hours after birth; may calcify; risk of jaundice." }
};
let scalpFluid = null;
function buildScalp() {
  const svg = sv("svg", { viewBox: "0 0 700 430", role: "img", "aria-label": "Layers of the scalp in section" });
  const defs = sv("defs", {}, svg);
  const all = [...SCALP_L, ...SCALP_X];
  // layer bands
  all.forEach(l => {
    const g = sv("g", { class: "sl", "data-l": l.id, style: { cursor: "pointer" }, tabindex: "0", role: "button", "aria-label": l.n }, svg);
    if (l.id === "bone") {
      sv("rect", { x: 20, y: l.y, width: 660, height: 22, style: { fill: "var(--bone)" } }, g);
      sv("rect", { x: 20, y: l.y + 22, width: 660, height: 36, style: { fill: "var(--bone)", opacity: .6 } }, g);
      for (let i = 0; i < 90; i++) sv("circle", { cx: 25 + (i * 73) % 650, cy: l.y + 26 + (i * 29) % 30, r: 2 + (i % 3), style: { fill: "var(--bone-dk)", opacity: .4 } }, g);
      sv("rect", { x: 20, y: l.y + 58, width: 660, height: 22, style: { fill: "var(--bone)" } }, g);
      sv("ellipse", { cx: 520, cy: l.y + 40, rx: 26, ry: 7, style: { fill: "var(--vein)", opacity: .85 } }, g);
      sv("text", { x: 552, y: l.y + 44, text: "diploic v.", style: { fontSize: "11px", fill: "var(--ink)", fontFamily: "var(--f-body)" } }, g);
      // suture gap
      sv("rect", { x: 346, y: l.y, width: 8, height: 80, style: { fill: "var(--muscle)" } }, g);
    } else if (l.id === "dura") {
      sv("rect", { x: 20, y: l.y, width: 660, height: l.h, style: { fill: "var(--muted)", opacity: .5 } }, g);
      sv("path", { d: `M310 ${l.y} L 390 ${l.y} L 350 ${l.y + 50} Z`, style: { fill: "var(--vein)", opacity: .9 } }, g);
      sv("text", { x: 395, y: l.y + 40, text: "superior sagittal sinus", style: { fontSize: "11px", fill: "var(--ink)", fontFamily: "var(--f-body)", fontWeight: 700 } }, g);
    } else {
      sv("rect", { x: 20, y: l.y, width: 660, height: l.h, style: { fill: l.col, opacity: l.id === "L" ? .6 : .92 } }, g);
    }
    sv("rect", { x: 20, y: l.y, width: 660, height: l.h, class: "slhl", style: { fill: "none", stroke: "var(--ink)", strokeWidth: 0 } }, g);
    g.onclick = () => scalpShow(l.id);
    g.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); scalpShow(l.id); } };
  });
  // hair
  for (let x = 30; x < 680; x += 14) sv("path", { d: `M${x} 70 C ${x + 2} 50, ${x - 3} 30, ${x + 4} 6`, style: { fill: "none", stroke: "var(--hair)", strokeWidth: 1.4, opacity: .8, pointerEvents: "none" } }, svg);
  // septa in C
  for (let x = 40; x < 680; x += 46) sv("path", { d: `M${x} 80 C ${x + 8} 100, ${x - 6} 120, ${x + 4} 144`, style: { fill: "none", stroke: "var(--skin-dk)", strokeWidth: 1.2, pointerEvents: "none" } }, svg);
  // vessels in C
  [[130, "a"], [158, "v"], [182, "n"], [440, "a"], [468, "v"], [492, "n"], [600, "a"], [626, "v"]].forEach(([x, k]) => {
    const c = k === "a" ? "var(--artery)" : k === "v" ? "var(--vein)" : "var(--nerve)";
    sv("circle", { cx: x, cy: 113, r: k === "n" ? 6 : 8, style: { fill: c, stroke: "var(--ink)", strokeWidth: .8, pointerEvents: "none" } }, svg);
  });
  // loose areolar fibres
  for (let x = 30; x < 680; x += 26) sv("path", { d: `M${x} 186 q 8 10 0 18 q -8 8 4 16`, style: { fill: "none", stroke: "var(--muted)", strokeWidth: .8, opacity: .6, pointerEvents: "none" } }, svg);
  // emissary vein
  sv("path", { d: "M310 113 C 312 150, 330 190, 338 230 C 344 270, 346 300, 350 340", style: { fill: "none", stroke: "var(--vein)", strokeWidth: 5, strokeLinecap: "round", pointerEvents: "none" } }, svg);
  sv("text", { x: 200, y: 214, text: "emissary vein", style: { fontSize: "11.5px", fill: "var(--ink)", fontWeight: 700, fontFamily: "var(--f-body)", pointerEvents: "none" } }, svg);
  sv("text", { x: 360, y: 260, text: "suture", style: { fontSize: "11px", fill: "var(--ink)", fontFamily: "var(--f-body)", pointerEvents: "none" } }, svg);
  sv("rect", { x: 20, y: 380, width: 660, height: 40, rx: 6, style: { fill: "var(--muscle)", opacity: .25, pointerEvents: "none" } }, svg);
  sv("text", { x: 30, y: 404, text: "Arachnoid, pia, brain", style: { fontSize: "11.5px", fill: "var(--muted)", fontFamily: "var(--f-body)" } }, svg);
  // layer letters
  all.forEach(l => sv("text", { x: 690, y: l.y + Math.min(l.h, 40) / 2 + 5, "text-anchor": "end", text: l.id.length === 1 ? l.id : "", style: { fontFamily: "var(--f-display)", fontWeight: 700, fontSize: "18px", fill: "var(--ink)", pointerEvents: "none" } }, svg));
  // fluids
  const fg = sv("g", { id: "fluid", style: { pointerEvents: "none" } }, svg);
  $("#scalpdiagram").appendChild(svg);
  const btns = $("#scalpbtns");
  for (const k in FLUID) {
    const b = h("button", { class: "btn", "data-f": k }, esc(FLUID[k].n));
    b.onclick = () => {
      scalpFluid = scalpFluid === k ? null : k;
      $$("#scalpbtns .btn").forEach(x => x.classList.toggle("on", x.dataset.f === scalpFluid));
      fg.innerHTML = "";
      if (scalpFluid) {
        sv("path", { d: FLUID[k].d, style: { fill: FLUID[k].col, fillOpacity: .55, stroke: FLUID[k].col, strokeWidth: 2 } }, fg);
        $("#scalpout").innerHTML = `<h3>${esc(FLUID[k].n)}</h3><p>${esc(FLUID[k].t)}</p><p class="note">Compare the three: caput lies above the galea; subgaleal is in layer L; cephalhaematoma is under the pericranium, stopping at the suture.</p>`;
      } else scalpShow("L");
    };
    btns.appendChild(b);
  }
  scalpShow("L");
  // table
  $("#scalptable").innerHTML = `<thead><tr><th>Region</th><th>Artery</th><th>Vein drains to</th><th>Sensory nerve</th><th>Lymph nodes</th></tr></thead><tbody>
   <tr><td>Medial forehead</td><td><span class="a">Supratrochlear</span> (ophthalmic ← ICA)</td><td><span class="v">Supratrochlear v.</span> → angular → facial v.</td><td><span class="n">Supratrochlear</span> (V1)</td><td>Submandibular, parotid</td></tr>
   <tr><td>Forehead to vertex</td><td><span class="a">Supraorbital</span> (ophthalmic ← ICA)</td><td><span class="v">Supraorbital v.</span> → angular → facial v.</td><td><span class="n">Supraorbital</span> (V1)</td><td>Parotid (preauricular)</td></tr>
   <tr><td>Anterior temple</td><td>Zygomatico-orbital (STA)</td><td>Superficial temporal v.</td><td><span class="n">Zygomaticotemporal</span> (V2)</td><td>Parotid</td></tr>
   <tr><td>Temple & side of scalp</td><td><span class="a">Superficial temporal</span> (ECA)</td><td><span class="v">Superficial temporal v.</span> → retromandibular</td><td><span class="n">Auriculotemporal</span> (V3)</td><td>Parotid (preauricular)</td></tr>
   <tr><td>Behind the ear</td><td><span class="a">Posterior auricular</span> (ECA)</td><td><span class="v">Posterior auricular v.</span> → EJV</td><td><span class="n">Lesser occipital</span> (C2), <span class="n">great auricular</span> (C2, C3)</td><td>Mastoid (retroauricular)</td></tr>
   <tr><td>Back of scalp</td><td><span class="a">Occipital</span> (ECA)</td><td><span class="v">Occipital v.</span> → suboccipital plexus</td><td><span class="n">Greater occipital</span> (C2), <span class="n">third occipital</span> (C3)</td><td>Occipital</td></tr>
   <tr><td>Motor</td><td colspan="4">Frontalis: temporal branch of CN VII. Occipitalis: posterior auricular branch of CN VII. Auricular muscles: temporal & posterior auricular branches.</td></tr></tbody>`;
}
function scalpShow(id) {
  const l = [...SCALP_L, ...SCALP_X].find(z => z.id === id);
  $$("#scalpdiagram .slhl").forEach(r => r.style.strokeWidth = r.parentNode.dataset.l === id ? 3 : 0);
  $("#scalpout").innerHTML = `<span class="note" style="font-family:var(--f-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase">${id.length === 1 ? "Layer " + id : "Beneath the scalp"}</span>
   <h3>${esc(l.n)}</h3><p>${esc(l.t)}</p><p style="border-left:3px solid var(--bad);padding-left:10px">${esc(l.k)}</p>
   <p class="note">S-C-A-L-P: Skin, Connective tissue, Aponeurosis, Loose areolar tissue, Pericranium.</p>`;
}

// ================= venous routes tab =================
const VN = {
  st: [80, 46, "Supratrochlear v.", "supratrochlear_v"], so: [230, 46, "Supraorbital v.", "supraorbital_v"],
  ang: [150, 130, "Angular v.", "angular_v"], sov: [370, 130, "Sup. ophthalmic v.", "sup_ophthalmic_v"], cs: [620, 130, "Cavernous sinus", "cavernous_sinus"],
  fv: [150, 250, "Facial v.", "facial_v"], dfv: [370, 250, "Deep facial v.", "deep_facial_v"], pp: [620, 250, "Pterygoid plexus", "pterygoid_plexus"],
  mxv: [620, 340, "Maxillary v.", "maxillary_v"], stv: [760, 340, "Sup. temporal v.", "stv"],
  cfv: [370, 430, "Common facial v.", "common_facial_v"], rmv: [690, 430, "Retromandibular v.", "rmv"], pav: [840, 430, "Post. auricular v.", "post_auricular_v"],
  ijv: [370, 520, "Internal jugular v.", "ijv"], ejv: [760, 520, "External jugular v.", "ejv"],
  scalp: [840, 46, "Scalp veins", null], sss: [620, 46, "Dural venous sinuses", "emissary_v"]
};
const VE = [
  ["st", "ang"], ["so", "ang"], ["ang", "fv"], ["ang", "sov", "", "danger"], ["sov", "cs", "", "danger"], ["fv", "dfv", "", "danger"], ["dfv", "pp", "", "danger"],
  ["pp", "cs", "emissary veins (foramen ovale, Vesalius)", "danger"], ["pp", "mxv"], ["mxv", "rmv"], ["stv", "rmv"], ["fv", "cfv"], ["rmv", "cfv", "anterior division"],
  ["rmv", "ejv", "posterior division"], ["pav", "ejv"], ["cfv", "ijv"], ["scalp", "sss", "", "danger"], ["so", "stv", "scalp network"]
];
const VROUTES = {
  normal: { n: "Normal drainage of the face", seq: [["st", "ang"], ["so", "ang"], ["ang", "fv"], ["fv", "cfv"], ["stv", "rmv"], ["pp", "mxv"], ["mxv", "rmv"], ["rmv", "cfv"], ["rmv", "ejv"], ["pav", "ejv"], ["cfv", "ijv"]], t: "Superficial face → angular → facial vein → common facial → IJV. Side of scalp and deep face → superficial temporal + maxillary → retromandibular, which splits: anterior division joins the facial vein, posterior division joins the posterior auricular to form the EJV → subclavian vein." },
  danger1: { n: "Danger triangle → cavernous sinus (via orbit)", seq: [["ang", "fv"], ["ang", "sov"], ["sov", "cs"]], t: "A squeezed boil on the upper lip or nose: flow reverses, against the normal arrows, and infected thrombus passes up the valveless facial vein to the angular vein, into the superior ophthalmic vein, through the superior orbital fissure into the cavernous sinus. Signs: fever, proptosis, chemosis, ptosis, ophthalmoplegia (CN III, IV, VI), V1/V2 numbness. Can spread to the other eye." },
  danger2: { n: "Deep route via pterygoid plexus", seq: [["fv", "dfv"], ["dfv", "pp"], ["pp", "cs"]], t: "Infection of the cheek, upper molars or a needle-track: facial vein → deep facial vein → pterygoid plexus → emissary veins through foramen ovale and the sphenoidal emissary foramen (of Vesalius) → cavernous sinus." },
  scalp: { n: "Scalp infection → dural sinus", seq: [["scalp", "sss"]], t: "Infection in the loose areolar tissue (layer L) spreads along emissary veins (parietal, mastoid) to the superior sagittal and sigmoid sinuses: venous sinus thrombosis, meningitis or abscess." }
};
let vSvg;
function buildVeins() {
  vSvg = sv("svg", { viewBox: "0 0 920 570", role: "img", "aria-label": "Venous drainage flow diagram" });
  const defs = sv("defs", {}, vSvg);
  [["arrV", "var(--vein)"], ["arrD", "var(--bad)"]].forEach(([id, c]) => { const m = sv("marker", { id, viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 11, markerHeight: 11, markerUnits: "userSpaceOnUse", orient: "auto" }, defs); sv("path", { d: "M0 0 L10 5 L0 10 Z", style: { fill: c } }, m); });
  const eg = sv("g", {}, vSvg), ng = sv("g", {}, vSvg);
  VE.forEach(([a, b, lab, kind]) => {
    const A = VN[a], B = VN[b];
    const dx = B[0] - A[0], dy = B[1] - A[1], len = Math.hypot(dx, dy);
    const ux = dx / len, uy = dy / len;
    const off = (n) => Math.abs(ux) > Math.abs(uy) * 2.2 ? 64 : 20;
    const x1 = A[0] + ux * off(), y1 = A[1] + uy * (Math.abs(uy) > .3 ? 20 : off()), x2 = B[0] - ux * off(), y2 = B[1] - uy * (Math.abs(uy) > .3 ? 22 : off());
    const p = sv("path", { d: `M${x1} ${y1} L${x2} ${y2}`, "data-e": a + ">" + b, "marker-end": kind === "danger" ? "url(#arrD)" : "url(#arrV)", style: { stroke: kind === "danger" ? "var(--bad)" : "var(--vein)", strokeWidth: 2.4, fill: "none", strokeDasharray: kind === "danger" ? "6 4" : null, opacity: .75 } }, eg);
    if (lab) sv("text", { x: (x1 + x2) / 2 + 6, y: (y1 + y2) / 2 - 6, text: lab, style: { fontSize: "11px", fill: "var(--muted)", fontFamily: "var(--f-body)" } }, eg);
  });
  for (const k in VN) {
    const [x, y, n, ref] = VN[k];
    const g = sv("g", { "data-n": k, style: { cursor: "pointer" }, tabindex: "0", role: "button", "aria-label": n }, ng);
    sv("rect", { x: x - 66, y: y - 18, width: 132, height: 36, rx: 18, class: "vb", style: { fill: k === "cs" || k === "sss" ? "var(--vein-dk)" : "var(--panel)", stroke: "var(--vein)", strokeWidth: 2 } }, g);
    sv("text", { x, y: y + 4.5, "text-anchor": "middle", text: n, style: { fontSize: "12.5px", fontWeight: 700, fontFamily: "var(--f-body)", fill: k === "cs" || k === "sss" ? "#FFFFFF" : "var(--ink)" } }, g);
    g.onclick = () => vInfo(k);
    g.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); vInfo(k); } };
  }
  sv("text", { x: 760, y: 560, "text-anchor": "middle", text: "→ subclavian vein", style: { fontSize: "11px", fill: "var(--muted)", fontFamily: "var(--f-body)" } }, vSvg);
  sv("text", { x: 370, y: 560, "text-anchor": "middle", text: "→ brachiocephalic vein", style: { fontSize: "11px", fill: "var(--muted)", fontFamily: "var(--f-body)" } }, vSvg);
  $("#vdiagram").appendChild(vSvg);
  const box = $("#vroutes");
  for (const k in VROUTES) { const b = h("button", { class: "btn" + (k === "normal" ? "" : ""), "data-r": k }, (k === "normal" ? "▶ " : "⚠ ") + esc(VROUTES[k].n)); b.onclick = () => playRoute(k); box.appendChild(b); }
  vInfo("cs");
}
let routeTimers = [];
function playRoute(k) {
  routeTimers.forEach(clearTimeout); routeTimers = [];
  const r = VROUTES[k];
  $$("#vroutes .btn").forEach(b => b.classList.toggle("on", b.dataset.r === k));
  $$("path[data-e]", vSvg).forEach(p => { p.style.opacity = .15; p.style.strokeWidth = 2.4; });
  $$("[data-n] .vb", vSvg).forEach(b => b.style.strokeWidth = 2);
  $("#vout").innerHTML = `<h3>${esc(r.n)}</h3><p>${esc(r.t)}</p>`;
  r.seq.forEach(([a, b], i) => routeTimers.push(setTimeout(() => {
    let p = vSvg.querySelector(`path[data-e="${a}>${b}"]`) || vSvg.querySelector(`path[data-e="${b}>${a}"]`);
    if (p) { p.style.opacity = 1; p.style.strokeWidth = 5; }
    [a, b].forEach(n => { const bx = vSvg.querySelector(`[data-n="${n}"] .vb`); if (bx) bx.style.strokeWidth = 4.5; });
  }, reduceMotion ? 0 : i * 650)));
}
function vInfo(k) {
  const [, , n, ref] = VN[k];
  const o = ref && S[ref];
  const extra = { scalp: "Veins of the scalp run in layer C with the arteries and drain to the facial, superficial temporal, posterior auricular and occipital veins. They connect inward through emissary and diploic veins.", sss: "Dural venous sinuses receive emissary veins from the scalp (parietal emissary to the superior sagittal sinus; mastoid emissary to the sigmoid sinus)." };
  $("#vout").innerHTML = `<h3>${esc(n)}</h3><p>${esc(o ? o.sum : extra[k])}</p>${o && o.f && o.f.k ? `<p style="border-left:3px solid var(--bad);padding-left:10px">${esc(o.f.k)}</p>` : ""}${o ? `<button class="btn primary" data-open="${ref}">Trace it on the atlas</button>` : ""}`;
  const b = $("[data-open]", $("#vout")); if (b) b.onclick = () => { showTab("explore"); select(ref, { trace: !!S[ref].steps }); };
}

// ================= muscles tab =================
function buildMuscles() {
  const box = $("#mgrid");
  const groups = [["Scalp", "Scalp (epicranius)"], ["Orbit", "Around the eye"], ["Nose", "Around the nose"], ["Mouth", "Around the mouth"], ["Ear", "Around the ear"], ["Neck", "Neck"]];
  let html = "";
  for (const [g, title] of groups) {
    const ids = Object.keys(S).filter(k => S[k].sys === "muscle" && S[k].grp === g);
    html += `<div class="grp-h">${esc(title)}</div><div class="mgrid">` + ids.map(k => {
      const o = S[k], f = o.f || {};
      return `<div class="mcard"><h4>${esc(o.n)}</h4><span class="br">CN VII: ${esc(o.br)}</span>
       ${f.o ? `<div class="row"><b>Origin</b>${esc(f.o)}</div>` : ""}${f.i ? `<div class="row"><b>Insertion</b>${esc(f.i)}</div>` : ""}
       ${f.a ? `<div class="row"><b>Action</b>${esc(f.a)}</div>` : ""}${f.t ? `<div class="row"><b>Test</b>${esc(f.t)}</div>` : ""}
       <button class="btn" data-m="${k}">Show on plate</button></div>`;
    }).join("") + `</div>`;
  }
  html += `<div class="card" style="margin-top:18px"><h3>Bedside examination of the facial nerve (motor)</h3>
   <div class="tablewrap"><table><thead><tr><th>Ask the patient to…</th><th>Muscle</th><th>Branch</th></tr></thead><tbody>
   <tr><td>Raise the eyebrows</td><td>Frontalis</td><td>Temporal</td></tr>
   <tr><td>Screw the eyes shut (try to open them)</td><td>Orbicularis oculi</td><td>Temporal + zygomatic</td></tr>
   <tr><td>Frown</td><td>Corrugator supercilii</td><td>Temporal</td></tr>
   <tr><td>Wrinkle the nose / flare nostrils</td><td>Procerus, nasalis, LLSAN</td><td>Buccal</td></tr>
   <tr><td>Puff out the cheeks</td><td>Buccinator, orbicularis oris</td><td>Buccal</td></tr>
   <tr><td>Show the teeth / smile</td><td>Zygomaticus major & minor, levators, risorius</td><td>Zygomatic + buccal</td></tr>
   <tr><td>Pull the mouth down / show lower teeth</td><td>Depressors, mentalis</td><td>Marginal mandibular</td></tr>
   <tr><td>Grimace, tense the neck</td><td>Platysma</td><td>Cervical</td></tr></tbody></table></div></div>`;
  box.innerHTML = html;
  $$("[data-m]", box).forEach(b => b.onclick = () => { showTab("explore"); setView("ant"); select(b.dataset.m); window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }); });
}

// ================= quiz tab =================
const MCQ = [
  ["A 72-year-old has a new headache, jaw pain on chewing and a tender, thickened, pulseless artery in front of the tragus. Which artery is biopsied?", ["Facial artery", "Superficial temporal artery", "Occipital artery", "Posterior auricular artery"], 1, "Giant cell (temporal) arteritis. The STA crosses the posterior root of the zygomatic arch in front of the tragus, where it is biopsied. Start steroids promptly to protect vision."],
  ["Where do you feel the facial artery pulse?", ["In front of the tragus", "At the medial canthus", "On the lower border of the mandible at the anterior border of masseter", "Below the angle of the mandible"], 2, "It hooks around the inferior border of the mandible at the anterior edge of masseter. Clench the teeth to find the edge."],
  ["Right facial weakness including the forehead. Taste, tears and hearing are normal; no hyperacusis. Where is the lesion?", ["Internal acoustic meatus", "Geniculate ganglion", "Between nerve to stapedius and chorda tympani", "At or distal to the stylomastoid foramen"], 3, "All intracranial branches (GSPN, stapedius, chorda) are intact, so the lesion lies after they leave: at the stylomastoid foramen or beyond."],
  ["After a stroke, the left lower face droops but the patient can wrinkle the forehead on both sides. Where is the lesion?", ["Left facial nucleus", "Right motor cortex / corticobulbar fibres", "Left stylomastoid foramen", "Right parotid gland"], 1, "UMN lesion: contralateral lower face weakness with forehead sparing, because the upper face motor neurons receive input from both hemispheres."],
  ["A patient squeezes a boil beside the nose. Days later there is proptosis, chemosis and a lateral gaze palsy. The route of spread was most likely…", ["Facial vein → EJV", "Angular vein → superior ophthalmic vein → cavernous sinus", "Retromandibular vein → IJV", "Occipital vein → suboccipital plexus"], 1, "The valveless facial–angular–ophthalmic route carries infection to the cavernous sinus. CN VI, free in the sinus beside the ICA, is often affected first."],
  ["Which nerve supplies the skin over the angle of the mandible?", ["Mandibular division (V3)", "Great auricular nerve (C2, C3)", "Buccal branch of facial nerve", "Lesser occipital nerve"], 1, "The angle is not trigeminal. Sensory loss that includes the angle should make you doubt a trigeminal lesion."],
  ["Which layer of the scalp is called the 'danger area'?", ["Dense connective tissue", "Galea aponeurotica", "Loose areolar tissue", "Pericranium"], 2, "Infection spreads freely in layer L and can pass through emissary veins to the dural venous sinuses."],
  ["Why do scalp lacerations bleed so much?", ["The scalp has no veins", "Vessels are held open by the dense connective tissue and cannot retract or constrict", "Platelets do not work in the scalp", "The arteries come only from the ICA"], 1, "Vessel walls are fixed to the fibrous septa of layer C. Firm pressure, or suturing including the galea, controls it."],
  ["Buccinator is supplied by…", ["Buccal nerve (V3)", "Buccal branch of the facial nerve", "Nerve to mylohyoid", "Hypoglossal nerve"], 1, "The buccal nerve of V3 only pierces buccinator to carry sensation from the cheek; motor supply is CN VII."],
  ["Inside the parotid gland, which order is correct from superficial to deep?", ["ECA → retromandibular vein → facial nerve", "Facial nerve → retromandibular vein → ECA", "Retromandibular vein → facial nerve → ECA", "Facial nerve → ECA → retromandibular vein"], 1, "Nerve, vein, artery from superficial to deep. The vein is the surgeon's landmark: the nerve lies just superficial to it."],
  ["Gustatory sweating over the cheek after parotidectomy (Frey syndrome) involves misdirected fibres in the…", ["Great auricular nerve", "Auriculotemporal nerve", "Chorda tympani", "Buccal branch of CN VII"], 1, "Parasympathetic fibres for the parotid (CN IX → otic ganglion) run in the auriculotemporal nerve and regrow into the sweat glands of the skin."],
  ["A blow to the forehead causes bruising that appears in both upper eyelids a day later. Why?", ["Fracture of the orbital roof", "Blood in the loose areolar layer tracks forward because frontalis attaches to skin, not bone", "Damage to the supraorbital artery inside the orbit", "Blood under the pericranium crosses sutures"], 1, "Layer L has no bony attachment anteriorly, so blood tracks into the eyelids. A subperiosteal bleed would stop at the sutures."],
  ["The facial vein ends by…", ["Joining the EJV directly", "Joining the anterior division of the retromandibular vein to form the common facial vein → IJV", "Draining into the subclavian vein", "Entering the pterygoid plexus"], 1, "Common facial vein → internal jugular vein near the level of the hyoid bone."],
  ["After a punch to the eye: numb cheek and upper lip, and double vision looking up. Which nerve is injured?", ["Supraorbital", "Infraorbital", "Zygomaticotemporal", "Mental"], 1, "Blow-out fracture of the orbital floor injures the infraorbital nerve in its canal and may trap inferior rectus."],
  ["Hyperacusis and loss of taste, but tear production is normal. The lesion is…", ["Proximal to the geniculate ganglion", "Between the geniculate ganglion and the nerve to stapedius", "Between stapedius and chorda tympani", "In the parotid"], 1, "GSPN (tears) leaves at the geniculate, so it is spared. Stapedius and chorda leave further down, so both are affected."],
  ["Which scalp arteries come from the internal carotid system?", ["Superficial temporal and occipital", "Supratrochlear and supraorbital", "Posterior auricular and occipital", "Transverse facial and supraorbital"], 1, "Both are branches of the ophthalmic artery. The other three scalp arteries are from the ECA."]
];
let mcqRight = 0, mcqDone = 0;
function buildMCQ() {
  const box = $("#mcq"); box.innerHTML = "";
  MCQ.forEach(([q, opts, ans, exp], qi) => {
    const c = h("div", { class: "qcard" }, `<b>${qi + 1}.</b> ${esc(q)}<div class="opts">${opts.map((o, i) => `<button data-i="${i}">${esc(o)}</button>`).join("")}</div>`);
    $$(".opts button", c).forEach(b => b.onclick = () => {
      if (c.dataset.done) return; c.dataset.done = 1; mcqDone++;
      const i = +b.dataset.i; if (i === ans) mcqRight++;
      $$(".opts button", c).forEach((x, k) => { if (k === ans) x.classList.add("right"); else if (k === i) x.classList.add("wrong"); });
      c.appendChild(h("div", { class: "exp" }, esc(exp)));
      $("#mcqscore").textContent = `${mcqRight} / ${mcqDone} correct`;
    });
    box.appendChild(c);
  });
}
let ordState = null;
function buildOrder() {
  const sel = $("#ordsel");
  ORDER_PATHS.forEach(k => sel.appendChild(h("option", { value: k }, esc(S[k].n))));
  sel.onchange = newOrder; $("#ordnew").onclick = newOrder;
  newOrder();
}
function newOrder() {
  const id = $("#ordsel").value, steps = S[id].steps.map((s, i) => ({ i, t: s[2] }));
  for (let i = steps.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [steps[i], steps[j]] = [steps[j], steps[i]]; }
  ordState = { id, picked: [], steps };
  const list = $("#ordlist"); list.innerHTML = ""; $("#ordres").textContent = "";
  steps.forEach(s => {
    const b = h("button", {}, `<span class="num"></span><span>${esc(s.t)}</span>`);
    b.onclick = () => {
      if (b.dataset.n) return;
      ordState.picked.push(s.i); b.dataset.n = ordState.picked.length;
      $(".num", b).textContent = ordState.picked.length;
      if (ordState.picked.length === steps.length) {
        let ok = 0;
        $$("button", list).forEach((x, k) => { const n = +x.dataset.n - 1, good = steps[k].i === n; if (good) ok++; x.classList.add(good ? "ok" : "no"); if (!good) $(".num", x).textContent = `${x.dataset.n}→${steps[k].i + 1}`; });
        $("#ordres").innerHTML = `${ok} of ${steps.length} in the right place. ${ok === steps.length ? "You can trace it." : "Red items show your position → the correct position."} <button class="btn" id="ordtrace">Watch it on the atlas</button>`;
        $("#ordtrace").onclick = () => { showTab("explore"); select(id, { trace: true }); };
      }
    };
    list.appendChild(b);
  });
}

// ================= plan tab =================
const PLAN = [
  ["08:00", "Orientation: bones, foramina, layers", ["Find the supraorbital, infraorbital and mental foramina on the plate; confirm they line up through the pupil", "Learn S-C-A-L-P and click every layer in the Scalp tab", "Palpate on yourself: zygomatic arch, angle of mandible, mastoid, anterior border of masseter (clench)"]],
  ["09:00", "Arteries", ["Recite the 8 ECA branches in order (Some Anatomists Like Freaking Out Poor Medical Students)", "Trace the facial artery: all 8 steps without looking", "Trace the superficial temporal artery; feel your own pulse in front of the tragus", "Learn the 3 parts of the maxillary artery and the branches of each", "Trace occipital and posterior auricular arteries; name the 5 scalp arteries and which come from the ICA"]],
  ["10:45", "Veins", ["Trace supratrochlear + supraorbital → angular → facial → common facial → IJV", "Trace the retromandibular vein and both divisions; form the EJV", "Play both danger routes in the Venous tab and explain cavernous sinus thrombosis", "Draw the venous flow chart from memory"]],
  ["13:00", "Facial nerve", ["Intracranial course: IAM → labyrinthine → geniculate → tympanic → mastoid → stylomastoid foramen", "Place the lesion at every station in the Facial nerve tab and predict the table before clicking", "Trace the extracranial trunk and the 5 branches (To Zanzibar By Motor Car)", "State the parotid relations: nerve → vein → artery"]],
  ["14:30", "Muscles of facial expression", ["Go through every muscle card; perform each bedside test in a mirror", "Switch the atlas to Anterior with skin at 0% and name each muscle", "Link each muscle to its CN VII branch"]],
  ["15:45", "Sensory supply", ["Turn on the sensory map; trace V1, V2, V3 boundaries in both views", "Trace infraorbital, supraorbital and auriculotemporal nerves", "Name the 4 nerves in front of the ear and the 4 behind for the scalp", "Remember: the angle of the mandible is C2/C3"]],
  ["17:00", "Integration", ["Run 'Quiz: find it' on the lateral view with all layers on until you score 20/25", "Do the course-ordering game for at least 6 pathways", "Answer all clinical questions"]],
  ["19:30", "Teach it back", ["Without notes, draw a lateral head and trace the facial artery, facial vein and facial nerve branches in three colours", "Explain to someone (or out loud) the danger triangle and the scalp danger area"]]
];
function buildPlan() {
  const done = store.get("plan", {});
  const box = $("#plan");
  PLAN.forEach(([t, title, items], bi) => {
    const b = h("div", { class: "block" }, `<div class="t">${t}</div><div><h4>${esc(title)}</h4>${items.map((it, ii) => { const id = `p${bi}-${ii}`; return `<label for="${id}"><input type="checkbox" id="${id}" ${done[id] ? "checked" : ""}> <span>${esc(it)}</span></label>`; }).join("")}</div>`);
    box.appendChild(b);
  });
  const upd = () => {
    const all = $$("#plan input"), n = all.filter(x => x.checked).length;
    $("#planbar").style.width = (100 * n / all.length) + "%";
    $("#planpct").textContent = `${n} of ${all.length} done`;
  };
  $$("#plan input").forEach(x => x.onchange = () => { const d = store.get("plan", {}); d[x.id] = x.checked; store.set("plan", d); upd(); });
  upd();
  const MN = [
    ["ECA branches", "Some Anatomists Like Freaking Out Poor Medical Students: Superior thyroid, Ascending pharyngeal, Lingual, Facial, Occipital, Posterior auricular, Maxillary, Superficial temporal."],
    ["Facial nerve branches", "To Zanzibar By Motor Car: Temporal, Zygomatic, Buccal, Marginal mandibular, Cervical."],
    ["Scalp layers", "SCALP: Skin, Connective tissue, Aponeurosis, Loose areolar tissue (danger), Pericranium."],
    ["Parotid, superficial → deep", "Nerve, Vein, Artery: facial nerve → retromandibular vein → external carotid artery."],
    ["Maxillary artery, 1st part", "DAM I AM: Deep auricular, Anterior tympanic, Middle meningeal, Inferior alveolar, Accessory Meningeal."],
    ["Cavernous sinus", "O TOM CAT: lateral wall Oculomotor, Trochlear, Ophthalmic, Maxillary; inside Carotid and Abducens (the T's are trochlear)."],
    ["Foramina in a line", "Supraorbital, infraorbital and mental foramina sit on one vertical line through the pupil: same line for nerve blocks of V1, V2, V3."],
    ["Artery vs vein on the face", "Artery: tortuous and in front. Vein: straight and behind. Both cross the mandible at the anterior border of masseter."],
    ["Scalp nerves", "Four in front of the ear (supratrochlear, supraorbital, zygomaticotemporal, auriculotemporal: V1, V1, V2, V3) and four behind (great auricular, lesser occipital, greater occipital, third occipital: C2–C3)."],
    ["Scalp arteries", "Two from the ICA in front (supratrochlear, supraorbital); three from the ECA (superficial temporal, posterior auricular, occipital)."],
    ["UMN vs LMN facial palsy", "UMN: lower face only, opposite side, forehead spared. LMN: whole half of the face, same side, forehead involved."],
    ["Facial nerve branch order in the bone", "Tears (GSPN) → Hearing dampening (stapedius) → Taste (chorda) → Face. A lesion loses everything after it."]
  ];
  $("#mnem").innerHTML = MN.map(([a, b]) => `<div><b>${esc(a)}</b>${esc(b)}</div>`).join("");
}

// ================= boot =================
initAtlas();
buildCN7();
buildScalp();
buildVeins();
buildMuscles();
buildMCQ();
buildOrder();
buildPlan();
