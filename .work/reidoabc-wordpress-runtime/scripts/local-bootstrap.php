<?php
declare(strict_types=1);

define('WP_INSTALLING', true);
require '/var/www/html/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
require_once ABSPATH . 'wp-admin/includes/plugin.php';
require_once ABSPATH . 'wp-admin/includes/theme.php';

$password = getenv('REIDOABC_BOOTSTRAP_ADMIN_PASSWORD');
if (!is_string($password) || $password === '') {
    fwrite(STDERR, "Bootstrap password unavailable.\n");
    exit(1);
}

global $wpdb;
$options_table_exists = $wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s', $wpdb->options)) === $wpdb->options;
if (!$options_table_exists || get_option('siteurl') === false) {
    wp_install('Rei do ABC Local', 'reidoabc_admin', 'local@example.test', 0, '', $password, 'pt_BR');
}

$user = get_user_by('login', 'reidoabc_admin');
if ($user) {
    wp_set_password($password, $user->ID);
}

foreach (['woocommerce/woocommerce.php', 'reidoabc-commerce/reidoabc-commerce.php'] as $plugin) {
    if (!is_plugin_active($plugin)) {
        $result = activate_plugin($plugin);
        if (is_wp_error($result)) {
            throw new RuntimeException($result->get_error_message());
        }
    }
}

if (class_exists('WC_Install')) {
    WC_Install::create_pages();
}

switch_theme('reidoabc-gourmet');
update_option('home', getenv('WORDPRESS_HOME'));
update_option('siteurl', getenv('WORDPRESS_SITEURL'));
update_option('permalink_structure', '/%postname%/');
update_option('woocommerce_enable_guest_checkout', 'yes');
update_option('woocommerce_enable_signup_and_login_from_checkout', 'yes');
update_option('woocommerce_enable_myaccount_registration', 'yes');
update_option('woocommerce_currency', 'BRL');
update_option('woocommerce_feature_custom_order_tables_enabled', 'yes');
update_option('woocommerce_custom_orders_table_data_sync_enabled', 'yes');
update_option('woocommerce_reidoabc_pix_settings', [
    'enabled' => 'yes',
    'title' => 'PIX',
    'instructions' => 'Seu pedido foi registrado. Use a chave abaixo e aguarde a confirmação do pagamento.',
    'pix_key' => 'pix-local@reidoabc.test',
]);

$front = get_page_by_path('inicio');
$front_id = $front ? (int) $front->ID : wp_insert_post([
    'post_title' => 'Início',
    'post_name' => 'inicio',
    'post_status' => 'publish',
    'post_type' => 'page',
]);
update_option('show_on_front', 'page');
update_option('page_on_front', $front_id);

$categories = [];
foreach (['pedacos-de-tortas' => 'Pedaços de Tortas', 'barras-de-chocolate' => 'Barras de Chocolate'] as $slug => $name) {
    $term = get_term_by('slug', $slug, 'product_cat');
    if (!$term) {
        $created = wp_insert_term($name, 'product_cat', ['slug' => $slug]);
        if (is_wp_error($created)) {
            throw new RuntimeException($created->get_error_message());
        }
        $categories[$slug] = (int) $created['term_id'];
    } else {
        $categories[$slug] = (int) $term->term_id;
    }
}

$catalog = [
    ['Pedaço de Torta Holandesa Premium', '18.90', 'pedacos-de-tortas', 'product-1.jpg'],
    ['Pedaço de Torta de Limão Gourmet', '16.50', 'pedacos-de-tortas', 'product-2.jpg'],
    ['Pedaço de Torta Red Velvet', '19.90', 'pedacos-de-tortas', 'product-3.jpg'],
    ['Pedaço de Banoffee Pie Rei do ABC', '17.90', 'pedacos-de-tortas', 'product-4.jpg'],
    ['Barra de Chocolate Amargo 70% com Pistache', '28.00', 'barras-de-chocolate', 'product-5.jpg'],
    ['Barra de Chocolate ao Leite com Avelã', '26.50', 'barras-de-chocolate', 'product-6.jpg'],
    ['Barra de Chocolate Branco com Frutas Vermelhas', '24.90', 'barras-de-chocolate', 'product-7.jpg'],
    ['Barra de Chocolate Caramelo Flor de Sal', '27.50', 'barras-de-chocolate', 'product-8.jpg'],
];

foreach ($catalog as $position => [$name, $price, $category, $image]) {
    $sku = 'LOCAL-' . ($position + 1);
    $id = wc_get_product_id_by_sku($sku);
    $product = $id ? wc_get_product($id) : new WC_Product_Simple();
    $product->set_name($name);
    $product->set_sku($sku);
    $product->set_regular_price($price);
    $product->set_price($price);
    $product->set_status('publish');
    $product->set_catalog_visibility('visible');
    $product->set_category_ids([$categories[$category]]);
    $product->set_manage_stock(true);
    $product->set_stock_quantity(100);
    $product->set_stock_status('instock');
    $product->set_menu_order($position);
    $product->update_meta_data('_reidoabc_display_image', content_url('/uploads/seed-products/' . $image));
    $product->save();
}

flush_rewrite_rules();
echo "Local WordPress bootstrap complete.\n";
