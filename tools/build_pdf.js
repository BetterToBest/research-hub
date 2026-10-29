#!/usr/bin/env node
/* Rebuild a paper's PDF from its HTML page (step S46; CLAUDE.md: rebuild a paper's PDF whenever its HTML changes).

Usage: node tools/build_pdf.js <page.html> [<page.html> ...]
Writes papers/pdfs/<page name>.pdf for each page, printed by headless Chromium with the page's own
print styles (styles.css, @media print), US Letter, backgrounds on. Outside requests are blocked so the
PDF depends only on files in this repository. Needs Node and Playwright (npm i playwright).
*/
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');

(async () => {
  const pages = process.argv.slice(2);
  if (!pages.length) { console.error('usage: node tools/build_pdf.js <page.html> ...'); process.exit(2); }
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch();
  for (const p of pages) {
    const src = path.resolve(root, p);
    const out = path.join(root, 'papers/pdfs', path.basename(p, '.html') + '.pdf');
    const page = await browser.newPage();
    await page.route(/^https?:/, r => r.abort());
    await page.goto('file://' + src, { waitUntil: 'load' });
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: out, format: 'Letter', printBackground: true,
                     margin: { top: '0.7in', bottom: '0.7in', left: '0.7in', right: '0.7in' } });
    await page.close();
    console.log(`${p} -> ${path.relative(root, out)} (${fs.statSync(out).size} bytes)`);
  }
  await browser.close();
})();
