// Renders tree.html to PNG (2x) and a page-sized PDF with Chromium, so Poppins is used.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const W = 1800, H = 1790;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(dir, 'tree.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(dir, 'Operational-Process-Tree_2026-10-12.png'), fullPage: false });
  await page.pdf({ path: path.join(dir, 'Operational-Process-Tree_2026-10-12.pdf'), width: W + 'px', height: H + 'px', printBackground: true, pageRanges: '1' });
  const fonts = await page.evaluate(() => [...document.fonts].map(f => f.family + ' ' + f.status));
  console.log('fonts seen by page:', fonts.length ? fonts.join('; ') : '(system fonts only)');
  await browser.close();
  console.log('rendered PNG + PDF');
})().catch(e => { console.error(e); process.exit(1); });
