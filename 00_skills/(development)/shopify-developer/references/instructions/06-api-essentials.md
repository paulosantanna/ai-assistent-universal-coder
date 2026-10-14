<!-- Package: 00_skills/(development)/shopify-developer; relative command/resource examples resolve from that package or workspace root. -->

## API Essentials

```javascript
// GraphQL Admin - always use GraphQL over REST
const response = await fetch(`https://${store}.myshopify.com/admin/api/2026-01/graphql.json`, {
  method: 'POST',
  headers: {
    'X-Shopify-Access-Token': accessToken,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ query, variables }),
})
const { data, errors } = await response.json()
if (errors) throw new Error(errors[0].message)

// Ajax API (theme-only cart operations)
fetch('/cart/add.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id: variantId, quantity: 1 }),
})
```
