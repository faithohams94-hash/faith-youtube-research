// Usage: node render.js deck.html out.pdf fields.json
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [html, pdf, json] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await pg.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  const fields = await pg.evaluate(() => {
    const out = [];
    document.querySelectorAll('section.slide').forEach((s, i) => {
      const o = s.getBoundingClientRect();
      s.querySelectorAll('.box, .notebox').forEach(el => {
        const r = el.getBoundingClientRect();
        const cb = el.closest('[data-cb]');
        out.push({ page: i, kind: el.classList.contains('box') ? 'cb' : 'text',
          name: cb ? cb.dataset.cb : 'notes', x: r.left - o.left, y: r.top - o.top, w: r.width, h: r.height });
      });
    });
    return out;
  });
  await pg.pdf({ path: pdf, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  fs.writeFileSync(json, JSON.stringify(fields));
  await b.close();
})();
