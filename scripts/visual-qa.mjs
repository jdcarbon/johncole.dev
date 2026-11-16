import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.env.QA_BASE || 'http://127.0.0.1:4321';
const OUT = path.resolve('tmp/visual-qa');
fs.mkdirSync(OUT, { recursive: true });

const widths = [360, 390, 430, 768, 1024, 1280, 1600];
const pages = [
  { name: 'home', path: '/' },
  { name: 'work', path: '/work/' },
  { name: 'teaching', path: '/teaching/' },
  { name: 'hdse', path: '/hdse/' },
  { name: 'about', path: '/about/' },
  { name: 'lesson-intro', path: '/teaching/lessons/functions-and-testing/' },
  { name: 'lesson-code', path: '/teaching/lessons/evaluating-ai-code/' },
];

const allowedOverflow = new Set(['HTML', 'BODY', 'MAIN']);

function isIntentionallyScrollable(el) {
  const style = window.getComputedStyle(el);
  const ox = style.overflowX;
  return (ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth + 1;
}

const browser = await chromium.launch();
const report = [];

for (const width of widths) {
  const context = await browser.newContext({
    viewport: { width, height: 900 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  for (const route of pages) {
    const url = BASE + route.path;
    await page.goto(url, { waitUntil: 'networkidle' });

    // Open mobile menu when present and assert links exist
    const menuVisible = await page.locator('.navtoggle').isVisible().catch(() => false);
    if (menuVisible && width < 900) {
      await page.locator('.navtoggle').click();
      await page.waitForSelector('.navmenu[open] .navpanel a');
    }

    const metrics = await page.evaluate(({ allowed }) => {
      const docOverflow = document.documentElement.scrollWidth > window.innerWidth + 1;
      const overflowing = [...document.querySelectorAll('*')].filter((el) => {
        if (allowed.includes(el.tagName)) return false;
        if (el.closest('.code-frame, .datatable-wrap, .navpanel')) return false;
        const style = window.getComputedStyle(el);
        const ox = style.overflowX;
        if ((ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth + 1) return false;
        const rect = el.getBoundingClientRect();
        return rect.right > window.innerWidth + 1 || rect.left < -1;
      }).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName,
          className: String(el.className || '').slice(0, 80),
          right: Math.round(rect.right),
          width: Math.round(rect.width),
        };
      });

      const bodyFont = window.getComputedStyle(document.body).fontSize;
      const h1 = document.querySelector('h1');
      const h1Size = h1 ? window.getComputedStyle(h1).fontSize : null;
      return {
        docOverflow,
        scrollWidth: document.documentElement.scrollWidth,
        innerWidth: window.innerWidth,
        overflowing: overflowing.slice(0, 12),
        bodyFont,
        h1Size,
      };
    }, { allowed: [...allowedOverflow] });

    const shotName = `${route.name}-${width}.png`;
    // Representative screenshots only for key widths
    if ([360, 768, 1280].includes(width)) {
      await page.screenshot({
        path: path.join(OUT, shotName),
        fullPage: false,
      });
    }

    report.push({
      page: route.name,
      width,
      ...metrics,
      menuVisible,
    });

    if (menuVisible && width < 900) {
      // close for next navigation cleanliness
      await page.locator('.navtoggle').click().catch(() => {});
    }
  }

  await context.close();
}

await browser.close();

const problems = report.filter((r) => r.docOverflow || r.overflowing.length > 0);
fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify({ report, problems }, null, 2));
console.log(`Checked ${report.length} page/width combos`);
console.log(`Problems: ${problems.length}`);
for (const p of problems.slice(0, 40)) {
  console.log(`- ${p.page} @${p.width}: docOverflow=${p.docOverflow} elements=${p.overflowing.length}`, p.overflowing[0] || '');
}
if (problems.length === 0) console.log('No document-level overflow detected.');
console.log(`Screenshots/report in ${OUT}`);
