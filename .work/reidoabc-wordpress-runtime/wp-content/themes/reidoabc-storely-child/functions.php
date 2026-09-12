<?php
declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

add_action('wp_enqueue_scripts', static function (): void {
    wp_enqueue_style(
        'storely-parent',
        get_template_directory_uri() . '/style.css',
        [],
        wp_get_theme('storely')->get('Version') ?: '29.2'
    );

    wp_enqueue_style(
        'reidoabc-storely-overrides',
        get_stylesheet_directory_uri() . '/assets/css/reidoabc-storely-overrides.css',
        ['storely-parent'],
        '1.0.0'
    );
}, 20);

function reidoabc_hero_slide_one_url(): string
{
    $replacement = get_stylesheet_directory() . '/assets/images/hero-slide-1-replacement.jpg';

    if (file_exists($replacement)) {
        return get_stylesheet_directory_uri() . '/assets/images/hero-slide-1-replacement.jpg';
    }

    return content_url('uploads/2025/08/Banner-Pistache-2.jpg');
}
