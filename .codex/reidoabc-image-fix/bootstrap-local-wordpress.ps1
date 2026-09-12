$ErrorActionPreference = 'Stop'

$adminPassword = $env:REIDOABC_LOCAL_ADMIN_PASSWORD
if ([string]::IsNullOrWhiteSpace($adminPassword)) {
    $bytes = [byte[]]::new(24)
    [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
    $adminPassword = [Convert]::ToBase64String($bytes)
}
$env:REIDOABC_BOOTSTRAP_ADMIN_PASSWORD = $adminPassword

$installPhp = @'
<?php
define('WP_INSTALLING', true);
require '/var/www/html/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/upgrade.php';

$admin_password = getenv('REIDOABC_BOOTSTRAP_ADMIN_PASSWORD');
if (!$admin_password) {
    fwrite(STDERR, "Missing local bootstrap admin password.\n");
    exit(1);
}

if (!is_blog_installed()) {
    wp_install(
        'Rei do ABC Local',
        'reidoabc_admin',
        'local@example.test',
        0,
        '',
        $admin_password,
        'pt_BR'
    );
    echo "installed\n";
    exit;
}

echo "already-installed\n";
'@

$configurePhp = @'
<?php
require '/var/www/html/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/plugin.php';
require_once ABSPATH . 'wp-admin/includes/theme.php';

$local_url = getenv('WORDPRESS_HOME') ?: 'http://localhost:8087';
update_option('home', $local_url);
update_option('siteurl', $local_url);
update_option('woocommerce_currency', 'BRL');

$plugins = [
    'woocommerce/woocommerce.php',
    'reidoabc-site-controls/reidoabc-site-controls.php',
    'reidoabc-commerce-runtime/reidoabc-commerce-runtime.php',
];

foreach ($plugins as $plugin) {
    if (file_exists(WP_PLUGIN_DIR . '/' . $plugin) && !is_plugin_active($plugin)) {
        $result = activate_plugin($plugin);
        if (is_wp_error($result)) {
            fwrite(STDERR, $plugin . ': ' . $result->get_error_message() . "\n");
            exit(1);
        }
        echo "activated-plugin=$plugin\n";
    }
}

$theme = wp_get_theme('reidoabc-gourmet-reference');
if ($theme->exists()) {
    switch_theme('reidoabc-gourmet-reference');
    echo "theme=reidoabc-gourmet-reference\n";
}

$content = <<<'HTML'
<!-- wp:group {"className":"reidoabc-local-home"} -->
<div class="wp-block-group reidoabc-local-home">
<!-- wp:image {"sizeSlug":"full","className":"reidoabc-local-hero"} -->
<figure class="wp-block-image size-full reidoabc-local-hero"><img src="/wp-content/uploads/2025/08/Banner-Pistache-2.jpg" alt="Primeiro slide mapeado do Rei do ABC" data-replacement-slot="/wp-content/themes/reidoabc-gourmet-reference/assets/images/hero-slide-1.jpg"/></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2>Redes Sociais</h2>
<!-- /wp:heading -->

<!-- wp:shortcode -->
[reidoabc_encomendas_brasil context="home"]
<!-- /wp:shortcode -->

<!-- wp:heading -->
<h2>Produtos selecionados</h2>
<!-- /wp:heading -->

<!-- wp:shortcode -->
[reidoabc_product_table]
<!-- /wp:shortcode -->
</div>
<!-- /wp:group -->
HTML;

$page = get_page_by_path('rei-do-abc-local-preview');
$page_id = $page ? (int) $page->ID : 0;
$postarr = [
    'ID' => $page_id,
    'post_title' => 'Rei do ABC Local Preview',
    'post_name' => 'rei-do-abc-local-preview',
    'post_status' => 'publish',
    'post_type' => 'page',
    'post_content' => $content,
];

$page_id = wp_insert_post($postarr, true);
if (is_wp_error($page_id)) {
    fwrite(STDERR, $page_id->get_error_message() . "\n");
    exit(1);
}

update_option('show_on_front', 'page');
update_option('page_on_front', (int) $page_id);
update_option('permalink_structure', '/%postname%/');
flush_rewrite_rules();

echo "front-page=$page_id\n";
'@

$installPhp | docker compose exec -T -e REIDOABC_BOOTSTRAP_ADMIN_PASSWORD wordpress php
$configurePhp | docker compose exec -T wordpress php

$seedProductsPhp = @'
<?php
require '/var/www/html/wp-load.php';

if (!class_exists('WC_Product_Simple')) {
    fwrite(STDERR, "WooCommerce is not available for local catalog seed.\n");
    exit(1);
}

$categories = [
    'pedacos-de-tortas' => 'Pedaços de Tortas',
    'barras-de-chocolate' => 'Barras de Chocolate',
];
$categoryIds = [];
foreach ($categories as $slug => $name) {
    $term = get_term_by('slug', $slug, 'product_cat');
    if (!$term) {
        $created = wp_insert_term($name, 'product_cat', ['slug' => $slug]);
        if (is_wp_error($created)) {
            fwrite(STDERR, $created->get_error_message() . "\n");
            exit(1);
        }
        $categoryIds[$slug] = (int) $created['term_id'];
        continue;
    }
    $categoryIds[$slug] = (int) $term->term_id;
}

function reidoabc_local_demo_image_id(string $filename, string $title): int {
    static $image_ids = [];

    if (isset($image_ids[$filename])) {
        return $image_ids[$filename];
    }

    $existing = get_posts([
        'post_type' => 'attachment',
        'post_status' => 'inherit',
        'posts_per_page' => 1,
        'fields' => 'ids',
        'meta_key' => '_reidoabc_local_demo_asset',
        'meta_value' => $filename,
    ]);
    if ($existing) {
        return $image_ids[$filename] = (int) $existing[0];
    }

    $source = get_stylesheet_directory() . '/assets/images/' . $filename;
    if (!is_readable($source)) {
        fwrite(STDERR, "Missing local product SVG: $filename\n");
        exit(1);
    }

    $uploads = wp_upload_dir();
    $directory = trailingslashit($uploads['basedir']) . 'reidoabc-demo';
    if (!wp_mkdir_p($directory)) {
        fwrite(STDERR, "Unable to create local product image directory.\n");
        exit(1);
    }

    $destination = trailingslashit($directory) . $filename;
    if (!file_exists($destination) || md5_file($source) !== md5_file($destination)) {
        if (!copy($source, $destination)) {
            fwrite(STDERR, "Unable to copy local product SVG: $filename\n");
            exit(1);
        }
    }

    $attachment_id = wp_insert_attachment([
        'post_mime_type' => 'image/svg+xml',
        'post_title' => $title,
        'post_status' => 'inherit',
    ], $destination);
    if (is_wp_error($attachment_id)) {
        fwrite(STDERR, $attachment_id->get_error_message() . "\n");
        exit(1);
    }

    update_attached_file($attachment_id, $destination);
    wp_update_attachment_metadata($attachment_id, [
        'width' => 1200,
        'height' => 960,
        'file' => _wp_relative_upload_path($destination),
        'sizes' => [
            'woocommerce_thumbnail' => [
                'file' => $filename,
                'width' => 600,
                'height' => 480,
                'mime-type' => 'image/svg+xml',
            ],
        ],
    ]);
    update_post_meta($attachment_id, '_wp_attachment_image_alt', $title);
    update_post_meta($attachment_id, '_reidoabc_local_demo_asset', $filename);

    return $image_ids[$filename] = (int) $attachment_id;
}

// Local-only seed mirroring the storefront's former static cards. Never use as production catalog data.
$products = [
    ['local-demo-torta-holandesa', 'Pedaço de Torta Holandesa Premium', '18.90', 'pedacos-de-tortas'],
    ['local-demo-torta-limao', 'Pedaço de Torta de Limão Gourmet', '16.50', 'pedacos-de-tortas'],
    ['local-demo-torta-red-velvet', 'Pedaço de Torta Red Velvet com Cream Cheese', '19.90', 'pedacos-de-tortas'],
    ['local-demo-banoffee', 'Pedaço de Banoffee Pie Rei do ABC', '17.90', 'pedacos-de-tortas'],
    ['local-demo-chocolate-pistache', 'Barra de Chocolate Amargo 70% com Pistache', '28.00', 'barras-de-chocolate'],
    ['local-demo-chocolate-avela', 'Barra de Chocolate ao Leite Recheada com Avelã', '26.50', 'barras-de-chocolate'],
    ['local-demo-chocolate-frutas', 'Barra de Chocolate Branco com Frutas Vermelhas', '24.90', 'barras-de-chocolate'],
    ['local-demo-chocolate-caramelo', 'Barra de Chocolate Caramelo Flor de Sal', '27.50', 'barras-de-chocolate'],
];

foreach ($products as [$sku, $name, $price, $category]) {
    $product_id = wc_get_product_id_by_sku($sku);
    $product = $product_id ? wc_get_product($product_id) : new WC_Product_Simple();
    if (!$product instanceof WC_Product) {
        fwrite(STDERR, "Unable to load local product: $sku\n");
        exit(1);
    }

    if (!$product_id) {
        $product->set_name($name);
        $product->set_sku($sku);
        $product->set_regular_price($price);
        $product->set_price($price);
        $product->set_status('publish');
        $product->set_catalog_visibility('visible');
        $product->set_stock_status('instock');
        $product->set_category_ids([$categoryIds[$category]]);
        $product_id = $product->save();
        echo "seeded-product=$sku\n";
    }

    if (!$product->get_image_id()) {
        $asset = $category === 'barras-de-chocolate' ? 'product-chocolate.svg' : 'product-cake.svg';
        $product->set_image_id(reidoabc_local_demo_image_id($asset, $name));
        $product->save();
        echo "assigned-product-image=$sku\n";
    }
}
'@

$seedProductsPhp | docker compose exec -T wordpress php

Write-Output 'Local WordPress bootstrap complete.'
Write-Output 'URL: http://localhost:8087/'
Write-Output 'Local admin user: reidoabc_admin'
if ([string]::IsNullOrWhiteSpace($env:REIDOABC_LOCAL_ADMIN_PASSWORD)) {
    Write-Output 'Admin password was generated in memory. Set REIDOABC_LOCAL_ADMIN_PASSWORD before a fresh bootstrap if you need an explicit local password.'
}
