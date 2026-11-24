// Flat 2D webcomic character busts and icons for the Episode 1 info cards.
// Every character is drawn in SVG: bold black outlines, flat fills, oversized heads.

const INK = "#141414";
const SW = 6; // outline width

function hairCurlyBlack() {
  // the narrator's messy curly jet-black hair (matches brand/protagonist-reference.png)
  const curls = [
    [70, 118, 30], [84, 82, 32], [112, 58, 34], [148, 48, 36], [186, 56, 34], [216, 80, 32], [232, 116, 28],
    [100, 96, 26], [140, 86, 26], [178, 90, 26], [206, 104, 22], [80, 140, 20], [224, 142, 18],
  ];
  const fringe = [[104, 112, 18], [128, 104, 17], [158, 104, 18], [186, 110, 16]];
  return `<g fill="#151515" stroke="${INK}" stroke-width="4">
    ${curls.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}"/>`).join("")}
    ${fringe.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}"/>`).join("")}
  </g>
  <g fill="none" stroke="#3a3a3a" stroke-width="3" stroke-linecap="round">
    <path d="M100 70 q10 -10 22 -4"/><path d="M150 60 q12 -8 24 0"/><path d="M196 74 q10 -4 16 6"/></g>`;
}
function hairSlicked(color, gray) {
  return `<path d="M58 140 Q52 60 120 42 Q190 26 236 70 Q252 92 244 140 Q232 96 196 88 Q150 80 110 92 Q74 104 58 140 Z"
      fill="${color}" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>
    <path d="M100 66 Q150 46 214 70" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="5" stroke-linecap="round"/>
    ${gray ? `<path d="M60 128 Q60 112 70 104" stroke="#bdbdbd" stroke-width="9" fill="none" stroke-linecap="round"/>
              <path d="M242 128 Q242 112 232 104" stroke="#bdbdbd" stroke-width="9" fill="none" stroke-linecap="round"/>` : ""}`;
}
function hairPuff() {
  return `<circle cx="150" cy="38" r="62" fill="#2b1a12" stroke="${INK}" stroke-width="${SW}"/>
    ${[[110, 26], [150, 4], [190, 26], [126, 54], [176, 54]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="14" fill="none" stroke="#4a3022" stroke-width="3"/>`).join("")}
    <path d="M60 140 Q58 80 150 72 Q242 80 240 140 Q220 102 150 98 Q80 102 60 140 Z" fill="#2b1a12" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
}
function hairShoulderCurls() {
  const c = [[64, 120], [62, 160], [70, 198], [236, 120], [238, 160], [230, 198], [96, 70], [130, 54], [170, 54], [204, 70], [82, 92], [218, 92]];
  return `<g fill="#2b1a12" stroke="${INK}" stroke-width="4">${c.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="26"/>`).join("")}</g>`;
}
function hairBuzzWhite() {
  return `<path d="M62 132 Q60 58 150 50 Q240 58 238 132 Q226 92 150 86 Q74 92 62 132 Z" fill="#ececec" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
}
function hairBob() {
  return `<path d="M50 220 Q34 60 150 44 Q266 60 250 220 Q230 214 226 150 Q214 96 150 96 Q86 96 74 150 Q70 214 50 220 Z"
      fill="#121212" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
}
function hairShortBrown() {
  return `<path d="M62 132 Q58 54 150 46 Q242 54 238 132 Q222 90 186 92 Q160 74 130 92 Q82 90 62 132 Z" fill="#7a5233" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
}

function hairFade() {
  // Danny: short dark top, faded sides
  return `<path d="M66 128 Q62 62 150 54 Q238 62 234 128 Q222 98 150 94 Q78 98 66 128 Z" fill="#2a1d14" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>
    <path d="M60 150 Q60 126 72 116 M240 150 Q240 126 228 116" stroke="#6b5a4c" stroke-width="10" fill="none" stroke-linecap="round"/>`;
}
function hairGrayCurls() {
  const c = [[78, 108], [100, 80], [130, 64], [166, 62], [198, 76], [222, 102], [70, 140], [230, 138], [116, 90], [182, 90]];
  return `<g fill="#cfcfcf" stroke="${INK}" stroke-width="4">${c.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="24"/>`).join("")}</g>`;
}
function hairBaldGray() {
  return `<path d="M58 170 Q54 120 76 98 M242 170 Q246 120 224 98" stroke="#d6d6d6" stroke-width="18" fill="none" stroke-linecap="round"/>
    <path d="M58 170 Q54 120 76 98 M242 170 Q246 120 224 98" stroke="${INK}" stroke-width="3" fill="none" opacity=".35"/>`;
}
function hairPonytail() {
  return `<path d="M200 40 Q270 30 262 120 Q250 90 222 76 Z" fill="#e8c35a" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
    <path d="M60 140 Q56 60 150 52 Q244 60 240 140 Q226 98 150 94 Q74 98 60 140 Z" fill="#f0cd65" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>
    <circle cx="206" cy="58" r="10" fill="#e5484d" stroke="${INK}" stroke-width="4"/>`;
}
function hairShortGray() {
  return `<path d="M64 132 Q62 62 150 56 Q238 62 236 132 Q224 100 150 96 Q76 100 64 132 Z" fill="#d9d9d9" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>
    <g fill="#b0b0b0">${Array.from({ length: 22 }, (_, i) => `<circle cx="${84 + (i * 29) % 132}" cy="${70 + (i * 11) % 28}" r="3"/>`).join("")}</g>`;
}
function hairBraids() {
  const c = [];
  for (const x of [62, 74, 226, 238]) for (const y of [150, 180, 210, 240]) c.push([x, y]);
  return `<g fill="#1e1410" stroke="${INK}" stroke-width="3">${c.map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="11" ry="16"/>`).join("")}</g>`;
}

function eyes(kind, glasses) {
  const L = 112, R = 188, Y = 152;
  let e = "";
  if (kind === "shocked") {
    e = [L, R].map((x) => `<ellipse cx="${x}" cy="${Y}" rx="18" ry="20" fill="#fff" stroke="${INK}" stroke-width="4"/><circle cx="${x}" cy="${Y}" r="5" fill="${INK}"/>`).join("");
  } else if (kind === "kind" || kind === "sad") {
    e = [L, R].map((x) => `<ellipse cx="${x}" cy="${Y + 2}" rx="13" ry="15" fill="#fff" stroke="${INK}" stroke-width="4"/><circle cx="${x + 1}" cy="${Y + 4}" r="8" fill="#2a1a12"/><circle cx="${x + 4}" cy="${Y}" r="2.5" fill="#fff"/>`).join("");
  } else {
    // half-lidded: heavy upper lid covering the top of the eye
    e = [L, R].map((x) => `<ellipse cx="${x}" cy="${Y + 3}" rx="17" ry="14" fill="#fff" stroke="${INK}" stroke-width="4"/>
      <circle cx="${x + 2}" cy="${Y + 7}" r="8" fill="${INK}"/>
      <path d="M${x - 19} ${Y + 1} Q${x} ${Y - 7} ${x + 19} ${Y + 1} L${x + 19} ${Y - 14} L${x - 19} ${Y - 14} Z" fill="var(--skin)" stroke="none"/>
      <path d="M${x - 19} ${Y + 1} Q${x} ${Y - 7} ${x + 19} ${Y + 1}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`).join("");
  }
  let brows = "";
  const bw = 7;
  if (kind === "worried" || kind === "sad" || kind === "shocked")
    brows = `<path d="M${L - 20} ${Y - 26} L${L + 16} ${Y - 36}" stroke="${INK}" stroke-width="${bw}" stroke-linecap="round"/><path d="M${R - 16} ${Y - 36} L${R + 20} ${Y - 26}" stroke="${INK}" stroke-width="${bw}" stroke-linecap="round"/>`;
  else if (kind === "smug")
    brows = `<path d="M${L - 20} ${Y - 30} Q${L} ${Y - 40} ${L + 18} ${Y - 30}" fill="none" stroke="${INK}" stroke-width="${bw}" stroke-linecap="round"/><path d="M${R - 18} ${Y - 38} Q${R} ${Y - 46} ${R + 20} ${Y - 36}" fill="none" stroke="${INK}" stroke-width="${bw}" stroke-linecap="round"/>`;
  else
    brows = `<path d="M${L - 22} ${Y - 28} L${L + 18} ${Y - 31}" stroke="${INK}" stroke-width="${bw + 1}" stroke-linecap="round"/><path d="M${R - 18} ${Y - 31} L${R + 22} ${Y - 28}" stroke="${INK}" stroke-width="${bw + 1}" stroke-linecap="round"/>`;
  const g = glasses
    ? `<g fill="rgba(255,255,255,.08)" stroke="${INK}" stroke-width="8" stroke-linejoin="round">
        <rect x="${L - 32}" y="${Y - 20}" width="64" height="44" rx="6"/><rect x="${R - 32}" y="${Y - 20}" width="64" height="44" rx="6"/></g>
       <path d="M${L + 32} ${Y - 4} L${R - 32} ${Y - 4}" stroke="${INK}" stroke-width="7"/>
       <path d="M${L - 32} ${Y - 6} L${L - 52} ${Y - 10}" stroke="${INK}" stroke-width="7"/><path d="M${R + 32} ${Y - 6} L${R + 52} ${Y - 10}" stroke="${INK}" stroke-width="7"/>`
    : "";
  return brows + e + g;
}
function mouth(kind) {
  const y = 214;
  switch (kind) {
    case "halfsmile": return `<path d="M132 ${y} Q152 ${y + 6} 170 ${y - 4}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    case "smug": return `<path d="M124 ${y - 4} Q156 ${y + 18} 184 ${y - 10}" fill="#fff" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M128 ${y - 1} L182 ${y - 7}" stroke="${INK}" stroke-width="3"/>`;
    case "worried": return `<path d="M128 ${y + 4} q8 -8 16 0 q8 8 16 0 q8 -8 16 0" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    case "shocked": return `<ellipse cx="152" cy="${y + 2}" rx="13" ry="17" fill="#3a1010" stroke="${INK}" stroke-width="5"/>`;
    case "kind": return `<path d="M136 ${y - 2} Q152 ${y + 10} 168 ${y - 2}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    case "sad": return `<path d="M136 ${y + 6} Q152 ${y - 4} 168 ${y + 6}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    default: return `<path d="M136 ${y} L168 ${y}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
  }
}
function outfit(kind, extra = {}) {
  const body = (fill) => `<path d="M14 380 Q22 284 150 266 Q278 284 286 380 Z" fill="${fill}" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
  switch (kind) {
    case "hoodie": return `<path d="M70 300 Q64 246 104 244 L196 244 Q236 246 230 300 Z" fill="#262626" stroke="${INK}" stroke-width="${SW}"/>${body("#1c1c1c")}
      <path d="M128 286 L132 350 M172 286 L168 350" stroke="#444" stroke-width="5"/>`;
    case "crewneck": return `${body("#1d1d1d")}<path d="M118 268 L150 300 L182 268" fill="#f3f3f3" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      ${extra.lanyard ? `<path d="M120 276 L146 340 M180 276 L154 340" stroke="#2f6fb5" stroke-width="6"/><rect x="134" y="336" width="32" height="40" rx="4" fill="#fff" stroke="${INK}" stroke-width="4"/>` : ""}`;
    case "jacket": return `${body("#33373a")}<path d="M120 268 L150 380 L180 268 Z" fill="#111" stroke="${INK}" stroke-width="4"/>
      <path d="M116 268 L138 330 L104 300 Z M184 268 L162 330 L196 300 Z" fill="#2a2d30" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
    case "shirt_tie": return `${body("#a9c8ea")}<path d="M124 266 L150 290 L176 266" fill="#cfe1f5" stroke="${INK}" stroke-width="4"/>
      <path d="M142 290 L158 290 L164 372 L150 384 L136 372 Z" fill="#1f2f55" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
      ${extra.santa ? "" : ""}`;
    case "suit_tie": return `${body("#3b3f45")}<path d="M120 268 L150 300 L180 268 L172 380 L128 380 Z" fill="#e9eef5" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M144 296 L156 296 L162 372 L150 382 L138 372 Z" fill="#1f2f55" stroke="${INK}" stroke-width="4" transform="rotate(8 150 330)"/>
      <path d="M118 268 L140 340 L100 304 Z M182 268 L160 340 L200 304 Z" fill="#33373c" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
      ${extra.sweat ? `<path d="M126 270 Q150 286 174 270" fill="none" stroke="#5a6b80" stroke-width="5"/>` : ""}`;
    case "blazer_burgundy": return `${body("#7a2234")}<path d="M124 268 L150 310 L176 268" fill="#f1e6e2" stroke="${INK}" stroke-width="4"/>
      ${extra.lanyard ? `<path d="M122 274 L146 342 M178 274 L154 342" stroke="#E3B341" stroke-width="5"/><rect x="132" y="338" width="36" height="40" rx="4" fill="#fff" stroke="${INK}" stroke-width="4"/>` : ""}`;
    case "blazer_gray": return `${body("#8b8f94")}<path d="M124 268 L150 312 L176 268" fill="#f4f4f4" stroke="${INK}" stroke-width="4"/>`;
    case "flannel": return `${body("#c9a76a")}<path d="M118 268 L150 380 L182 268 Z" fill="#b8423a" stroke="${INK}" stroke-width="4"/>
      <path d="M134 290 L166 290 M128 320 L172 320 M124 350 L176 350 M140 276 L140 380 M160 276 L160 380" stroke="#7d2a24" stroke-width="3"/>`;
    case "polo": return `${body("#1f8a8a")}<path d="M128 266 L150 300 L172 266" fill="#176b6b" stroke="${INK}" stroke-width="4"/>
      <path d="M140 300 L140 330 M160 300 L160 330" stroke="#fff" stroke-width="5"/><rect x="196" y="300" width="40" height="24" rx="4" fill="#E3B341" stroke="${INK}" stroke-width="3"/>`;
    case "cardigan": return `${body("#7a2c3a")}<path d="M124 268 L150 380 L176 268 Z" fill="#efe4d0" stroke="${INK}" stroke-width="4"/>
      ${[300, 330, 360].map((y) => `<circle cx="168" cy="${y}" r="5" fill="#E3B341" stroke="${INK}" stroke-width="2"/>`).join("")}`;
    case "workshirt": return `${body("#2f4a6b")}<path d="M124 266 L150 296 L176 266" fill="#3c5c82" stroke="${INK}" stroke-width="4"/>
      <rect x="182" y="300" width="58" height="26" rx="5" fill="#fff" stroke="${INK}" stroke-width="3"/><text x="211" y="319" font-family="Arial" font-weight="700" font-size="16" text-anchor="middle" fill="#2f4a6b">RAY</text>`;
    case "top_pink": return `${body("#e98bb0")}<path d="M120 268 Q150 300 180 268" fill="none" stroke="${INK}" stroke-width="4"/>`;
    case "suit_navy": return `${body("#1f2f55")}<path d="M124 268 L150 314 L176 268" fill="#f4f4f4" stroke="${INK}" stroke-width="4"/>
      <path d="M118 268 L140 340 L100 304 Z M182 268 L160 340 L200 304 Z" fill="#18264a" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
    case "scrubs": return `${body("#4fa3b8")}<path d="M124 266 L150 312 L176 266" fill="#3d8aa0" stroke="${INK}" stroke-width="4"/>`;
    case "worn_jacket": return `${body("#5b6146")}<path d="M150 270 L150 380" stroke="${INK}" stroke-width="4"/><path d="M126 268 L150 296 L174 268" fill="#2c2c2c" stroke="${INK}" stroke-width="4"/>
      <path d="M40 350 q14 -10 28 0 M232 350 q14 -10 28 0" stroke="#7a805f" stroke-width="5" fill="none"/>`;
    case "hoodie_red": return `<path d="M70 300 Q64 246 104 244 L196 244 Q236 246 230 300 Z" fill="#a8282b" stroke="${INK}" stroke-width="${SW}"/>${body("#c0302f")}`;
    case "suit_gray": return `${body("#b7bcc2")}<path d="M124 268 L150 300 L176 268" fill="#fff" stroke="${INK}" stroke-width="4"/>`;
    default: return body("#444");
  }
}

const SKIN = { pale: "#ecebe6", light: "#f1d2b6", tan: "#e3b48c", brown: "#8d5a3b", warm: "#e8c4a0" };

// person = { hair, skin, glasses, outfit, outfitExtra, expr, mouth, extras }
function bust(p) {
  const skin = SKIN[p.skin] || p.skin;
  const hair = { curly: hairCurlyBlack, slicked: () => hairSlicked("#5a3a22", false), slickedGray: () => hairSlicked("#5a3a22", true),
    puff: hairPuff, shoulder: hairShoulderCurls, buzz: hairBuzzWhite, bob: hairBob, short: hairShortBrown,
    fade: hairFade, grayCurls: hairGrayCurls, baldGray: hairBaldGray, ponytail: hairPonytail, shortGray: hairShortGray, braids: hairBraids }[p.hair]();
  const backHair = p.hair === "shoulder" ? hair : p.hair === "bob" ? hair : p.hair === "braids" ? hair : "";
  const frontHair = p.hair === "shoulder"
    ? `<path d="M68 132 Q66 70 150 64 Q234 70 232 132 Q212 96 150 94 Q88 96 68 132 Z" fill="#2b1a12" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`
    : p.hair === "bob"
    ? `<path d="M58 140 Q56 58 150 52 Q244 58 242 140 Q232 104 196 100 L178 120 L170 100 Q150 98 104 100 Q70 104 58 140 Z" fill="#121212" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`
    : p.hair === "braids"
    ? `<path d="M64 136 Q62 62 150 56 Q238 62 236 136 Q222 98 150 94 Q78 98 64 136 Z" fill="#1e1410" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`
    : hair;
  const ex = p.extras || {};
  return `<svg viewBox="0 0 300 380" xmlns="http://www.w3.org/2000/svg" style="--skin:${skin}">
    ${backHair}
    ${outfit(p.outfit, p.outfitExtra || {})}
    <rect x="124" y="226" width="52" height="50" fill="${skin}" stroke="${INK}" stroke-width="${SW}"/>
    <ellipse cx="58" cy="158" rx="16" ry="22" fill="${skin}" stroke="${INK}" stroke-width="${SW}"/>
    <ellipse cx="242" cy="158" rx="16" ry="22" fill="${skin}" stroke="${INK}" stroke-width="${SW}"/>
    <ellipse cx="150" cy="150" rx="94" ry="98" fill="${skin}" stroke="${INK}" stroke-width="${SW}"/>
    ${ex.earrings ? `<circle cx="56" cy="186" r="9" fill="none" stroke="#E3B341" stroke-width="5"/><circle cx="244" cy="186" r="9" fill="none" stroke="#E3B341" stroke-width="5"/>` : ""}
    ${ex.stubble ? `<g fill="#bdbdbd">${Array.from({ length: 40 }, (_, i) => `<circle cx="${96 + (i * 37) % 110}" cy="${198 + (i * 13) % 40}" r="2.2"/>`).join("")}</g>` : ""}
    ${frontHair}
    ${eyes(p.expr, p.glasses)}
    <path d="M150 168 Q144 188 156 192" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>
    ${mouth(p.mouth || p.expr)}
    ${ex.sweat ? `<path d="M236 112 q10 18 0 26 q-10 -8 0 -26 Z" fill="#9fd3ff" stroke="${INK}" stroke-width="3"/><path d="M70 128 q8 14 0 20 q-8 -6 0 -20 Z" fill="#9fd3ff" stroke="${INK}" stroke-width="3"/>` : ""}
    ${ex.pencil ? `<path d="M226 104 L262 84" stroke="#E3B341" stroke-width="10" stroke-linecap="round"/><path d="M262 84 L272 79" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>` : ""}
    ${ex.santa ? `<path d="M64 92 Q150 -40 238 92 Z" fill="#c62828" stroke="${INK}" stroke-width="${SW}"/><rect x="56" y="80" width="190" height="26" rx="13" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="236" cy="0" r="0"/><circle cx="96" cy="18" r="16" fill="#fff" stroke="${INK}" stroke-width="5"/>` : ""}
    ${ex.goatee ? `<path d="M132 226 Q150 250 168 226 Q160 238 150 238 Q140 238 132 226 Z" fill="#2a1d14" stroke="${INK}" stroke-width="4"/>` : ""}
    ${ex.mustache ? `<path d="M118 200 Q150 186 182 200 Q166 210 150 204 Q134 210 118 200 Z" fill="#d6d6d6" stroke="${INK}" stroke-width="4"/>` : ""}
    ${ex.chain ? `<path d="M98 160 Q80 230 120 262 M202 160 Q220 230 180 262" fill="none" stroke="#E3B341" stroke-width="3" stroke-dasharray="4 4"/>` : ""}
    ${ex.blush ? `<ellipse cx="96" cy="190" rx="14" ry="7" fill="rgba(229,72,77,.35)"/><ellipse cx="204" cy="190" rx="14" ry="7" fill="rgba(229,72,77,.35)"/>` : ""}
  </svg>`;
}

const PEOPLE = {
  me_now: { label: "YOU", hair: "curly", skin: "pale", glasses: true, outfit: "worn_jacket", expr: "calm", mouth: "flat" },
  me_now_calm: { label: "YOU", hair: "curly", skin: "pale", glasses: true, outfit: "worn_jacket", expr: "calm", mouth: "halfsmile" },
  me_sad: { label: "YOU", hair: "curly", skin: "pale", glasses: true, outfit: "hoodie", expr: "sad" },
  danny: { label: "DANNY", hair: "fade", skin: "tan", glasses: false, outfit: "polo", expr: "smug", extras: { goatee: true } },
  danny_worried: { label: "DANNY", hair: "fade", skin: "tan", glasses: false, outfit: "polo", expr: "worried", extras: { goatee: true, sweat: true } },
  danny_shock: { label: "DANNY", hair: "fade", skin: "tan", glasses: false, outfit: "polo", expr: "shocked", extras: { goatee: true } },
  mom: { label: "MOM", hair: "grayCurls", skin: "tan", glasses: false, outfit: "cardigan", expr: "kind" },
  mom_sad: { label: "MOM", hair: "grayCurls", skin: "tan", glasses: false, outfit: "cardigan", expr: "sad" },
  dad: { label: "DAD", hair: "baldGray", skin: "tan", glasses: false, outfit: "workshirt", expr: "calm", mouth: "flat", extras: { mustache: true } },
  dad_sad: { label: "DAD", hair: "baldGray", skin: "tan", glasses: false, outfit: "workshirt", expr: "sad", extras: { mustache: true } },
  kayla: { label: "KAYLA", hair: "ponytail", skin: "light", glasses: false, outfit: "top_pink", expr: "smug", mouth: "kind" },
  okafor: { label: "MS. OKAFOR", hair: "shortGray", skin: "brown", glasses: true, outfit: "suit_navy", expr: "calm", mouth: "flat", extras: { chain: true } },
  gloria: { label: "GLORIA", hair: "braids", skin: "brown", glasses: false, outfit: "scrubs", expr: "kind" },
  nephew: { label: "NEPHEW", hair: "short", skin: "tan", glasses: false, outfit: "hoodie_red", expr: "kind" },
  me_owner: { label: "YOU", hair: "curly", skin: "pale", glasses: true, outfit: "jacket", expr: "calm", mouth: "halfsmile" },
  me_past: { label: "YOU", hair: "curly", skin: "pale", glasses: true, outfit: "crewneck", outfitExtra: { lanyard: true }, expr: "calm", mouth: "flat" },
  me_home: { label: "YOU", hair: "curly", skin: "pale", glasses: true, outfit: "hoodie", expr: "calm", mouth: "flat" },
  marcus_past: { label: "MARCUS", hair: "slicked", skin: "light", glasses: false, outfit: "shirt_tie", expr: "smug" },
  marcus_broke: { label: "MARCUS", hair: "slicked", skin: "light", glasses: false, outfit: "shirt_tie", expr: "worried", extras: { sweat: true } },
  marcus_santa: { label: "MARCUS", hair: "slicked", skin: "light", glasses: false, outfit: "shirt_tie", expr: "smug", extras: { santa: true } },
  marcus_now: { label: "MARCUS", hair: "slickedGray", skin: "light", glasses: false, outfit: "suit_tie", outfitExtra: { sweat: true }, expr: "worried", extras: { sweat: true } },
  marcus_shock: { label: "MARCUS", hair: "slickedGray", skin: "light", glasses: false, outfit: "suit_tie", outfitExtra: { sweat: true }, expr: "shocked", extras: { sweat: true } },
  dana_now: { label: "DANA", hair: "shoulder", skin: "brown", glasses: false, outfit: "blazer_burgundy", outfitExtra: { lanyard: true }, expr: "sad", extras: { earrings: true } },
  pm: { label: "PROPERTY MANAGER", hair: "bob", skin: "tan", glasses: false, outfit: "blazer_gray", expr: "calm", mouth: "kind" },
  arthur: { label: "ARTHUR", hair: "buzz", skin: "warm", glasses: false, outfit: "flannel", expr: "calm", mouth: "kind", extras: { stubble: true, pencil: true } },
  arthur_worried: { label: "ARTHUR", hair: "buzz", skin: "warm", glasses: false, outfit: "flannel", expr: "worried", extras: { stubble: true, pencil: true } },
  staffer: { label: "STAFFER", hair: "short", skin: "light", glasses: false, outfit: "suit_gray", expr: "shocked" },
};

// ---------------------------------------------------------------- icons (100x100)
const I = (inner, vb = "0 0 100 100") => `<svg viewBox="${vb}" xmlns="http://www.w3.org/2000/svg">${inner}</svg>`;
const ICONS = {
  container: I(`<rect x="10" y="34" width="80" height="50" rx="10" fill="#fdfdfd" stroke="${INK}" stroke-width="5"/><rect x="6" y="24" width="88" height="14" rx="6" fill="#6fb3e0" stroke="${INK}" stroke-width="5"/>
    <ellipse cx="34" cy="60" rx="16" ry="11" fill="#f4f1e6" stroke="${INK}" stroke-width="3"/><ellipse cx="62" cy="58" rx="14" ry="10" fill="#c9783e" stroke="${INK}" stroke-width="3"/><circle cx="74" cy="70" r="8" fill="#4f9a4a" stroke="${INK}" stroke-width="3"/>`),
  salad: I(`<path d="M10 46 Q50 100 90 46 Z" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="34" cy="40" r="12" fill="#62b35c" stroke="${INK}" stroke-width="3"/><circle cx="52" cy="34" r="12" fill="#8ccf63" stroke="${INK}" stroke-width="3"/><circle cx="68" cy="42" r="10" fill="#e5484d" stroke="${INK}" stroke-width="3"/>`),
  coffee: I(`<path d="M24 26 L76 26 L68 92 L32 92 Z" fill="#fff" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><rect x="20" y="16" width="60" height="14" rx="4" fill="#5c3b22" stroke="${INK}" stroke-width="5"/><rect x="28" y="48" width="44" height="18" fill="#c9a76a"/>`),
  highrise: I(`<rect x="28" y="8" width="44" height="86" fill="#9fb6c9" stroke="${INK}" stroke-width="5"/>${[18, 32, 46, 60, 74].map((y) => `<rect x="36" y="${y}" width="10" height="8" fill="#ffe08a"/><rect x="54" y="${y}" width="10" height="8" fill="#ffe08a"/>`).join("")}`),
  car: (c) => I(`<path d="M8 66 L16 44 Q20 36 30 36 L70 36 Q80 36 84 44 L92 66 Z" fill="${c}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><rect x="6" y="60" width="88" height="20" rx="6" fill="${c}" stroke="${INK}" stroke-width="5"/>
    <path d="M28 42 L72 42 L78 56 L22 56 Z" fill="#cfe7f7" stroke="${INK}" stroke-width="3"/><circle cx="26" cy="82" r="10" fill="#222" stroke="${INK}" stroke-width="4"/><circle cx="74" cy="82" r="10" fill="#222" stroke="${INK}" stroke-width="4"/>`),
  cocktail: I(`<path d="M18 16 L82 16 L50 54 Z" fill="#e66fa3" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M50 54 L50 86 M32 88 L68 88" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><circle cx="70" cy="18" r="8" fill="#9ccc65" stroke="${INK}" stroke-width="3"/>`),
  studio: I(`<path d="M12 48 L50 16 L88 48" fill="none" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><rect x="20" y="44" width="60" height="46" fill="#d9c7a6" stroke="${INK}" stroke-width="5"/><rect x="42" y="62" width="16" height="28" fill="#7a5233" stroke="${INK}" stroke-width="3"/>`),
  lunchbox: I(`<rect x="10" y="34" width="80" height="54" rx="10" fill="#2f86e8" stroke="${INK}" stroke-width="5"/><path d="M34 34 Q34 14 50 14 Q66 14 66 34" fill="none" stroke="${INK}" stroke-width="6"/><rect x="58" y="48" width="26" height="16" rx="3" fill="#fff" stroke="${INK}" stroke-width="3" transform="rotate(-12 70 56)"/>`),
  watch: I(`<rect x="38" y="4" width="24" height="92" rx="6" fill="#d4a62a" stroke="${INK}" stroke-width="5"/><circle cx="50" cy="50" r="26" fill="#f6e3a1" stroke="${INK}" stroke-width="6"/><path d="M50 50 L50 34 M50 50 L62 56" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`),
  unit: (lit) => I(`<rect x="16" y="10" width="68" height="80" rx="4" fill="${lit ? "#ffd866" : "#8f9aa3"}" stroke="${INK}" stroke-width="6"/><path d="M50 10 L50 90 M16 50 L84 50" stroke="${INK}" stroke-width="5"/>`),
  building: (c, label) => I(`<rect x="14" y="20" width="72" height="76" fill="${c}" stroke="${INK}" stroke-width="5"/>${[32, 52, 72].map((y) => `<rect x="26" y="${y}" width="14" height="10" fill="#ffe08a" stroke="${INK}" stroke-width="2"/><rect x="60" y="${y}" width="14" height="10" fill="#ffe08a" stroke="${INK}" stroke-width="2"/>`).join("")}<rect x="10" y="12" width="80" height="10" fill="#555" stroke="${INK}" stroke-width="4"/>`),
  phone: I(`<rect x="26" y="6" width="48" height="88" rx="10" fill="#111" stroke="${INK}" stroke-width="5"/><rect x="31" y="16" width="38" height="66" rx="4" fill="#ffb347"/>`),
};

module.exports = { bust, PEOPLE, ICONS };
