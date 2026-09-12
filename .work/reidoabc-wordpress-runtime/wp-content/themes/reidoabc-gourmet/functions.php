<?php
/** Rei do ABC gourmet child theme. */
declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

define('REIDOABC_GOURMET_VERSION', '13.0.0');

add_action('wp_enqueue_scripts', static function (): void {
    wp_enqueue_style('storely-parent-style', get_template_directory_uri() . '/style.css', [], REIDOABC_GOURMET_VERSION);
    wp_enqueue_style('reidoabc-gourmet-style', get_stylesheet_uri(), ['storely-parent-style'], REIDOABC_GOURMET_VERSION);
    wp_enqueue_script('reidoabc-carousel', get_stylesheet_directory_uri() . '/assets/js/carousel.js', [], REIDOABC_GOURMET_VERSION, true);
    wp_enqueue_script('reidoabc-checkout-enhancements', get_stylesheet_directory_uri() . '/assets/js/checkout-native.js', [], REIDOABC_GOURMET_VERSION, true);
    wp_localize_script('reidoabc-checkout-enhancements', 'ReiDoABCCheckout', ['viaCepEndpoint' => 'https://viacep.com.br/ws/']);
});

function reidoabc_get_hero_slide_1_url(): string {
    $replacement = get_stylesheet_directory() . '/assets/images/hero-slide-1-replacement.jpg';
    if (is_readable($replacement)) {
        return get_stylesheet_directory_uri() . '/assets/images/hero-slide-1-replacement.jpg';
    }
    return content_url('/uploads/2025/08/Banner-Pistache-2.jpg');
}

function reidoabc_gourmet_cart_label(): string {
    if (!function_exists('WC') || !WC()->cart) {
        return '0 item(s) - R$ 0,00';
    }
    return sprintf('%d item(s) - %s', WC()->cart->get_cart_contents_count(), wp_strip_all_tags(WC()->cart->get_cart_total()));
}

function reidoabc_gourmet_product_image_url(WC_Product $product): string {
    $image_id = $product->get_image_id();
    if ($image_id) {
        $image = wp_get_attachment_image_url($image_id, 'woocommerce_thumbnail');
        if ($image) {
            return $image;
        }
    }
    $fallback = (string) $product->get_meta('_reidoabc_display_image', true);
    return $fallback !== '' ? esc_url_raw($fallback) : wc_placeholder_img_src('woocommerce_thumbnail');
}

function reidoabc_gourmet_products(): array {
    if (!function_exists('wc_get_products')) {
        return [];
    }
    return wc_get_products(['status' => 'publish', 'limit' => 8, 'category' => ['pedacos-de-tortas', 'barras-de-chocolate'], 'orderby' => 'menu_order', 'order' => 'ASC']);
}
