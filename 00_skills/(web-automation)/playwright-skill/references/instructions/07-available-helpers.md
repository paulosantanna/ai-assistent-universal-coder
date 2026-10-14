<!-- Package: 00_skills/(web-automation)/playwright-skill; relative command/resource examples resolve from that package or workspace root. -->

## Available Helpers

Optional utility functions in `lib/helpers.js`:

```javascript
const helpers = require('./lib/helpers')

// Detect running dev servers (CRITICAL - use this first!)
const servers = await helpers.detectDevServers()
console.log('Found servers:', servers)

// Safe click with retry
await helpers.safeClick(page, 'button.submit', { retries: 3 })

// Safe type with clear
await helpers.safeType(page, '#username', 'testuser')

// Take timestamped screenshot
await helpers.takeScreenshot(page, 'test-result')

// Handle cookie banners
await helpers.handleCookieBanner(page)

// Extract table data
const data = await helpers.extractTableData(page, 'table.results')
```

See `lib/helpers.js` for full list.
