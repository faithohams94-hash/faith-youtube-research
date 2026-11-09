const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const SKILL = "/root/.claude/skills/synced/8f8de047-06e5-479d-8ec1-17e486028796_fc57a870-7bdc-4bf8-ac52-a1e3e81836d1/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";

// ---------- Theme: "Quiet Equity" — dark old-money green with gold ----------
const HEX = {
  ink: "0B1410", panel: "13231B", panel2: "1A3026", white: "F2F5F3", muted: "9DB0A6",
  green: "2FBF71", gold: "E3B341", red: "E5484D", blue: "6FA8FF",
};
const THEME = {
  name: "Quiet Equity",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.panel, lt2: HEX.muted,
    accent1: HEX.green, accent2: HEX.gold, accent3: HEX.red, accent4: HEX.blue,
    accent5: HEX.panel2, accent6: "1C3327", hlink: HEX.gold, folHlink: HEX.muted,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Quiet Equity: The Monetization Playbook";
pres.author = "Somber Journal";
const C = pres.SchemeColor;
const W = 13.333, H = 7.5;

// ---------- Icons ----------
async function icon(name, color = HEX.white) {
  const Comp = fa[name];
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- Layouts ----------
const footer = () => ({ text: { text: "QUIET EQUITY  ·  MONETIZATION PLAYBOOK", options: { x: 0.6, y: 6.95, w: 6, h: 0.3, fontSize: 10, color: C.background2, charSpacing: 2, margin: 0 } } });

pres.defineSlideMaster({
  title: "Cover",
  background: { color: HEX.ink },
  margin: [0.5, 0.6, 0.5, 0.6],
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 0.8, y: 1.9, w: 8, h: 0.5, fontSize: 16, bold: true, color: C.accent2, charSpacing: 4, fontFace: "Calibri" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.45, w: 9.2, h: 2.0, fontSize: 54, bold: true, color: C.background1, fontFace: "Cambria", valign: "top", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.55, w: 8.6, h: 1.1, fontSize: 20, color: C.background2, fontFace: "Calibri", valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Section",
  background: { color: HEX.ink },
  margin: [0.5, 0.6, 0.5, 0.6],
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 0.8, y: 2.55, w: 8, h: 0.5, fontSize: 16, bold: true, color: C.accent2, charSpacing: 4 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 3.05, w: 9.5, h: 1.3, fontSize: 44, bold: true, color: C.background1, fontFace: "Cambria", valign: "top", align: "left" }, text: "" } },
    footer(),
  ],
  slideNumber: { x: 12.2, y: 6.9, w: 0.6, h: 0.35, fontSize: 10, color: HEX.muted, align: "right" },
});
pres.defineSlideMaster({
  title: "Content",
  background: { color: HEX.ink },
  margin: [0.5, 0.6, 0.5, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.95, fontSize: 36, bold: true, color: C.background1, fontFace: "Cambria", valign: "middle", margin: 0, align: "left" }, text: "" } },
    footer(),
  ],
  slideNumber: { x: 12.2, y: 6.9, w: 0.6, h: 0.35, fontSize: 10, color: HEX.muted, align: "right" },
});

// ---------- Morph motif: a soft gold orb + green ring that drift between slides ----------
function motif(s, o) {
  // o = {ox, oy, os, rx, ry, rs}
  s.addShape(pres.shapes.OVAL, { x: o.ox, y: o.oy, w: o.os, h: o.os, fill: { color: C.accent2, transparency: 88 }, line: { type: "none" }, objectName: "!!orb" });
  s.addShape(pres.shapes.OVAL, { x: o.rx, y: o.ry, w: o.rs, h: o.rs, fill: { type: "none" }, line: { color: C.accent1, width: 2, transparency: 55 }, objectName: "!!ring" });
}
const POS = [
  { ox: 8.6, oy: 0.6, os: 6.2, rx: 9.6, ry: 1.4, rs: 4.6 },
  { ox: 10.9, oy: -1.6, os: 3.6, rx: 11.6, ry: 5.6, rs: 2.4 },
  { ox: -1.4, oy: 5.2, os: 3.4, rx: 11.9, ry: -0.9, rs: 2.2 },
  { ox: 11.2, oy: 5.0, os: 3.4, rx: -1.0, ry: -1.0, rs: 2.4 },
  { ox: 7.4, oy: 1.0, os: 6.6, rx: 8.4, ry: 1.9, rs: 4.8 },
];
let posIdx = 0;
const nextPos = () => POS[(posIdx++) % POS.length];

// ---------- Helpers ----------
function card(s, x, y, w, h, name, fill = C.text2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { type: "none" }, objectName: name });
}
function txt(s, text, opt) { s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Calibri", color: C.background1, fontSize: 16, valign: "top" }, opt)); }
async function iconDot(s, x, y, d, name, fill, name2) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: name2 + "_dot" });
  s.addImage({ data: await icon(name), x: x + d * 0.25, y: y + d * 0.25, w: d * 0.5, h: d * 0.5, objectName: name2 + "_icon" });
}
function content(title, section, notes) {
  const s = pres.addSlide({ masterName: "Content", sectionTitle: section });
  motif(s, nextPos());
  s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}
function sectionSlide(kicker, title, section, notes) {
  pres.addSection({ title: section });
  const s = pres.addSlide({ masterName: "Section", sectionTitle: section });
  motif(s, { ox: 7.8, oy: 0.4, os: 6.8, rx: 8.9, ry: 1.5, rs: 4.6 });
  s.addText(kicker, { placeholder: "kicker" });
  s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}

(async () => {
  // ===== 1. Cover =====
  pres.addSection({ title: "Opening" });
  let s = pres.addSlide({ masterName: "Cover", sectionTitle: "Opening" });
  motif(s, POS[0]);
  s.addText("SOMBER JOURNAL  →  QUIET EQUITY", { placeholder: "kicker" });
  s.addText("The Monetization Playbook", { placeholder: "title" });
  s.addText("Why the channel isn't growing, what the winners did, and the exact plan for the next 30 days", { placeholder: "body" });
  s.addNotes("This deck sums up the full audit: where the channel stands, what seven competitor channels show, the formula that works in POV finance, and the plan for the first two videos and the first 30 days.");

  // ===== Section 1: Diagnosis =====
  sectionSlide("PART 1", "Where you stand", "Diagnosis", "First, the honest numbers.");

  // 2. Stats
  s = content("Not rejected — just not found yet", "Diagnosis",
    "Fifteen subscribers and about 154 views across five videos. The watch-hour figure is an estimate (154 views at about two minutes each). Nothing is wrong with the account; YouTube simply hasn't found an audience for these videos.");
  const stats = [
    ["15", "subscribers", "FaUsers", C.accent1],
    ["5", "videos", "FaVideo", C.accent4],
    ["~154", "total views", "FaEye", C.accent2],
    ["~5", "watch hours", "FaClock", C.accent3],
  ];
  for (let i = 0; i < 4; i++) {
    const x = 0.6 + i * 3.08;
    card(s, x, 1.75, 2.8, 3.1, "stat" + i);
    await iconDot(s, x + 0.35, 2.05, 0.75, stats[i][2], stats[i][3], "stat" + i);
    txt(s, stats[i][0], { x: x + 0.35, y: 2.95, w: 2.2, h: 1.0, fontSize: 60, bold: true, fontFace: "Cambria" });
    txt(s, stats[i][1], { x: x + 0.35, y: 4.0, w: 2.2, h: 0.45, fontSize: 18, color: C.background2 });
  }
  txt(s, [
    { text: "The verdict: ", options: { bold: true, color: C.accent2 } },
    { text: "about 0.1% of the way to monetization. Not a penalty — a packaging and focus problem." },
  ], { x: 0.6, y: 5.25, w: 12.1, h: 0.9, fontSize: 20 });

  // 3. The bar
  s = content("The bar you have to clear", "Diagnosis",
    "Today: 1,000 subscribers plus 4,000 watch hours in 12 months, or 10 million Shorts views in 90 days. From 1 February 2027 new applicants need 8,000 hours or 20 million Shorts views; subscribers stay at 1,000. These figures come from news coverage of YouTube's August 2026 announcement, so check the official help page.");
  card(s, 0.6, 1.7, 5.9, 3.6, "barNow");
  txt(s, "NOW  ·  UNTIL 31 JAN 2027", { x: 0.95, y: 1.95, w: 5.2, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 3 });
  txt(s, "4,000", { x: 0.95, y: 2.4, w: 5.2, h: 1.1, fontSize: 64, bold: true, fontFace: "Cambria" });
  txt(s, "watch hours + 1,000 subscribers\nor 10M Shorts views in 90 days", { x: 0.95, y: 3.55, w: 5.2, h: 1.0, fontSize: 18, color: C.background2 });
  card(s, 6.85, 1.7, 5.9, 3.6, "barNext");
  txt(s, "FROM 1 FEB 2027", { x: 7.2, y: 1.95, w: 5.2, h: 0.4, fontSize: 14, bold: true, color: C.accent3, charSpacing: 3 });
  txt(s, "8,000", { x: 7.2, y: 2.4, w: 5.2, h: 1.1, fontSize: 64, bold: true, fontFace: "Cambria" });
  txt(s, "watch hours + 1,000 subscribers\nor 20M Shorts views in 90 days", { x: 7.2, y: 3.55, w: 5.2, h: 1.0, fontSize: 18, color: C.background2 });
  txt(s, [
    { text: "The math that matters: ", options: { bold: true, color: C.accent2 } },
    { text: "one 50K-view, 20-minute video ≈ 5,800 watch hours. You don't need slow growth — you need one or two hits." },
  ], { x: 0.6, y: 5.6, w: 12.1, h: 0.9, fontSize: 18 });

  // 4. Chart of your videos
  s = content("Your best video was the only one that showed the win", "Diagnosis",
    "The divorce video got about 3.5 times the views of the others per day online. It is the only thumbnail with a money transformation: AGE 55: $0, AGE 56: $1.4M. The two Every Level of Wealth videos are the weakest.");
  s.addChart(pres.charts.BAR, [{ name: "Views", labels: ["Divorced at 55 → $1.4M", "Live with parents at 30", "Getting sick, every level", "Work for younger brother", "Family, every level"], values: [70, 40, 20, 17, 7] }], {
    x: 0.6, y: 1.6, w: 7.4, h: 4.9, barDir: "bar", chartColors: [HEX.green],
    catAxisLabelColor: HEX.white, valAxisLabelColor: HEX.muted, catAxisLabelFontSize: 14, valAxisLabelFontSize: 12,
    catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt",
    valGridLine: { color: HEX.panel2, size: 0.75 }, catGridLine: { style: "none" }, catAxisOrientation: "maxMin",
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: HEX.white, dataLabelFontSize: 14,
    showLegend: false, showTitle: true, title: "Views per video (Somber Journal)", titleColor: HEX.muted, titleFontSize: 14, titleFontFace: "+mn-lt",
    valAxisHidden: true, barGapWidthPct: 60,
  });
  card(s, 8.4, 1.7, 4.35, 4.7, "insight");
  await iconDot(s, 8.75, 2.0, 0.75, "FaTrophy", C.accent2, "insight");
  txt(s, "3.5×", { x: 8.75, y: 2.95, w: 3.7, h: 0.9, fontSize: 54, bold: true, fontFace: "Cambria", color: C.accent2 });
  txt(s, "The divorce thumbnail said \"AGE 55: $0 → AGE 56: $1.4M\". Viewers knew the payoff before they clicked.\n\nThe two \"Every Level\" videos got 20 and 7.", { x: 8.75, y: 3.9, w: 3.7, h: 2.3, fontSize: 16, color: C.background2 });

  // ===== Section 2: Competitors =====
  sectionSlide("PART 2", "What the winners did", "Competitors", "Seven channels from the screenshots, compared.");

  // 5. Pivot pattern
  s = content("Three channels pivoted into the same formula", "Competitors",
    "POV Finance went from retirement listicles to old-money stories. Finance With Henry went from listicles and Every Level videos to quiet-wealth stories. POV Finance Life went from explainers to boss-and-building stories. Same channels, same art style, different angle.");
  const piv = [
    ["POV Finance", "Retirement listicles", "316", "Old-money POV stories", "744K"],
    ["Finance With Henry", "\"Every Level\" & listicles", "633", "\"Richer than your boss\"", "20K"],
    ["POV Finance Life", "Money explainers", "7", "\"You own the building\"", "48K"],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 4.12;
    card(s, x, 1.7, 3.85, 4.75, "piv" + i);
    txt(s, piv[i][0], { x: x + 0.3, y: 1.95, w: 3.3, h: 0.5, fontSize: 20, bold: true, fontFace: "Cambria" });
    txt(s, "BEFORE", { x: x + 0.3, y: 2.6, w: 3.3, h: 0.3, fontSize: 12, bold: true, color: C.accent3, charSpacing: 3 });
    txt(s, piv[i][1], { x: x + 0.3, y: 2.9, w: 3.3, h: 0.4, fontSize: 15, color: C.background2 });
    txt(s, piv[i][2] + " views", { x: x + 0.3, y: 3.3, w: 3.3, h: 0.55, fontSize: 26, bold: true, color: C.background2 });
    s.addShape(pres.shapes.LINE, { x: x + 0.3, y: 4.05, w: 3.25, h: 0, line: { color: C.accent5, width: 1 } });
    txt(s, "AFTER", { x: x + 0.3, y: 4.2, w: 3.3, h: 0.3, fontSize: 12, bold: true, color: C.accent1, charSpacing: 3 });
    txt(s, piv[i][3], { x: x + 0.3, y: 4.5, w: 3.3, h: 0.4, fontSize: 15, color: C.background2 });
    txt(s, piv[i][4] + " views", { x: x + 0.3, y: 4.95, w: 3.3, h: 0.9, fontSize: 40, bold: true, fontFace: "Cambria", color: C.accent1 });
  }

  // 6. What kills views
  s = content("What kills views in this niche", "Competitors",
    "Patterns from every low-view video in the screenshots.");
  const kills = [
    ["FaChalkboardTeacher", "Lectures & listicles", "\"5 Signs…\", \"Leasing vs Buying\" — under 2K, often under 50"],
    ["FaLayerGroup", "\"Every Level of Wealth\"", "633 for Henry, 7 and 20 for you — the format is worn out"],
    ["FaCrown", "Abstract power fantasy", "\"You Control Political Power\" — 137. Nobody relates"],
    ["FaQuestion", "No conflict, no twist", "A nice feeling with nobody to beat — 335"],
    ["FaCopy", "Copied thumbnails", "Clones of 384K and 198K hits got 636 and 371"],
    ["FaStopwatch", "5–8 minute videos", "POV Finance Max: 22 videos, 9 subscribers"],
  ];
  for (let i = 0; i < 6; i++) {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.15, y = 1.65 + row * 1.6;
    card(s, x, y, 5.95, 1.4, "kill" + i);
    await iconDot(s, x + 0.25, y + 0.3, 0.8, kills[i][0], C.accent3, "kill" + i);
    txt(s, kills[i][1], { x: x + 1.3, y: y + 0.22, w: 4.45, h: 0.4, fontSize: 18, bold: true });
    txt(s, kills[i][2], { x: x + 1.3, y: y + 0.65, w: 4.45, h: 0.65, fontSize: 14, color: C.background2 });
  }

  // 7. Why people love it
  s = content("What people love: the quiet winner", "Competitors",
    "The audience watches to feel like the person who was underestimated and quietly won. That is why 744K and 493K views are possible on simple illustrated stories.");
  const love = [
    ["FaUserSecret", "The quiet-winner fantasy", "Everyone has been underestimated by a boss, family, an ex"],
    ["FaLeaf", "Relief from flexing", "Old money and \"nobody knows\" feel within reach"],
    ["FaLightbulb", "It feels useful", "A money idea without a lecture"],
    ["FaBolt", "The payoff", "The moment the doubters find out"],
    ["FaHome", "Everyday settings", "Bosses, landlords, family dinners, car loans"],
  ];
  for (let i = 0; i < 5; i++) {
    const y = 1.6 + i * 0.98;
    await iconDot(s, 0.6, y, 0.72, love[i][0], C.accent1, "love" + i);
    txt(s, love[i][1], { x: 1.55, y: y + 0.02, w: 4.6, h: 0.4, fontSize: 18, bold: true });
    txt(s, love[i][2], { x: 1.55, y: y + 0.4, w: 4.8, h: 0.4, fontSize: 14, color: C.background2 });
  }
  card(s, 7.0, 1.7, 5.75, 4.75, "loveStat");
  txt(s, "744K", { x: 7.4, y: 2.0, w: 5.0, h: 1.2, fontSize: 72, bold: true, fontFace: "Cambria", color: C.accent2 });
  txt(s, "\"POV You Adopted the Old Money Mindset\"\nPOV Finance · 2 months", { x: 7.4, y: 3.25, w: 5.0, h: 0.8, fontSize: 16, color: C.background2 });
  txt(s, "48K in 7 days", { x: 7.4, y: 4.3, w: 5.0, h: 0.8, fontSize: 40, bold: true, fontFace: "Cambria", color: C.accent1 });
  txt(s, "from a channel with only 709 subscribers", { x: 7.4, y: 5.15, w: 5.0, h: 0.5, fontSize: 16, color: C.background2 });

  // ===== Section 3: The formula =====
  sectionSlide("PART 3", "The formula", "The formula", "Titles, thumbnails, mood and editing.");

  // 8. Title formula
  s = content("One title formula, every single time", "The formula",
    "Put the twist in the title. The viewer clicks to watch the payoff happen, not to find out what it is. Your brother title had only the first half.");
  card(s, 0.6, 1.6, 12.15, 1.35, "formula", C.accent5);
  txt(s, [
    { text: "POV: ", options: { color: C.background2 } },
    { text: "[someone looks down on you]", options: { color: C.accent3 } },
    { text: "  —  ", options: { color: C.background2 } },
    { text: "[you secretly have the money]", options: { color: C.accent1 } },
  ], { x: 0.95, y: 1.85, w: 11.5, h: 0.85, fontSize: 26, bold: true, fontFace: "Cambria", valign: "middle" });
  txt(s, "WINNERS", { x: 0.6, y: 3.25, w: 5.8, h: 0.35, fontSize: 13, bold: true, color: C.accent1, charSpacing: 3 });
  txt(s, [
    { text: "Your Boss Still Thinks You Need This Job — You Own the Building He Rents  (48K)", options: { bullet: true, breakLine: true } },
    { text: "You Became Richer Than Your Boss — And Kept It to Yourself  (20K)", options: { bullet: true, breakLine: true } },
    { text: "You Became the Rich Friend — Then Things Got Awkward  (439K)", options: { bullet: true } },
  ], { x: 0.6, y: 3.65, w: 5.9, h: 2.6, fontSize: 15, color: C.background2, paraSpaceAfter: 8 });
  card(s, 6.85, 3.25, 5.9, 3.2, "rewrite");
  txt(s, "YOURS (17 VIEWS)", { x: 7.15, y: 3.45, w: 5.3, h: 0.3, fontSize: 12, bold: true, color: C.accent3, charSpacing: 3 });
  txt(s, "You are 40 and You Still Work for your Younger Brother", { x: 7.15, y: 3.8, w: 5.3, h: 0.7, fontSize: 16, color: C.background2, italic: true });
  txt(s, "REWRITTEN", { x: 7.15, y: 4.6, w: 5.3, h: 0.3, fontSize: 12, bold: true, color: C.accent1, charSpacing: 3 });
  txt(s, "Your Little Brother Thinks He Gave You a Job — You Own 24% of His Company", { x: 7.15, y: 4.95, w: 5.3, h: 1.3, fontSize: 20, bold: true, fontFace: "Cambria" });

  // 9. Thumbnail recipe with mock
  s = content("The thumbnail recipe", "The formula",
    "Every winning thumbnail: the protagonist big and calm with a visible face, proof of money, one to three shocked faces, bright daylight, zero to three words.");
  const rec = ["Big, calm, visible face — never the back of his head", "Proof of money: green number, PAID IN FULL, a deed", "1–3 shocked or jealous faces on the other side", "Bright daylight, simple background", "0–3 words of text, or none at all"];
  for (let i = 0; i < 5; i++) {
    const y = 1.65 + i * 0.95;
    s.addShape(pres.shapes.OVAL, { x: 0.6, y, w: 0.62, h: 0.62, fill: { color: C.accent2 }, line: { type: "none" }, objectName: "num" + i });
    txt(s, String(i + 1), { x: 0.6, y, w: 0.62, h: 0.62, fontSize: 20, bold: true, color: C.text1, align: "center", valign: "middle" });
    txt(s, rec[i], { x: 1.45, y: y + 0.08, w: 4.9, h: 0.55, fontSize: 16, valign: "middle" });
  }
  // mock thumbnail 16:9
  const mx = 6.75, my = 1.75, mw = 6.0, mh = 3.375;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: mx, y: my, w: mw, h: mh, rectRadius: 0.12, fill: { color: "8FC9F2" }, line: { color: C.background1, width: 2 }, objectName: "mockFrame" });
  s.addShape(pres.shapes.RECTANGLE, { x: mx, y: my + 2.4, w: mw, h: 0.95, fill: { color: "7FB069" }, line: { type: "none" }, objectName: "mockGround" });
  s.addShape(pres.shapes.OVAL, { x: mx + 0.35, y: my + 0.7, w: 1.9, h: 1.9, fill: { color: "F4D9C0" }, line: { color: C.text1, width: 3 }, objectName: "mockHero" });
  s.addShape(pres.shapes.RECTANGLE, { x: mx + 0.25, y: my + 2.45, w: 2.1, h: 0.9, fill: { color: C.text1 }, line: { type: "none" }, objectName: "mockBody" });
  txt(s, "calm\nhalf-smile", { x: mx + 0.35, y: my + 1.25, w: 1.9, h: 0.8, fontSize: 12, color: C.text1, align: "center", valign: "middle" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: mx + 2.35, y: my + 1.35, w: 1.05, h: 1.75, rectRadius: 0.1, fill: { color: C.text1 }, line: { color: C.background1, width: 1.5 }, objectName: "mockPhone" });
  txt(s, "$2.4M", { x: mx + 2.35, y: my + 1.85, w: 1.05, h: 0.5, fontSize: 16, bold: true, color: C.accent1, align: "center" });
  for (let k = 0; k < 2; k++) {
    s.addShape(pres.shapes.OVAL, { x: mx + 3.8 + k * 1.05, y: my + 1.4 + k * 0.25, w: 0.95, h: 0.95, fill: { color: "F4D9C0" }, line: { color: C.text1, width: 2 }, objectName: "mockShock" + k });
    txt(s, "O_O", { x: mx + 3.8 + k * 1.05, y: my + 1.55 + k * 0.25, w: 0.95, h: 0.6, fontSize: 16, bold: true, color: C.text1, align: "center", valign: "middle" });
  }
  txt(s, "HE HAS NO IDEA", { x: mx + 2.6, y: my + 0.25, w: 3.2, h: 0.6, fontSize: 24, bold: true, color: "FFE14D", fontFace: "Calibri", align: "right" });
  txt(s, "Layout sketch, not final art", { x: mx, y: my + mh + 0.15, w: mw, h: 0.35, fontSize: 12, color: C.background2, italic: true });
  txt(s, "Drop the \"YOU + red arrow\" over crowded scenes.", { x: mx, y: 5.8, w: mw, h: 0.4, fontSize: 15, color: C.accent2, bold: true });

  // 10. Rebrand
  s = content("From Somber Journal to Quiet Equity", "The formula",
    "Same niche, same channel, new promise. The audience wants the win, not the pain. Renaming costs nothing at 15 subscribers.");
  const reb = [
    ["Name", "Somber Journal", "Quiet Equity"],
    ["Mood", "Sad, wounded, deadpan", "Calm, in control, quietly winning"],
    ["Character", "Hood up, tired eyes", "Same face, sweater, knowing half-smile"],
    ["Thumbnails", "He's losing, often in the dark", "He's winning, in daylight, with proof"],
    ["Who loses composure", "Him", "The people who doubted him"],
  ];
  card(s, 0.6, 1.6, 12.15, 4.85, "rebCard");
  txt(s, "BEFORE", { x: 3.6, y: 1.8, w: 4.2, h: 0.35, fontSize: 13, bold: true, color: C.accent3, charSpacing: 3 });
  txt(s, "AFTER", { x: 8.2, y: 1.8, w: 4.3, h: 0.35, fontSize: 13, bold: true, color: C.accent1, charSpacing: 3 });
  for (let i = 0; i < reb.length; i++) {
    const y = 2.3 + i * 0.8;
    txt(s, reb[i][0], { x: 0.95, y, w: 2.5, h: 0.6, fontSize: 16, bold: true, color: C.accent2, valign: "middle" });
    txt(s, reb[i][1], { x: 3.6, y, w: 4.3, h: 0.6, fontSize: 16, color: C.background2, valign: "middle" });
    s.addImage({ data: await icon("FaArrowRight", HEX.gold), x: 7.65, y: y + 0.17, w: 0.28, h: 0.28, objectName: "rebArrow" + i });
    txt(s, reb[i][2], { x: 8.2, y, w: 4.3, h: 0.6, fontSize: 16, bold: true, valign: "middle" });
  }

  // 11. Editing
  s = content("Images + voiceover is enough — if it's edited", "The formula",
    "The big channels are illustrated stills with narration. What keeps viewers is the editing: constant motion, sound, numbers on screen, and a handful of animated moments.");
  s.addChart(pres.charts.DOUGHNUT, [{ name: "Mix", labels: ["Stills with zoom/pan", "Animated key moments"], values: [85, 15] }], {
    x: 0.5, y: 1.55, w: 4.6, h: 4.6, holeSize: 62, chartColors: [HEX.green, HEX.gold],
    showLegend: true, legendPos: "b", legendColor: HEX.white, legendFontSize: 14, legendFontFace: "+mn-lt",
    showPercent: true, showValue: false, dataLabelColor: HEX.ink, dataLabelFontSize: 14, dataLabelFontFace: "+mn-lt", showTitle: false,
    dataBorder: { pt: 1, color: HEX.ink },
  });
  const edits = [
    ["FaImages", "New image every 3–6 seconds"],
    ["FaSearchPlus", "Zoom or pan on every still"],
    ["FaVolumeUp", "Sound effects: buzz, cash register, crowd"],
    ["FaMusic", "Quiet music that lifts at the reveal"],
    ["FaDollarSign", "Dollar amounts pop up on screen"],
    ["FaMicrophone", "Natural voice at ~2.8 words per second"],
  ];
  for (let i = 0; i < 6; i++) {
    const y = 1.65 + i * 0.8;
    await iconDot(s, 5.6, y, 0.6, edits[i][0], C.accent1, "edit" + i);
    txt(s, edits[i][1], { x: 6.4, y: y + 0.08, w: 6.3, h: 0.45, fontSize: 18, valign: "middle" });
  }

  // 12. Series ladder
  s = content("Standalone first. Series later.", "The formula",
    "A series only works once people are waiting for the next episode. Copy how Beanie Survives writes titles: the hook first, the series label last.");
  const steps = [
    ["VIDEOS 1–15", "Standalone POV stories", "Same character, new life situation each time. Every title works alone."],
    ["FIRST 5K+ HIT", "Make a sequel", "\"Your Brother Found Out You Own 24% — Now He Wants It Back | Part 2\""],
    ["3–5 HITS", "Build the series", "Name the character, connect the stories: \"… | Quiet Equity Ep. 7\""],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 4.12;
    card(s, x, 2.0 + (2 - i) * 0.45, 3.85, 3.6 - (2 - i) * 0.45, "step" + i);
    txt(s, steps[i][0], { x: x + 0.3, y: 2.25 + (2 - i) * 0.45, w: 3.3, h: 0.35, fontSize: 13, bold: true, color: C.accent2, charSpacing: 3 });
    txt(s, steps[i][1], { x: x + 0.3, y: 2.65 + (2 - i) * 0.45, w: 3.3, h: 0.5, fontSize: 22, bold: true, fontFace: "Cambria" });
    txt(s, steps[i][2], { x: x + 0.3, y: 3.25 + (2 - i) * 0.45, w: 3.3, h: 1.6, fontSize: 15, color: C.background2 });
    if (i < 2) s.addImage({ data: await icon("FaChevronRight", HEX.gold), x: x + 3.88, y: 4.0, w: 0.22, h: 0.3, objectName: "stepArrow" + i });
  }
  txt(s, "Beanie Survives: 110K subscribers from 26 videos — but its titles still hook strangers first.", { x: 0.6, y: 5.9, w: 12.1, h: 0.45, fontSize: 15, italic: true, color: C.background2 });

  // 13. True stories
  s = content("Add true stories inside your POV format", "The formula",
    "Keep fictional POV as the core and add 'based on a true story' episodes about real quiet millionaires. Verify every fact before scripting; the figures here are approximate.");
  s.addChart(pres.charts.DOUGHNUT, [{ name: "Mix", labels: ["Fictional POV stories", "True-story POV"], values: [70, 30] }], {
    x: 0.5, y: 1.55, w: 4.6, h: 4.6, holeSize: 62, chartColors: [HEX.green, HEX.gold],
    showLegend: true, legendPos: "b", legendColor: HEX.white, legendFontSize: 14, legendFontFace: "+mn-lt",
    showPercent: true, showValue: false, dataLabelColor: HEX.ink, dataLabelFontSize: 14, dataLabelFontFace: "+mn-lt", showTitle: false,
    dataBorder: { pt: 1, color: HEX.ink },
  });
  const ts = [
    ["~$8M", "Ronald Read", "Gas station attendant and janitor; his town found out only after he died"],
    ["~$9M", "Sylvia Bloom", "Legal secretary who copied her bosses' stock trades on a small salary"],
    ["~$7M", "Grace Groner", "Bought three $60 shares in 1935 and left it all to her college"],
  ];
  for (let i = 0; i < 3; i++) {
    const y = 1.65 + i * 1.55;
    card(s, 5.6, y, 7.15, 1.35, "true" + i);
    txt(s, ts[i][0], { x: 5.9, y: y + 0.2, w: 1.7, h: 0.9, fontSize: 32, bold: true, fontFace: "Cambria", color: C.accent2, valign: "middle" });
    txt(s, ts[i][1], { x: 7.7, y: y + 0.18, w: 4.8, h: 0.4, fontSize: 18, bold: true });
    txt(s, ts[i][2], { x: 7.7, y: y + 0.58, w: 4.8, h: 0.65, fontSize: 14, color: C.background2 });
  }

  // ===== Section 4: The plan =====
  sectionSlide("PART 4", "The plan", "The plan", "The first two videos, the rules, and the first 30 days.");

  // 14. First two videos
  s = content("Your first two videos: two different bets", "The plan",
    "Both use the formula; each tests a different type of story. Video 1 within about five days, Video 2 within about ten.");
  const vids = [
    ["VIDEO 1  ·  FICTIONAL POV", "Your Landlord Raised the Rent Again — You Just Bought the Building", "You, calm, holding the deed; the landlord shocked in the doorway; \"HE HAS NO IDEA\"", "\"Your landlord just slid a rent increase under your door. Third one this year. He doesn't know that tomorrow at 9 a.m., you sign the papers that make you his landlord.\"", "FaKey", C.accent1],
    ["VIDEO 2  ·  TRUE STORY", "You're a Janitor Everyone Ignored — You Quietly Left $8 Million (True Story)", "Old man at a gas pump; a giant $8,000,000 check; shocked townspeople; \"TRUE STORY\"", "\"Everyone in town thought you were poor. You pumped gas for 25 years. When you died, they found $8 million.\"", "FaGasPump", C.accent2],
  ];
  for (let i = 0; i < 2; i++) {
    const x = 0.6 + i * 6.15;
    card(s, x, 1.6, 5.95, 4.95, "vid" + i);
    await iconDot(s, x + 0.3, 1.85, 0.7, vids[i][4], vids[i][5], "vid" + i);
    txt(s, vids[i][0], { x: x + 1.2, y: 2.0, w: 4.5, h: 0.4, fontSize: 13, bold: true, color: vids[i][5], charSpacing: 3 });
    txt(s, vids[i][1], { x: x + 0.3, y: 2.7, w: 5.35, h: 1.0, fontSize: 19, bold: true, fontFace: "Cambria" });
    txt(s, [{ text: "Thumbnail: ", options: { bold: true, color: C.background1 } }, { text: vids[i][2] }], { x: x + 0.3, y: 3.8, w: 5.35, h: 0.8, fontSize: 14, color: C.background2 });
    txt(s, [{ text: "First line: ", options: { bold: true, color: C.background1 } }, { text: vids[i][3], options: { italic: true } }], { x: x + 0.3, y: 4.65, w: 5.35, h: 1.8, fontSize: 14, color: C.background2 });
  }

  // 15. Rules table
  s = content("Rules for every upload", "The plan",
    "Keep these fixed so you learn from what changes.");
  const rows = [
    ["Length", "16–20 minutes (about 2,600–3,200 words)"],
    ["Opening", "Twist and payoff in the first 15 seconds; full premise by 0:30"],
    ["Pacing", "Something new every 60–90 seconds; hint the payoff at 40%"],
    ["Thumbnails", "3 versions, run with Test & Compare"],
    ["Posting time", "2–4 pm US Eastern, weekdays"],
    ["Engagement", "End screen to the other video; a pinned question"],
    ["Shorts", "Two 45–60 second vertical cuts per video"],
  ];
  const tRows = rows.map((r, i) => [
    { text: r[0], options: { bold: true, color: C.accent2, fill: { color: i % 2 ? C.text1 : C.text2 } } },
    { text: r[1], options: { color: C.background1, fill: { color: i % 2 ? C.text1 : C.text2 } } },
  ]);
  s.addTable(tRows, { x: 0.6, y: 1.65, w: 12.1, colW: [2.8, 9.3], fontSize: 16, fontFace: "Calibri", rowH: 0.62, valign: "middle", border: { type: "none" }, margin: [0.05, 0.18, 0.05, 0.18] });

  // 16. Decision table
  s = content("Read the numbers. Change one thing at a time.", "The plan",
    "Give each type of story three videos before judging it. The 10K will come from one video, not the channel average.");
  const dh = ["When", "Check", "If it's bad", "Change this"].map((t) => ({ text: t, options: { bold: true, color: C.text1, fill: { color: C.accent2 } } }));
  const drows = [
    ["48 hours", "Click-through rate", "Under 3%", "Thumbnail and title"],
    ["48 hours", "Still watching at 0:30", "Under 55%", "First 15 seconds of the next script"],
    ["7 days", "Impressions", "Under 1,000", "Topic or angle of the next video"],
    ["7 days", "Average % watched", "Under 25%", "Pacing and editing"],
  ].map((r, i) => r.map((t, j) => ({ text: t, options: { color: j === 2 ? C.accent3 : C.background1, bold: j === 0, fill: { color: i % 2 ? C.text1 : C.text2 } } })));
  s.addTable([dh, ...drows], { x: 0.6, y: 1.65, w: 12.1, colW: [2.0, 3.4, 2.4, 4.3], fontSize: 16, fontFace: "Calibri", rowH: 0.75, valign: "middle", border: { type: "none" }, margin: [0.05, 0.18, 0.05, 0.18] });
  txt(s, [
    { text: "When one video climbs faster than the rest: ", options: { bold: true, color: C.accent1 } },
    { text: "make 2–3 more on that theme straight away, plus a sequel." },
  ], { x: 0.6, y: 5.75, w: 12.1, h: 0.6, fontSize: 17 });

  // 17. January math
  s = content("January is a stretch goal — chase it the right way", "The plan",
    "To apply before the bar doubles you need roughly 35,000 views of 18-minute videos plus 1,000 subscribers by the end of January. That only happens with one or two hits. If you miss it, the target becomes about two good hits instead.");
  const jm = [["~35K", "views of 18-min videos\n≈ 4,000 hours", C.accent2], ["1,000", "subscribers\nby 31 January", C.accent4], ["1–2", "videos that take off\nis all it takes", C.accent1]];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 4.12;
    card(s, x, 1.7, 3.85, 2.9, "jm" + i);
    txt(s, jm[i][0], { x: x + 0.35, y: 1.95, w: 3.2, h: 1.2, fontSize: 64, bold: true, fontFace: "Cambria", color: jm[i][2] });
    txt(s, jm[i][1], { x: x + 0.35, y: 3.25, w: 3.2, h: 1.0, fontSize: 17, color: C.background2 });
  }
  card(s, 0.6, 4.9, 12.15, 1.5, "warn", C.accent5);
  await iconDot(s, 0.9, 5.25, 0.8, "FaBan", C.accent3, "warn");
  txt(s, [
    { text: "Never buy views, watch hours or subscribers. ", options: { bold: true, color: C.accent3 } },
    { text: "Bought hours don't count, they wreck targeting, and they get channels rejected or terminated. \"Monetization services\" are scams." },
  ], { x: 2.0, y: 5.1, w: 10.5, h: 1.1, fontSize: 17, valign: "middle" });

  // 18. Don'ts
  s = content("Never do these", "The plan", "Each of these teaches YouTube the wrong audience or risks the monetization review.");
  const donts = [
    ["Send videos to friends or WhatsApp groups", "They click and leave — YouTube learns the wrong audience"],
    ["Watch your own videos from other accounts", "Same problem, and it looks like manipulation"],
    ["Delete videos that underperform", "Unlist them instead"],
    ["Copy a competitor's exact title or thumbnail", "The clones in your screenshots got ~400–600 views"],
    ["Give AI-narrated investment advice", "Tell stories; don't tell people what to buy"],
    ["Change everything after one flop", "Keep the formula; change one variable"],
  ];
  for (let i = 0; i < 6; i++) {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.15, y = 1.65 + row * 1.6;
    card(s, x, y, 5.95, 1.4, "dont" + i);
    await iconDot(s, x + 0.25, y + 0.3, 0.8, "FaTimes", C.accent3, "dont" + i);
    txt(s, donts[i][0], { x: x + 1.3, y: y + 0.2, w: 4.45, h: 0.55, fontSize: 17, bold: true });
    txt(s, donts[i][1], { x: x + 1.3, y: y + 0.78, w: 4.45, h: 0.5, fontSize: 14, color: C.background2 });
  }

  // 19. 30 days
  s = content("Your first 30 days", "The plan", "Week one is the makeover; then two uploads a week, measured the same way every time.");
  const days = [
    ["WEEK 1", "Makeover", "Rename to Quiet Equity, new picture and banner, restyle the character. Retitle the brother, parents and divorce videos. Unlist the two Every Level videos."],
    ["WEEKS 1–4", "8 new videos", "Two a week, all in the formula, 16–20 minutes, premise inside 30 seconds."],
    ["EVERY UPLOAD", "Measure", "3 thumbnails in Test & Compare. Note click-through and 0:30 retention at 48 hours."],
    ["WEEK 4", "Double down", "Find the best video. Make 2 more on its theme, and a sequel if it passed 5K."],
  ];
  s.addShape(pres.shapes.LINE, { x: 0.9, y: 2.15, w: 11.5, h: 0, line: { color: C.accent2, width: 2 } });
  for (let i = 0; i < 4; i++) {
    const x = 0.6 + i * 3.08;
    s.addShape(pres.shapes.OVAL, { x: x + 0.15, y: 1.95, w: 0.4, h: 0.4, fill: { color: C.accent2 }, line: { color: C.text1, width: 3 }, objectName: "dot" + i });
    card(s, x, 2.65, 2.85, 3.75, "day" + i);
    txt(s, days[i][0], { x: x + 0.25, y: 2.85, w: 2.4, h: 0.35, fontSize: 13, bold: true, color: C.accent2, charSpacing: 3 });
    txt(s, days[i][1], { x: x + 0.25, y: 3.25, w: 2.4, h: 0.5, fontSize: 22, bold: true, fontFace: "Cambria" });
    txt(s, days[i][2], { x: x + 0.25, y: 3.85, w: 2.4, h: 2.4, fontSize: 14, color: C.background2 });
  }

  // 20. Closing
  pres.addSection({ title: "Close" });
  s = pres.addSlide({ masterName: "Cover", sectionTitle: "Close" });
  motif(s, POS[0]);
  s.addText("THE WHOLE STRATEGY IN ONE LINE", { placeholder: "kicker" });
  s.addText("Quiet wins compound", { placeholder: "title" });
  s.addText("One niche. One formula. Two videos a week. Find the hit, then build the series.", { placeholder: "body" });
  s.addNotes("Stay in POV finance, change the angle to the quiet winner, find one or two hits, then turn them into sequels and a series.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})().catch((e) => { console.error(e); process.exit(1); });
