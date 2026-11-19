// Render a print HTML file to PDF with Chromium.
// Usage: NODE_PATH=$(npm root -g) node tools/render_pdf.js IN.html OUT.pdf ["Footer label"]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inHtml, outPdf, footer] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(inHtml), { waitUntil: 'networkidle' }).catch(e => console.log('nav', e.message));
  console.log('fonts loaded:', await p.evaluate(() => document.fonts.check('12px "Playfair Display"')));
  const opts = { path: outPdf, format: 'A4', printBackground: true, outline: true, tagged: true };
  if (footer) {
    // Optional page footer: label on the left, "Page X of Y" on the right.
    Object.assign(opts, {
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: `<div style="font-family:DejaVu Sans,sans-serif;font-size:6.5px;color:#555;width:100%;padding:0 15mm;display:flex;justify-content:space-between"><span>${footer}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
    });
  }
  await p.pdf(opts);
  await b.close();
})();
