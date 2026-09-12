<?php
/**
 * Plugin Name: Rei do ABC Site Controls
 * Description: Adds Rei do ABC commerce links, product filtering, and shortcode controls without editing WordPress core.
 * Version: 1.0.0
 * Author: Rei do ABC
 * Requires at least: 7.1
 * Requires PHP: 8.2
 * Text Domain: reidoabc-site-controls
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

final class ReiDoABC_Site_Controls
{
    private const VERSION = '1.0.0';

    public function __construct()
    {
        add_action('wp_enqueue_scripts', [$this, 'enqueue_assets'], 30);
        add_action('customize_register', [$this, 'register_customizer']);
        add_shortcode('reidoabc_encomendas_brasil', [$this, 'shortcode_commerce_links']);
        add_shortcode('reidoabc_product_table', [$this, 'shortcode_product_table']);
    }

    public static function activate(): void
    {
        if (!taxonomy_exists('product_cat')) {
            return;
        }

        $terms = [
            'Pedaços de Tortas' => 'pedacos-de-tortas',
            'Barras de Chocolate' => 'barras-de-chocolate',
        ];

        foreach ($terms as $name => $slug) {
            if (!term_exists($slug, 'product_cat')) {
                wp_insert_term($name, 'product_cat', ['slug' => $slug]);
            }
        }
    }

    public function enqueue_assets(): void
    {
        wp_enqueue_style(
            'reidoabc-site-controls',
            plugins_url('assets/css/site-controls.css', __FILE__),
            [],
            self::VERSION
        );

        wp_enqueue_script(
            'reidoabc-footer-commerce-links',
            plugins_url('assets/js/footer-commerce-links.js', __FILE__),
            [],
            self::VERSION,
            true
        );

        wp_localize_script(
            'reidoabc-footer-commerce-links',
            'reiDoABCCommerceLinks',
            [
                'html' => $this->render_commerce_links('footer'),
            ]
        );
    }

    public function register_customizer(WP_Customize_Manager $customizer): void
    {
        $customizer->add_section('reidoabc_commerce_links', [
            'title' => __('Rei do ABC - Encomendas', 'reidoabc-site-controls'),
            'priority' => 160,
        ]);

        foreach ($this->default_links() as $link) {
            $settingId = 'reidoabc_link_' . $link['id'];
            $customizer->add_setting($settingId, [
                'default' => $link['url'],
                'sanitize_callback' => 'esc_url_raw',
            ]);
            $customizer->add_control($settingId, [
                'label' => $link['label'],
                'section' => 'reidoabc_commerce_links',
                'type' => 'url',
            ]);
        }
    }

    public function shortcode_commerce_links(): string
    {
        return $this->render_commerce_links('shortcode');
    }

    public function public_commerce_links(string $context = 'footer'): string
    {
        return $this->render_commerce_links($context);
    }

    public function shortcode_product_table(): string
    {
        if (!function_exists('wc_get_products')) {
            return '';
        }

        $products = wc_get_products([
            'status' => 'publish',
            'limit' => 24,
            'category' => ['pedacos-de-tortas', 'barras-de-chocolate'],
            'orderby' => 'title',
            'order' => 'ASC',
        ]);

        if (!$products) {
            return '<p class="reidoabc-products-empty">' . esc_html__('Nenhum produto público foi encontrado no catálogo atual.', 'reidoabc-site-controls') . '</p>';
        }

        ob_start();
        ?>
        <table class="reidoabc-product-table">
            <thead>
                <tr>
                    <th><?php esc_html_e('Produto', 'reidoabc-site-controls'); ?></th>
                    <th><?php esc_html_e('Categoria', 'reidoabc-site-controls'); ?></th>
                    <th><?php esc_html_e('Preço', 'reidoabc-site-controls'); ?></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($products as $product): ?>
                    <tr>
                        <td><a href="<?php echo esc_url($product->get_permalink()); ?>"><?php echo esc_html($product->get_name()); ?></a></td>
                        <td><?php echo esc_html(wc_get_product_category_list($product->get_id(), ', ', '', '')); ?></td>
                        <td><?php echo wp_kses_post($product->get_price_html()); ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php
        return (string) ob_get_clean();
    }

    private function render_commerce_links(string $context): string
    {
        $links = array_filter($this->links(), static function (array $link): bool {
            return (bool) filter_var($link['url'], FILTER_VALIDATE_URL);
        });

        if (!$links) {
            return '';
        }

        ob_start();
        ?>
        <nav class="reidoabc-commerce-links reidoabc-commerce-links--<?php echo esc_attr($context); ?>" aria-label="<?php esc_attr_e('Encomendas para todo o Brasil', 'reidoabc-site-controls'); ?>">
            <h5 class="reidoabc-commerce-links__title"><?php esc_html_e('Encomendas para todo o Brasil', 'reidoabc-site-controls'); ?></h5>
            <ul class="reidoabc-commerce-links__list">
                <?php foreach ($links as $link): ?>
                    <li class="reidoabc-commerce-links__item">
                        <a class="reidoabc-commerce-links__link" href="<?php echo esc_url($link['url']); ?>" target="_blank" rel="noopener noreferrer" aria-label="<?php echo esc_attr($link['label']); ?>" title="<?php echo esc_attr($link['label']); ?>">
                            <img class="reidoabc-commerce-links__icon" src="<?php echo esc_url($link['icon']); ?>" alt="" loading="lazy" decoding="async">
                            <span class="screen-reader-text"><?php echo esc_html($link['label']); ?></span>
                        </a>
                    </li>
                <?php endforeach; ?>
            </ul>
        </nav>
        <?php
        return (string) ob_get_clean();
    }

    private function links(): array
    {
        return array_map(function (array $link): array {
            $setting = get_theme_mod('reidoabc_link_' . $link['id'], $link['url']);
            $link['url'] = is_string($setting) ? $setting : '';
            return $link;
        }, $this->default_links());
    }

    private function default_links(): array
    {
        $base = plugin_dir_url(__FILE__) . 'assets/icons/';

        return [
            ['id' => 'mercado_livre', 'label' => 'Mercado Livre', 'url' => 'https://www.mercadolivre.com.br/', 'icon' => $base . 'mercado-livre.svg'],
            ['id' => 'mercado_pago', 'label' => 'Mercado Pago', 'url' => 'https://www.mercadopago.com.br/', 'icon' => $base . 'mercado-pago.svg'],
            ['id' => 'tiktok_store', 'label' => 'TikTok Store', 'url' => 'https://www.tiktok.com/', 'icon' => $base . 'tiktok-store.svg'],
            ['id' => 'app_99', 'label' => '99', 'url' => 'https://www.99app.com/', 'icon' => $base . '99.svg'],
            ['id' => 'ifood', 'label' => 'iFood', 'url' => 'https://www.ifood.com.br/busca?q=Rei%20do%20ABC', 'icon' => $base . 'ifood.svg'],
            ['id' => 'keeta', 'label' => 'Keeta', 'url' => 'https://www.keeta.com/', 'icon' => $base . 'keeta.svg'],
        ];
    }
}

function reidoabc_render_commerce_links(string $context = 'footer'): string
{
    $plugin = $GLOBALS['reidoabc_site_controls'] ?? null;
    if (!$plugin instanceof ReiDoABC_Site_Controls) {
        return '';
    }

    return $plugin->public_commerce_links($context);
}

register_activation_hook(__FILE__, ['ReiDoABC_Site_Controls', 'activate']);
$GLOBALS['reidoabc_site_controls'] = new ReiDoABC_Site_Controls();
