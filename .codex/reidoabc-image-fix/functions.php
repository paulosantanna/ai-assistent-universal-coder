<?php
/**
 * Theme Name: Storely Child Rei do ABC (Gourmet Cream & Black Mode)
 * Description: Tema filho gourmet do Rei do ABC com vitrine integrada ao WordPress e WooCommerce.
 * Version: 12.1.0
 * Author: Rei do ABC Team
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

const REIDOABC_THEME_VERSION = '12.1.0';

function reidoabc_theme_asset(string $relative): string
{
    return get_stylesheet_directory_uri() . '/assets/' . ltrim($relative, '/');
}

function reidoabc_logo_url(): string
{
    return reidoabc_theme_asset('images/logo-rei-do-abc.svg');
}

function reidoabc_product_image_url(WC_Product $product, string $size = 'woocommerce_thumbnail'): string
{
    $image_id = $product->get_image_id();
    if ($image_id) {
        $image_url = wp_get_attachment_image_url($image_id, $size);
        if (is_string($image_url) && $image_url !== '') {
            return $image_url;
        }
    }

    $asset = has_term('barras-de-chocolate', 'product_cat', $product->get_id())
        ? 'product-chocolate.svg'
        : 'product-cake.svg';

    return reidoabc_theme_asset('images/' . $asset);
}

function reidoabc_brand_profile(): array
{
    return [
        'name' => 'Rei do ABC',
        'street' => 'R. André Capretz Filho, 16',
        'neighborhood' => 'Rudge Ramos',
        'city' => 'São Bernardo do Campo',
        'region' => 'SP',
        'postal' => '09626-120',
        'country' => 'BR',
        'phone' => '+55 11 94894-8977',
        'phone_link' => 'tel:+5511948948977',
        'email' => 'contato@reidoabc.com.br',
        'hours' => 'Seg à Dom, 11:30 às 22:00',
        'whatsapp' => 'https://api.whatsapp.com/send?phone=5511948948977',
        'maps' => 'https://www.google.com/maps/search/?api=1&query=' . rawurlencode('R. André Capretz Filho, 16, Rudge Ramos, São Bernardo do Campo, SP, 09626-120'),
        'ifood' => 'https://www.ifood.com.br/busca?q=Rei%20do%20ABC',
        'instagram' => 'https://instagram.com/reidoabc',
        'youtube' => 'https://youtube.com/@reidoabc',
        'tiktok' => 'https://www.tiktok.com/@reidoabc',
        'description' => 'Confeitaria gourmet em São Bernardo do Campo: pedaços de tortas, barras de chocolate e food service com envio para todo o Brasil.',
    ];
}

function reidoabc_asset_version(string $relative): string
{
    $path = get_stylesheet_directory() . '/assets/' . ltrim($relative, '/');
    return file_exists($path) ? (string) filemtime($path) : REIDOABC_THEME_VERSION;
}

function reidoabc_local_image_url(string $filename, string $fallback): string
{
    $path = get_stylesheet_directory() . '/assets/images/' . $filename;
    if (file_exists($path)) {
        return get_stylesheet_directory_uri() . '/assets/images/' . $filename;
    }

    return $fallback;
}

function reidoabc_get_hero_slide_1_url(): string
{
    return reidoabc_local_image_url('hero-slide-1.jpg', reidoabc_theme_asset('images/hero-slide-chocolate.svg'));
}

function reidoabc_hero_slides(): array
{
    return [
        [
            'url' => reidoabc_get_hero_slide_1_url(),
            'alt' => 'Barras de chocolate gourmet Rei do ABC',
            'title' => 'Barras de Chocolate Gourmet 1Kg',
            'text' => 'Produzidas com cacau nobre selecionado e pistaches torrados em alta temperatura.',
        ],
        [
            'url' => reidoabc_local_image_url('hero-slide-2.jpg', reidoabc_theme_asset('images/hero-slide-torta.svg')),
            'alt' => 'Pedaços de tortas gourmet Rei do ABC',
            'title' => 'Pedaços de Tortas Gourmet Selecionadas',
            'text' => 'Fatias generosas com massa artesanal sablée e recheios cremosos de receita secreta.',
        ],
        [
            'url' => reidoabc_local_image_url('hero-slide-3.jpg', reidoabc_theme_asset('images/hero-slide-limited.svg')),
            'alt' => 'Edição limitada barra 1kg Rei do ABC',
            'title' => 'Edição Limitada Rei do ABC - Barra 1Kg',
            'text' => 'Chocolate nobre recheado com praliné artesanal e avelãs inteiras.',
        ],
    ];
}

function reidoabc_category_url(string $slug): string
{
    $term = get_term_by('slug', $slug, 'product_cat');
    if ($term instanceof WP_Term) {
        $link = get_term_link($term);
        if (!is_wp_error($link)) {
            return $link;
        }
    }

    return function_exists('wc_get_page_permalink') ? (string) wc_get_page_permalink('shop') : home_url('/');
}

add_action('after_setup_theme', static function (): void {
    add_theme_support('title-tag');
    add_theme_support('html5', ['search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script']);
    add_theme_support('woocommerce');
});

add_action('wp_enqueue_scripts', static function (): void {
    $layout_path = 'css/gourmet-layout.css';

    wp_enqueue_style('reidoabc-outfit', reidoabc_theme_asset('css/fonts.css'), [], reidoabc_asset_version('css/fonts.css'));
    wp_enqueue_style('storely-parent-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('storely-child-style', get_stylesheet_directory_uri() . '/style.css', ['storely-parent-style', 'reidoabc-outfit'], REIDOABC_THEME_VERSION);
    wp_enqueue_style('reidoabc-gourmet-layout', reidoabc_theme_asset($layout_path), ['storely-child-style'], reidoabc_asset_version($layout_path));
    wp_enqueue_script('reidoabc-carousel', reidoabc_theme_asset('js/carousel.js'), [], reidoabc_asset_version('js/carousel.js'), true);
    wp_enqueue_script('reidoabc-category-navigation', reidoabc_theme_asset('js/category-navigation.js'), [], reidoabc_asset_version('js/category-navigation.js'), true);

    wp_dequeue_style('storely-fonts');

    if (is_front_page()) {
        wp_dequeue_style('storely-parent-style');
        wp_dequeue_style('storely-main');
        wp_dequeue_style('storely-widgets');
        wp_dequeue_style('owl-carousel-min');
        wp_dequeue_style('tiny-slider');
        wp_dequeue_style('animate');
        wp_dequeue_style('storely-meanmenu');
        wp_dequeue_script('owl-carousel');
        wp_dequeue_script('owlcarousel2-filter');
        wp_dequeue_script('tiny-slider');
        wp_dequeue_script('isotope-pkgd');
        wp_dequeue_script('wow-min');
        wp_dequeue_script('storely-meanmenu');
    }
}, 100);

add_filter('query_vars', static function (array $query_vars): array {
    if (!in_array('reidoabc_product_category', $query_vars, true)) {
        $query_vars[] = 'reidoabc_product_category';
    }

    return $query_vars;
});

add_action('woocommerce_product_query', static function (WP_Query $query): void {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }

    $slug = $query->get('reidoabc_product_category');
    if (!is_string($slug) || $slug === '') {
        return;
    }

    $term = get_term_by('slug', sanitize_title($slug), 'product_cat');
    if (!$term instanceof WP_Term) {
        return;
    }

    $tax_query = (array) $query->get('tax_query');
    $tax_query[] = [
        'taxonomy' => 'product_cat',
        'field' => 'term_id',
        'terms' => [$term->term_id],
    ];
    $query->set('tax_query', $tax_query);
});

add_filter('woocommerce_placeholder_img_src', static function (): string {
    return reidoabc_theme_asset('images/product-cake.svg');
});

add_filter('woocommerce_product_get_image', static function (string $image, WC_Product $product, string|array $size, array $attributes, bool $placeholder): string {
    if (!$placeholder || $product->get_image_id()) {
        return $image;
    }

    $attributes['src'] = reidoabc_product_image_url($product, is_string($size) ? $size : 'woocommerce_thumbnail');
    $attributes['alt'] = $attributes['alt'] ?? $product->get_name();
    $attributes['class'] = $attributes['class'] ?? 'attachment-woocommerce_thumbnail size-woocommerce_thumbnail';
    $attributes['loading'] = $attributes['loading'] ?? 'lazy';
    $attributes['decoding'] = $attributes['decoding'] ?? 'async';

    return '<img ' . wc_implode_html_attributes($attributes) . '>';
}, 10, 5);

add_filter('document_title_parts', static function (array $parts): array {
    if (is_front_page()) {
        $parts['title'] = 'Rei do ABC';
        $parts['tagline'] = 'Confeitaria gourmet em São Bernardo do Campo';
    }

    return $parts;
});

add_action('wp_head', static function (): void {
    $brand = reidoabc_brand_profile();
    $title = wp_get_document_title();
    $description = $brand['description'];
    $image = reidoabc_logo_url();
    $url = home_url('/');

    if (function_exists('is_product') && is_product()) {
        $product = wc_get_product(get_the_ID());
        if ($product instanceof WC_Product) {
            $description = wp_strip_all_tags($product->get_short_description() ?: $product->get_name());
            $image_id = $product->get_image_id();
            if ($image_id) {
                $image = (string) wp_get_attachment_image_url($image_id, 'large');
            }
            $url = get_permalink();
        }
    }

    printf('<meta name="description" content="%s">' . "\n", esc_attr($description));
    printf('<meta name="theme-color" content="#07070a">' . "\n");
    printf('<link rel="canonical" href="%s">' . "\n", esc_url($url));
    printf('<meta property="og:locale" content="pt_BR">' . "\n");
    printf('<meta property="og:type" content="%s">' . "\n", (function_exists('is_product') && is_product()) ? 'product' : 'website');
    printf('<meta property="og:title" content="%s">' . "\n", esc_attr($title));
    printf('<meta property="og:description" content="%s">' . "\n", esc_attr($description));
    printf('<meta property="og:url" content="%s">' . "\n", esc_url($url));
    printf('<meta property="og:image" content="%s">' . "\n", esc_url($image));
    printf('<meta name="twitter:card" content="summary_large_image">' . "\n");

    if (is_front_page()) {
        $lcp = reidoabc_get_hero_slide_1_url();
        printf('<link rel="preload" as="image" href="%s">' . "\n", esc_url($lcp));

        $schema = [
            '@context' => 'https://schema.org',
            '@type' => 'Bakery',
            'name' => $brand['name'],
            'url' => home_url('/'),
            'image' => $image,
            'telephone' => $brand['phone'],
            'email' => $brand['email'],
            'address' => [
                '@type' => 'PostalAddress',
                'streetAddress' => $brand['street'],
                'addressLocality' => $brand['city'],
                'addressRegion' => $brand['region'],
                'postalCode' => $brand['postal'],
                'addressCountry' => $brand['country'],
            ],
            'openingHours' => 'Mo-Su 11:30-22:00',
            'servesCuisine' => 'Gourmet desserts',
            'sameAs' => [$brand['instagram'], $brand['youtube'], $brand['tiktok']],
        ];
        echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "</script>\n";
    }

    if (function_exists('is_product') && is_product()) {
        $product = wc_get_product(get_the_ID());
        if ($product instanceof WC_Product) {
            $offer = [
                '@context' => 'https://schema.org',
                '@type' => 'Product',
                'name' => $product->get_name(),
                'image' => $image,
                'description' => $description,
                'offers' => [
                    '@type' => 'Offer',
                    'url' => get_permalink(),
                    'priceCurrency' => get_woocommerce_currency(),
                    'price' => $product->get_price(),
                    'availability' => $product->is_in_stock() ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
                ],
            ];
            echo '<script type="application/ld+json">' . wp_json_encode($offer, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "</script>\n";
        }
    }
}, 5);
