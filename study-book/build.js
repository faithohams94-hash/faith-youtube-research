// Assemble the Distinction Study Book and render it to PDF.
// Usage: node build.js [out.pdf]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');

const ROOT = __dirname;
const out = path.resolve(process.argv[2] || path.join(ROOT, 'Kris-Ohapulomuogo-Distinction-Study-Book.pdf'));
const css = fs.readFileSync(path.join(ROOT, 'style.css'), 'utf8');

const partDivider = (id, kicker, title, text, chips) => `
<div class="part-title" id="${id}"><div class="kicker">${kicker}</div><h1>${title}</h1><p>${text}</p>
<div class="chips">${chips.map(c => `<span>${c}</span>`).join('')}</div></div>`;

const DIVIDERS = {
  anatomy: partDivider('part-anatomy', 'Part One', 'Anatomy',
    'Head &amp; Neck, Neuroanatomy, Embryology, Histology and Medical Genetics. Answers follow BD Chaurasia.',
    ['Q1–Q113', 'Source: BD Chaurasia', 'Diagram-heavy']),
  biochem: partDivider('part-biochem', 'Part Two', 'Biochemistry',
    'BCM 301, 303, 305, 307 and 309. Answers follow Vasudevan &amp; Sreekumari and U. Satyanarayana.',
    ['Q114–Q260', '50 MCQs answered', 'Pathways &amp; flowcharts']),
  physio: partDivider('part-physio', 'Part Three', 'Physiology',
    'Pathophysiology, Special Senses, GIT, Endocrine, Reproduction and Laboratory Practice. Answers follow K. Sembulingam.',
    ['Q261–Q402', 'Source: Sembulingam', 'Practical procedures']),
};

// --- gather parts ---
const partsDir = path.join(ROOT, 'parts');
const partNames = fs.readdirSync(partsDir).filter(d => fs.statSync(path.join(partsDir, d)).isDirectory()).sort();
let body = '';
for (const d of partNames) {
  const files = fs.readdirSync(path.join(partsDir, d)).filter(f => f.endsWith('.html')).sort();
  let html = files.map(f => fs.readFileSync(path.join(partsDir, d, f), 'utf8')).join('\n');
  if (d.startsWith('01-')) html = DIVIDERS.anatomy + html;
  if (d.startsWith('11-')) html = DIVIDERS.physio + html;
  if (html.includes('id="sec-bcm301"')) html = html.replace(/<h2[^>]*id="sec-bcm301"/, m => DIVIDERS.biochem + m);
  body += `\n<!-- ===== ${d} ===== -->\n` + html;
}

// --- TOC + question finder generated from the content ---
const strip = s => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
const tokens = [...body.matchAll(/<div class="part-title" id="([^"]+)"[\s\S]*?<h1>([\s\S]*?)<\/h1>|<h2 class="section"[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/h2>|<section class="q" id="(q\d+)"[\s\S]*?<h3 class="q-title">([\s\S]*?)<\/h3>|<div class="mcq" id="(mcq-\d+)"/g)];
let toc = '<div class="front page-break toc"><h2 id="toc">Contents</h2><p class="section-sub">Tap any blue number to jump to the answer. Your PDF reader\'s bookmarks panel also lists every section.</p>';
toc += '<div><a href="#how-to-use">How to use this book</a> · <a href="#masterclass">Exam-writing masterclass</a> · <a href="#qindex">Question finder (all questions with titles)</a></div>';
let finder = '<div class="front page-break"><h2 id="qindex">Question finder</h2><p class="section-sub">Every question in the bank, in order. Tap a line to open its answer.</p><table style="font-size:8.4pt">';
let open = false, mcqCount = 0, qCount = 0;
for (const t of tokens) {
  if (t[1]) { if (open) toc += '</div>'; open = false; toc += `<div class="toc-part"><a href="#${t[1]}">${strip(t[2])}</a></div>`; finder += `<tr><th colspan="2">${strip(t[2])}</th></tr>`; }
  else if (t[3]) { if (open) toc += '</div>'; toc += `<div class="toc-sec"><a href="#${t[3]}">${strip(t[4])}</a></div><div class="toc-qs">`; open = true; finder += `<tr><td colspan="2"><b><a href="#${t[3]}">${strip(t[4])}</a></b></td></tr>`; }
  else if (t[5]) { qCount++; const n = t[5].slice(1); toc += `<a href="#${t[5]}">${n}</a>`; finder += `<tr><td style="width:44px"><a href="#${t[5]}"><b>Q${n}</b></a></td><td><a href="#${t[5]}" style="color:#1b2330">${strip(t[6])}</a></td></tr>`; }
  else if (t[7]) { mcqCount++; if (mcqCount === 1) { toc += `<a href="#${t[7]}" style="min-width:90px">MCQ 1–50</a>`; finder += `<tr><td><a href="#${t[7]}"><b>MCQ</b></a></td><td><a href="#${t[7]}" style="color:#1b2330">BCM 309 Section B — 50 best-option MCQs with answers and reasons</a></td></tr>`; } }
}
if (open) toc += '</div>';
toc += '</div>';
finder += '</table></div>';

// Back-to-contents link on each question head
body = body.replace(/<div class="q-meta">/g, '<a class="backlink" href="#toc">↑ Contents</a><div class="q-meta">');

const front = fs.readFileSync(path.join(ROOT, 'front.html'), 'utf8');
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Distinction Study Book — Kris Ohapulomuogo</title><style>${css}</style></head>
<body>${front}${toc}${finder}${body}</body></html>`;
fs.writeFileSync(path.join(ROOT, 'book.html'), html);

// sanity report
const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
const idset = new Set(ids);
const broken = [...new Set([...html.matchAll(/href="#([^"]+)"/g)].map(m => m[1]).filter(h => !idset.has(h)))];
const have = new Set([...html.matchAll(/<section class="q" id="q(\d+)"/g)].map(m => +m[1]));
const missing = []; for (let i = 1; i <= 402; i++) if (!have.has(i)) missing.push(i);
console.log(`questions: ${qCount} unique: ${have.size}  mcqs: ${mcqCount}  svgs: ${(html.match(/<svg/g) || []).length}`);
console.log('missing questions:', missing.join(',') || 'none');
console.log('duplicate ids:', [...new Set(dup)].slice(0, 40).join(',') || 'none');
console.log('broken links:', broken.slice(0, 40).join(',') || 'none');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.setContent(html, { waitUntil: 'load', timeout: 0 });
  await p.pdf({
    path: out, format: 'A4', printBackground: true, outline: true, tagged: true, timeout: 0,
    margin: { top: '16mm', bottom: '18mm', left: '14mm', right: '14mm' },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="font-family:Inter,sans-serif;font-size:7.5pt;color:#5b6676;width:100%;padding:0 14mm;display:flex;justify-content:space-between">
      <span>Distinction Study Book · Kris Ohapulomuogo · 2nd MBBS IMSU</span><span>Page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  await b.close();
  console.log('PDF written:', out, (fs.statSync(out).size / 1e6).toFixed(1) + ' MB');
})();
