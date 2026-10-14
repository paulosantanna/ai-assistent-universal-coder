<!-- Package: 00_skills/(web-automation)/playwright-skill; relative command/resource examples resolve from that package or workspace root. -->

## Common Patterns

### Test a Page (Multiple Viewports)

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3001' // Auto-detected

;(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 })
  const page = await browser.newPage()

  // Desktop test
  await page.setViewportSize({ width: 1920, height: 1080 })
  await page.goto(TARGET_URL)
  console.log('Desktop - Title:', await page.title())
  await page.screenshot({ path: '/tmp/desktop.png', fullPage: true })

  // Mobile test
  await page.setViewportSize({ width: 375, height: 667 })
  await page.screenshot({ path: '/tmp/mobile.png', fullPage: true })

  await browser.close()
})()
```

### Test Login Flow

```javascript
// /tmp/playwright-test-login.js
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3001' // Auto-detected
// SECURITY: Use environment variables for credentials
const TEST_EMAIL = process.env.TEST_EMAIL || 'test@example.com'
const TEST_PASSWORD = process.env.TEST_PASSWORD || 'test-password'

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto(`${TARGET_URL}/login`)

  await page.fill('input[name="email"]', TEST_EMAIL)
  await page.fill('input[name="password"]', TEST_PASSWORD)
  await page.click('button[type="submit"]')

  // Wait for redirect
  await page.waitForURL('**/dashboard')
  console.log('✅ Login successful, redirected to dashboard')

  await browser.close()
})()
```

**Execute with credentials:**

```bash
TEST_EMAIL=user@example.com TEST_PASSWORD=secure123 \
  cd $SKILL_DIR && node run.js /tmp/playwright-test-login.js
```

### Fill and Submit Form

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3001' // Auto-detected

;(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 })
  const page = await browser.newPage()

  await page.goto(`${TARGET_URL}/contact`)

  await page.fill('input[name="name"]', 'John Doe')
  await page.fill('input[name="email"]', 'john@example.com')
  await page.fill('textarea[name="message"]', 'Test message')
  await page.click('button[type="submit"]')

  // Verify submission
  await page.waitForSelector('.success-message')
  console.log('✅ Form submitted successfully')

  await browser.close()
})()
```

### Check for Broken Links

```javascript
const { chromium } = require('playwright')

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto('http://localhost:3000')

  const links = await page.locator('a[href^="http"]').all()
  const results = { working: 0, broken: [] }

  for (const link of links) {
    const href = await link.getAttribute('href')
    try {
      const response = await page.request.head(href)
      if (response.ok()) {
        results.working++
      } else {
        results.broken.push({ url: href, status: response.status() })
      }
    } catch (e) {
      results.broken.push({ url: href, error: e.message })
    }
  }

  console.log(`✅ Working links: ${results.working}`)
  console.log(`❌ Broken links:`, results.broken)

  await browser.close()
})()
```

### Take Screenshot with Error Handling

```javascript
const { chromium } = require('playwright')

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  try {
    await page.goto('http://localhost:3000', {
      waitUntil: 'networkidle',
      timeout: 10000,
    })

    await page.screenshot({
      path: '/tmp/screenshot.png',
      fullPage: true,
    })

    console.log('📸 Screenshot saved to /tmp/screenshot.png')
  } catch (error) {
    console.error('❌ Error:', error.message)
  } finally {
    await browser.close()
  }
})()
```

### Test Responsive Design

```javascript
// /tmp/playwright-test-responsive-full.js
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3001' // Auto-detected

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  const viewports = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 },
  ]

  for (const viewport of viewports) {
    console.log(`Testing ${viewport.name} (${viewport.width}x${viewport.height})`)

    await page.setViewportSize({
      width: viewport.width,
      height: viewport.height,
    })

    await page.goto(TARGET_URL)
    await page.waitForTimeout(1000)

    await page.screenshot({
      path: `/tmp/${viewport.name.toLowerCase()}.png`,
      fullPage: true,
    })
  }

  console.log('✅ All viewports tested')
  await browser.close()
})()
```
