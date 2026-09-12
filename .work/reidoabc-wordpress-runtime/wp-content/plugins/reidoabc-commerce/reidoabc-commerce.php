<?php
/**
 * Plugin Name: Rei do ABC Commerce
 * Description: WooCommerce catalog policy and manual PIX gateway for Rei do ABC.
 * Version: 1.0.0
 * Requires Plugins: woocommerce
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

add_action('before_woocommerce_init', static function (): void {
    if (class_exists('Automattic\\WooCommerce\\Utilities\\FeaturesUtil')) {
        Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility('custom_order_tables', __FILE__, true);
    }
});

register_activation_hook(__FILE__, static function (): void {
    foreach ([
        'pedacos-de-tortas' => 'Pedaços de Tortas',
        'barras-de-chocolate' => 'Barras de Chocolate',
    ] as $slug => $name) {
        if (!term_exists($slug, 'product_cat')) {
            wp_insert_term($name, 'product_cat', ['slug' => $slug]);
        }
    }
});

add_action('woocommerce_product_query', static function (WP_Query $query): void {
    if (is_admin() || !$query->is_main_query() || !(is_shop() || is_product_taxonomy())) {
        return;
    }
    $tax_query = (array) $query->get('tax_query');
    $tax_query[] = [
        'taxonomy' => 'product_cat',
        'field' => 'slug',
        'terms' => ['pedacos-de-tortas', 'barras-de-chocolate'],
        'operator' => 'IN',
    ];
    $query->set('tax_query', $tax_query);
});

add_action('plugins_loaded', static function (): void {
    if (!class_exists('WC_Payment_Gateway')) {
        return;
    }

    final class ReiDoABCPixGateway extends WC_Payment_Gateway {
        public function __construct() {
            $this->id = 'reidoabc_pix';
            $this->method_title = 'PIX Rei do ABC';
            $this->method_description = 'Cria um pedido WooCommerce aguardando confirmação manual do PIX.';
            $this->has_fields = false;
            $this->supports = ['products'];
            $this->init_form_fields();
            $this->init_settings();
            $this->title = (string) $this->get_option('title', 'PIX');
            $this->instructions = (string) $this->get_option('instructions', 'Após finalizar o pedido, use a chave PIX exibida para efetuar o pagamento.');
            $this->pix_key = (string) $this->get_option('pix_key', '');
            $this->enabled = (string) $this->get_option('enabled', 'no');
            add_action('woocommerce_update_options_payment_gateways_' . $this->id, [$this, 'process_admin_options']);
            add_action('woocommerce_thankyou_' . $this->id, [$this, 'thankyou_page']);
        }

        public function init_form_fields(): void {
            $this->form_fields = [
                'enabled' => ['title' => 'Ativar', 'type' => 'checkbox', 'label' => 'Ativar PIX Rei do ABC', 'default' => 'no'],
                'title' => ['title' => 'Título', 'type' => 'text', 'default' => 'PIX'],
                'instructions' => ['title' => 'Instruções', 'type' => 'textarea', 'default' => 'Após finalizar o pedido, use a chave PIX exibida para efetuar o pagamento.'],
                'pix_key' => ['title' => 'Chave PIX', 'type' => 'text', 'default' => ''],
            ];
        }

        public function is_available(): bool {
            return parent::is_available() && $this->pix_key !== '';
        }

        public function process_payment($order_id): array {
            $order = wc_get_order($order_id);
            if (!$order) {
                return ['result' => 'failure'];
            }
            $order->update_status('on-hold', 'Aguardando confirmação de pagamento PIX.');
            wc_reduce_stock_levels($order_id);
            WC()->cart->empty_cart();
            return ['result' => 'success', 'redirect' => $this->get_return_url($order)];
        }

        public function thankyou_page($order_id): void {
            if ($this->instructions !== '') {
                echo wp_kses_post(wpautop(wptexturize($this->instructions)));
            }
            if ($this->pix_key !== '') {
                echo '<p><strong>Chave PIX:</strong> <code>' . esc_html($this->pix_key) . '</code></p>';
            }
        }
    }

    add_filter('woocommerce_payment_gateways', static function (array $gateways): array {
        $gateways[] = ReiDoABCPixGateway::class;
        return $gateways;
    });
}, 20);
