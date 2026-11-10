// Print an HTML file to PDF with Chromium: node render_pdf.js in.html out.pdf
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true, tagged: true });
  await browser.close();
})();
