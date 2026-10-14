<!-- Package: 00_skills/(web-automation)/playwright-skill; relative command/resource examples resolve from that package or workspace root. -->

## Execution Pattern

**Step 1: Detect dev servers (for localhost testing)**

```bash
cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
```

**Step 2: Write test script to /tmp with URL parameter**

```javascript
// /tmp/playwright-test-page.js
const { chromium } = require('playwright')

// Parameterized URL (detected or user-provided)
const TARGET_URL = 'http://localhost:3001' // <-- Auto-detected or from user

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto(TARGET_URL)
  console.log('Page loaded:', await page.title())

  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true })
  console.log('📸 Screenshot saved to /tmp/screenshot.png')

  await browser.close()
})()
```

**Step 3: Execute from skill directory**

```bash
cd $SKILL_DIR && node run.js /tmp/playwright-test-page.js
```
