// يولّد صور OG (1200×630) والأيقونات من قوالب HTML الناتجة عن build.py
// الاستخدام: NODE_PATH=/opt/node22/lib/node_modules node tools/og.mjs
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const tmp = path.join(here, '_og');
const out = path.join(here, '..', 'site', 'assets', 'img');
fs.mkdirSync(path.join(out, 'og'), { recursive: true });

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
let n = 0;
for (const f of fs.readdirSync(tmp).filter(x => x.endsWith('.html'))) {
  await p.goto('file://' + path.join(tmp, f), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(out, 'og', f.replace('.html', '.png')) });
  n++;
}
// أيقونات
const sym = fs.readFileSync(path.join(out, 'symbol.svg'), 'utf8');
const icon = (size, pad, bg) => `<!doctype html><html><body style="margin:0;width:${size}px;height:${size}px;background:${bg};display:grid;place-items:center">
<div style="width:${size - pad * 2}px;height:${size - pad * 2}px">${sym.replace('<svg ', '<svg style="width:100%;height:100%" ')}</div></body></html>`;
for (const [name, size, pad, bg] of [['favicon-32', 32, 3, '#FAFAFA'], ['apple-touch-icon', 180, 30, '#FAFAFA'], ['icon-192', 192, 32, '#FAFAFA'], ['icon-512', 512, 86, '#FAFAFA'], ['logo-512', 512, 86, '#FAFAFA']]) {
  const q = await b.newPage({ viewport: { width: size, height: size } });
  await q.setContent(icon(size, pad, bg));
  await q.screenshot({ path: path.join(out, name + '.png') });
  await q.close();
}
await b.close();
console.log(`✓ ${n} صورة OG + الأيقونات`);
