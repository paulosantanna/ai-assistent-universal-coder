<!-- Package: 00_skills/(quality)/seo; relative command/resource examples resolve from that package or workspace root. -->

## Technical SEO

### Crawlability

**robots.txt:**

```text
# /robots.txt
User-agent: *
Allow: /

# Block admin/private areas
Disallow: /admin/
Disallow: /api/
Disallow: /private/

# Don't block resources needed for rendering
# ❌ Disallow: /static/

Sitemap: https://example.com/sitemap.xml
```

**Meta robots:**

```html
<!-- Default: indexable, followable -->
<meta name="robots" content="index, follow" />

<!-- Noindex specific pages -->
<meta name="robots" content="noindex, nofollow" />

<!-- Indexable but don't follow links -->
<meta name="robots" content="index, nofollow" />

<!-- Control snippets -->
<meta name="robots" content="max-snippet:150, max-image-preview:large" />
```

**Canonical URLs:**

```html
<!-- Prevent duplicate content issues -->
<link rel="canonical" href="https://example.com/page" />

<!-- Self-referencing canonical (recommended) -->
<link rel="canonical" href="https://example.com/current-page" />

<!-- For paginated content -->
<link rel="canonical" href="https://example.com/products" />
<!-- Or use rel="prev" / rel="next" for explicit pagination -->
```

### XML sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/products</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Sitemap best practices:**

- Maximum 50,000 URLs or 50MB per sitemap
- Use sitemap index for larger sites
- Include only canonical, indexable URLs
- Update `lastmod` when content changes
- Submit to Google Search Console

### URL structure

```
✅ Good URLs:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ Poor URLs:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**URL guidelines:**

- Use hyphens, not underscores
- Lowercase only
- Keep short (< 75 characters)
- Include target keywords naturally
- Avoid parameters when possible
- Use HTTPS always

### HTTPS & security

```html
<!-- Ensure all resources use HTTPS -->
<img src="https://example.com/image.jpg" />

<!-- Not: -->
<img src="http://example.com/image.jpg" />
```

**Security headers for SEO trust signals:**

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

---
