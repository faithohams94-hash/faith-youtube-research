// Print index.html to PDF with the pre-installed Chromium.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const dir = __dirname;
  const out = process.argv[2] || path.join(dir, 'OMO-IYA-MI-Screenplay.pdf');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate:
      '<div style="width:100%;font-family:serif;font-size:8px;color:#555;padding:0 28mm 0 28mm;display:flex;justify-content:space-between;">' +
      '<span>ỌMỌ ÌYÁ MI | My Mother\'s Child</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '24mm', bottom: '24mm', left: '28mm', right: '22mm' },
    preferCSSPageSize: false,
  });
  await browser.close();
  console.log('wrote', out);
})();
