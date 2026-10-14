// Usage: node tools/shot.mjs <url> <out.png> [width] [height] [full]
import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const [url, out, w = '1280', h = '800', full] = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h } });
await p.goto(url, { waitUntil: 'load' });
await p.waitForFunction(() => !document.documentElement.classList.contains('in-full') && !document.documentElement.classList.contains('in-short'), null, { timeout: 8000 }).catch(() => {}); await p.mouse.move(900, 500); await p.waitForTimeout(600);
if (full === 'full') {
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo({top:y,behavior:'instant'}); await new Promise(r => setTimeout(r, 60)); } window.scrollTo({top:0,behavior:'instant'}); });
  await p.waitForTimeout(900);
}
await p.screenshot({ path: out, fullPage: full === 'full' });
await b.close();
