# Rei do ABC WordPress Mapping

Updated: 2026-09-11

## Remote Site

- Canonical URL: https://reidoabc.com.br
- Admin URL requested: https://reidoabc.com.br/wp-admin
- Derived site_id: 3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5
- Existing AEOS Beta Map: `.aeos/wordpress/sites/3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5/beta-map.json`

## Auth Status

Authenticated wp-admin access is blocked in this run. The requested `.txt` cookie file was not present, and the nearest file was not a cookie jar. It contained plaintext credentials, so it was not used as a cookie session source. Rotate those credentials before continuing production work.

## Publicly Verified Surfaces

- Home: HTTP 200.
- REST index: HTTP 200.
- `readme.html`: HTTP 200 and should be blocked.
- `/wp-content/`: HTTP 200 with empty body.
- `/wp-content/themes/storely/`: HTTP 200 with small body, no useful directory listing.
- `/wp-content/uploads/`: HTTP 403.

## Detected Stack

- WordPress core: 7.1 inferred from public map and asset versioning.
- Active theme in production: Storely 7.1.
- Local clone target theme: Storely 29.2 from WordPress.org, to move away from vulnerable Storely <= 18 releases.
- WooCommerce in production: 10.3.8.
- Local clone target WooCommerce: 11.1.0.
- Public catalog categories detected: Cremes, Caldas, Food Service.
- Requested allowed product groups: Pedaços de Tortas and Barras de Chocolate.

## Carousel

- Current first slide: `/wp-content/uploads/2025/08/Banner-Pistache-2.jpg`
- Replacement slot: `/wp-content/themes/reidoabc-storely-child/assets/images/hero-slide-1-replacement.jpg`
- Status: mapped and waiting for the final image choice.

## Clone Limits

This repository includes public content, public uploads referenced by REST/homepage, official WordPress core, official Storely, WooCommerce and Akismet packages, plus custom production-ready theme/plugin overrides. It does not include the production database dump, private uploads not referenced publicly, premium/custom plugin code, or hosting-only PHP files because no authenticated backup/FTP/SFTP/hosting access was available.
