$ErrorActionPreference = 'Stop'

$required = @(
  'index.php',
  'wp-config.php',
  'docker-compose.yml',
  'wp-content/themes/storely/style.css',
  'wp-content/themes/reidoabc-gourmet/functions.php',
  'wp-content/themes/reidoabc-gourmet/front-page.php',
  'wp-content/plugins/woocommerce/woocommerce.php',
  'wp-content/plugins/reidoabc-commerce/reidoabc-commerce.php',
  'wp-content/mu-plugins/reidoabc-hardening.php',
  'wp-content/uploads/seed-products/product-1.jpg',
  'config/production.env.example'
)

foreach ($file in $required) {
  if (-not (Test-Path -LiteralPath $file)) { throw "Missing required file: $file" }
}

$style = Get-Content -LiteralPath 'wp-content/themes/reidoabc-gourmet/style.css' -Raw
if ($style -notmatch '#302c9b') { throw 'Primary palette #302c9b is missing from the gourmet theme.' }
foreach ($oldColor in @('#d8b456', '#4a2c11', '#5c3a21', '#6f4e37', '#8b4513', '#a0522d')) {
  if ($style -match [regex]::Escape($oldColor)) { throw "Deprecated brown palette found: $oldColor" }
}

if (Test-Path -LiteralPath 'wp-content/themes/reidoabc-gourmet/assets/js/checkout.js') {
  throw 'The simulated browser checkout must not be present.'
}

if (-not (Select-String -LiteralPath 'wp-content/themes/reidoabc-gourmet/footer.php' -Pattern 'Encomendas para todo o Brasil' -Quiet)) {
  throw 'Commerce footer title is missing.'
}

Write-Output 'PASS: WordPress runtime, WooCommerce persistence, local assets, palette, secure checkout boundaries and production configuration template are present.'
