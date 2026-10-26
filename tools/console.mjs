import { chromium } from 'playwright';
const base = process.argv[2]; const paths = process.argv.slice(3);
const b = await chromium.launch(); const p = await b.newPage(); let bad = 0;
p.on('console', m => { if (m.type() === 'error') { bad++; console.log('  console error:', m.text().slice(0, 150)); } });
p.on('pageerror', e => { bad++; console.log('  page error:', e.message); });
p.on('requestfailed', r => { bad++; console.log('  failed request:', r.url()); });
p.on('response', r => { if (r.status() >= 400 && !r.url().includes('/nope')) { bad++; console.log('  HTTP', r.status(), r.url()); } });
for (const path of paths) { console.log(path); await p.goto(base + path, { waitUntil: 'networkidle' }); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } }); await p.waitForTimeout(300); }
// homepage form: empty submit must show validation, not send
await p.goto(base + '/', { waitUntil: 'networkidle' });
await p.click('#q-submit'); const errs = await p.$$eval('.field.bad', e => e.length);
console.log('form empty-submit -> fields flagged:', errs);
// job-type preselect buttons
await p.goto(base + '/#work'); await p.click('[data-job="Storage unit cleanout"]'); console.log('preselect ->', await p.$eval('#q-type', s => s.value));
console.log(bad ? `${bad} PROBLEMS` : 'NO CONSOLE/NETWORK ERRORS'); await b.close();
