const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 2048, height: 2048 } });
  await p.goto('file://' + __dirname + '/curtain.svg');
  await p.screenshot({ path: __dirname + '/curtain.png' });
  await b.close();
})();
