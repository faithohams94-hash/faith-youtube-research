// Usage: node preview.js parts/03-neuro.html outdir   -> renders that fragment to outdir/preview.pdf + page PNGs (first 40)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const frag = path.resolve(process.argv[2]); const out = path.resolve(process.argv[3] || 'preview-out');
  fs.mkdirSync(out, { recursive: true });
  const css = fs.readFileSync(path.join(__dirname, 'style.css'), 'utf8');
  const body = fs.statSync(frag).isDirectory()
    ? fs.readdirSync(frag).filter(f => f.endsWith('.html')).sort().map(f => fs.readFileSync(path.join(frag, f), 'utf8')).join('\n')
    : fs.readFileSync(frag, 'utf8');
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${body}</body></html>`;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.setContent(html, { waitUntil: 'load' });
  await p.pdf({ path: path.join(out, 'preview.pdf'), format: 'A4', printBackground: true, margin: { top: '16mm', bottom: '18mm', left: '14mm', right: '14mm' } });
  // screenshot each question block for visual checking
  const ids = await p.$$eval('section.q', els => els.map(e => e.id));
  let i = 0;
  for (const id of ids) { const el = await p.$('#' + id); await el.screenshot({ path: path.join(out, `${id}.png`) }); if (++i >= 60) break; }
  // broken internal link report
  const bad = await p.$$eval('a[href^="#"]', as => as.map(a => a.getAttribute('href')).filter(h => !document.querySelector(h)));
  console.log('sections:', ids.length, 'ids:', ids.join(','));
  console.log('links to anchors not in this fragment (ok if they exist elsewhere in book):', [...new Set(bad)].join(' '));
  await b.close();
})();
