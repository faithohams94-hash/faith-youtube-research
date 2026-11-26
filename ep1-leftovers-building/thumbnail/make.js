// Episode 1 split-screen thumbnail: "$4 LUNCH vs. $2.4M OWNER".
// usage: node make.js <outDir>   -> thumbnail-a.png (as briefed) and thumbnail-b.png (with Marcus shocked in the window)
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { bust, PEOPLE, ICONS } = require("../cards-src/art");
const FONTS = path.join(__dirname, "../cards-src/fonts");
const out = path.resolve(process.argv[2] || ".");

// ---------------------------------------------------------------- props
const fork = `<svg viewBox="0 0 60 200"><rect x="26" y="70" width="10" height="130" rx="5" fill="#cfd4d8" stroke="#141414" stroke-width="4"/>
  ${[10, 22, 34, 46].map((x) => `<rect x="${x}" y="0" width="6" height="70" rx="3" fill="#cfd4d8" stroke="#141414" stroke-width="3"/>`).join("")}
  <rect x="6" y="56" width="50" height="22" rx="8" fill="#cfd4d8" stroke="#141414" stroke-width="4"/></svg>`;
const hand = (fill) => `<svg viewBox="0 0 120 120"><ellipse cx="60" cy="64" rx="46" ry="40" fill="${fill}" stroke="#141414" stroke-width="6"/>
  <path d="M30 48 q10 -14 22 -6 M50 42 q10 -14 22 -4 M70 44 q10 -12 20 0" fill="none" stroke="#141414" stroke-width="5" stroke-linecap="round"/></svg>`;
const keys = `<svg viewBox="0 0 220 200">
  <circle cx="70" cy="50" r="34" fill="none" stroke="#E3B341" stroke-width="12"/>
  <g transform="rotate(25 70 80)"><rect x="60" y="80" width="22" height="100" rx="6" fill="#f2c94c" stroke="#141414" stroke-width="5"/>
    <rect x="82" y="140" width="22" height="12" fill="#f2c94c" stroke="#141414" stroke-width="4"/><rect x="82" y="162" width="16" height="12" fill="#f2c94c" stroke="#141414" stroke-width="4"/></g>
  <g transform="rotate(-20 70 80)"><rect x="30" y="80" width="20" height="90" rx="6" fill="#d9dee3" stroke="#141414" stroke-width="5"/>
    <rect x="12" y="130" width="18" height="12" fill="#d9dee3" stroke="#141414" stroke-width="4"/></g>
  <circle cx="150" cy="60" r="16" fill="#E3B341" stroke="#141414" stroke-width="5"/></svg>`;
const container = `<svg viewBox="0 0 300 170">
  <rect x="20" y="40" width="260" height="120" rx="22" fill="rgba(255,255,255,.85)" stroke="#141414" stroke-width="8"/>
  <ellipse cx="100" cy="100" rx="58" ry="34" fill="#f7f4ea" stroke="#141414" stroke-width="5"/>
  <ellipse cx="190" cy="92" rx="48" ry="30" fill="#c9783e" stroke="#141414" stroke-width="5"/>
  <circle cx="232" cy="124" r="22" fill="#4f9a4a" stroke="#141414" stroke-width="5"/><circle cx="208" cy="132" r="16" fill="#62b35c" stroke="#141414" stroke-width="4"/>
  <rect x="10" y="22" width="280" height="30" rx="12" fill="#6fb3e0" stroke="#141414" stroke-width="8" transform="rotate(-8 40 40)"/></svg>`;
const steam = `<svg viewBox="0 0 120 160"><path d="M30 150 q-20 -30 0 -60 q20 -30 0 -80 M70 150 q-20 -30 0 -60 q20 -30 0 -80" fill="none" stroke="rgba(255,255,255,.75)" stroke-width="9" stroke-linecap="round"/></svg>`;

// glass tower: grid of windows catching gold light
function tower(x, w, h, cols, rows, tint) {
  let win = "";
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const lit = (r * 7 + c * 3) % 5 === 0;
    win += `<rect x="${x + 14 + c * ((w - 28) / cols)}" y="${720 - h + 18 + r * 46}" width="${(w - 28) / cols - 8}" height="36" fill="${lit ? "#ffe3a1" : tint}" stroke="#141414" stroke-width="3"/>`;
  }
  return `<rect x="${x}" y="${720 - h}" width="${w}" height="${h}" fill="#2c4a63" stroke="#141414" stroke-width="7"/>${win}`;
}

function page(variant) {
  const left = bust(PEOPLE.me_hood);
  const right = bust(PEOPLE.me_owner);
  const marcus = bust({ ...PEOPLE.marcus_shock, label: "" });
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Anton;src:url('file://${FONTS}/anton-latin-400-normal.woff2')}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1280px;height:720px;overflow:hidden;background:#000}
.stage{position:relative;width:1280px;height:720px;overflow:hidden}
.L{position:absolute;inset:0;clip-path:polygon(0 0,672px 0,612px 720px,0 720px);background:linear-gradient(#5d7486,#2b3a47)}
.R{position:absolute;inset:0;clip-path:polygon(672px 0,1280px 0,1280px 720px,612px 720px);background:linear-gradient(#ffcf6e 0%,#ff9e4a 55%,#f07a3a 100%)}
.divider{position:absolute;inset:0;pointer-events:none}
.abs{position:absolute}
.banner{position:absolute;left:0;right:0;top:0;height:150px;background:linear-gradient(rgba(10,14,12,.92),rgba(10,14,12,.78));display:flex;align-items:center;justify-content:center;gap:26px;
  border-bottom:6px solid #141414}
.t{font-family:Anton;font-size:108px;line-height:1;letter-spacing:2px;-webkit-text-stroke:10px #000;paint-order:stroke fill;text-shadow:0 7px 0 rgba(0,0,0,.55)}
.w{color:#fff}.y{color:#ffd400}.vs{font-family:Anton;font-size:60px;color:#fff;-webkit-text-stroke:7px #000;paint-order:stroke fill;transform:translateY(8px)}
</style></head><body><div class="stage">
  <!-- LEFT: the cubicle, cold fluorescent -->
  <div class="L">
    <div class="abs" style="left:40px;top:180px;width:300px;height:14px;background:#e8f4ff;box-shadow:0 0 40px 10px rgba(220,240,255,.7);border:4px solid #141414"></div>
    <div class="abs" style="left:-20px;top:250px;width:700px;height:300px;background:#7f8f9b;border:7px solid #141414"></div>
    <div class="abs" style="left:380px;top:300px;width:190px;height:140px;background:#1d2a33;border:7px solid #141414;border-radius:8px"></div>
    <div class="abs" style="left:395px;top:315px;width:160px;height:110px;background:#4b7ea8"></div>
    <div class="abs" style="left:0;top:560px;width:680px;height:160px;background:#a7865c;border-top:8px solid #141414"></div>
    <div class="abs" style="left:30px;top:228px;width:430px;">${left}</div>
    <div class="abs" style="left:365px;top:555px;width:250px">${container}</div>
    <div class="abs" style="left:440px;top:445px;width:95px;opacity:.9">${steam}</div>
    <div class="abs" style="left:285px;top:520px;width:46px;transform:rotate(28deg)">${fork}</div>
    <div class="abs" style="left:300px;top:600px;width:110px">${hand("#ecebe6")}</div>
  </div>
  <!-- RIGHT: the tower, golden hour -->
  <div class="R">
    <svg class="abs" style="left:0;top:0" width="1280" height="720">${tower(760, 240, 560, 4, 12, "#6fa6cf")}${tower(1010, 300, 610, 5, 13, "#87b8dc")}
      <rect x="600" y="650" width="700" height="80" fill="#c7b08a" stroke="#141414" stroke-width="7"/></svg>
    ${variant === "b" ? `<div class="abs" style="left:1080px;top:250px;width:150px;transform:rotate(4deg)">${marcus}</div>
      <div class="abs" style="left:1060px;top:236px;width:190px;height:190px;border:9px solid #141414;background:rgba(135,184,220,.25)"></div>` : ""}
    <div class="abs" style="left:770px;top:228px;width:430px">${right}</div>
    <div class="abs" style="left:1050px;top:330px;width:225px;transform:rotate(180deg)">${keys}</div>
    <div class="abs" style="left:1080px;top:500px;width:125px">${hand("#ecebe6")}</div>
  </div>
  <svg class="divider" width="1280" height="720"><polygon points="672,0 690,0 630,720 612,720" fill="#fff" stroke="#141414" stroke-width="6"/></svg>
  <div class="banner"><span class="t w">$4 LUNCH</span><span class="vs">vs.</span><span class="t y">$2.4M OWNER</span></div>
</div></body></html>`;
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  for (const v of ["a", "b"]) {
    const f = path.join(out, `thumb-${v}.html`);
    fs.writeFileSync(f, page(v));
    await p.goto("file://" + f);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, `thumbnail-${v}.png`) });
    fs.unlinkSync(f);
  }
  await b.close();
  console.log("done");
})();
