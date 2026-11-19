// Render a print HTML file to PDF with Chromium.
// Usage: NODE_PATH=$(npm root -g) node tools/render_pdf.js IN.html OUT.pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inHtml, outPdf] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(inHtml), { waitUntil: 'networkidle' }).catch(e => console.log('nav', e.message));
  console.log('fonts loaded:', await p.evaluate(() => document.fonts.check('12px "Playfair Display"')));
  await p.pdf({ path: outPdf, format: 'A4', printBackground: true, outline: true, tagged: true });
  await b.close();
})();
