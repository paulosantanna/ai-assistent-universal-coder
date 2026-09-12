<?php
/**
 * Front Page Template - Rei do ABC Gourmet Storefront
 */
if (!defined('ABSPATH')) {
    exit;
}

get_header();

$logo = reidoabc_logo_url();
$brand = reidoabc_brand_profile();
$hero_slides = reidoabc_hero_slides();
$popular_products = [];

if (function_exists('wc_get_products')) {
    $database_products = wc_get_products([
        'status' => 'publish',
        'limit' => 24,
        'category' => ['pedacos-de-tortas', 'barras-de-chocolate'],
        'orderby' => 'date',
        'order' => 'DESC',
    ]);

    $popular_products = array_map(static function (WC_Product $product): array {
        return [
            'id' => $product->get_id(),
            'name' => $product->get_name(),
            'price' => wp_strip_all_tags($product->get_price_html()),
            'permalink' => $product->get_permalink(),
            'image' => reidoabc_product_image_url($product),
            'cart' => $product->add_to_cart_url(),
        ];
    }, $database_products);
}
?>

    <section class="hero-carousel-section" aria-roledescription="carousel" aria-label="Destaques da confeitaria">
        <div class="carousel-container">
            <button class="carousel-arrow prev" type="button" aria-label="Anterior">‹</button>
            <button class="carousel-arrow next" type="button" aria-label="Próximo">›</button>

            <?php foreach ($hero_slides as $index => $slide): ?>
            <div class="carousel-slide<?php echo $index === 0 ? ' active' : ''; ?>" data-slide="<?php echo (int) ($index + 1); ?>">
                <img
                    src="<?php echo esc_url($slide['url']); ?>"
                    alt="<?php echo esc_attr($slide['alt']); ?>"
                    width="1400"
                    height="520"
                    <?php echo $index === 0 ? 'fetchpriority="high"' : 'loading="lazy"'; ?>
                    decoding="async"
                >
                <div class="carousel-overlay">
                    <h2><?php echo esc_html($slide['title']); ?></h2>
                    <p><img src="<?php echo esc_url($logo); ?>" class="brand-crown-icon-sm" width="18" height="18" alt=""> <?php echo esc_html($slide['text']); ?></p>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </section>

    <section class="feature-bar-section" aria-label="Diferenciais">
        <div class="feature-box">
            <div class="feature-text">
                <h4>Envio para todo o Brasil</h4>
                <p>Encomendas embaladas para chegar com a mesma apresentação da loja.</p>
            </div>
        </div>
        <div class="feature-box">
            <div class="feature-text">
                <h4>Food Service</h4>
                <p>Cremes, caldas e bases gourmet para padarias, cafés e operações de alto padrão.</p>
            </div>
        </div>
        <div class="feature-box">
            <div class="feature-text">
                <h4>Pagamento seguro</h4>
                <p>PIX direto e Mercado Pago no checkout nativo da loja.</p>
            </div>
        </div>
    </section>

    <section class="products-section" id="produtos">
        <div class="section-pill-header">
            <img src="<?php echo esc_url($logo); ?>" class="brand-crown-icon" width="16" height="16" alt=""> Produtos Populares
        </div>

        <div class="product-grid">
            <?php foreach ($popular_products as $product): ?>
            <article class="product-card">
                <div>
                    <a href="<?php echo esc_url($product['permalink']); ?>">
                        <img src="<?php echo esc_url($product['image']); ?>" alt="<?php echo esc_attr($product['name']); ?>" class="product-img" width="400" height="320" loading="lazy" decoding="async">
                    </a>
                    <h3><a href="<?php echo esc_url($product['permalink']); ?>"><?php echo esc_html($product['name']); ?></a></h3>
                </div>
                <div>
                    <div class="price"><?php echo esc_html($product['price']); ?></div>
                    <a href="<?php echo esc_url($product['cart']); ?>" class="btn-add-cart">Adicionar ao carrinho</a>
                </div>
            </article>
            <?php endforeach; ?>
        </div>
        <?php if (!$popular_products): ?>
            <p class="reidoabc-products-empty">Nenhum produto está disponível no catálogo neste momento.</p>
        <?php endif; ?>
    </section>

    <section class="delivery-row-section">
        <div class="delivery-row-grid">
            <div class="callout-card">
                <div>
                    <span class="tag"><img src="<?php echo esc_url($logo); ?>" class="brand-crown-icon" width="16" height="16" alt=""> Loja Física</span>
                    <h3>Visite o Rei do ABC em Rudge Ramos</h3>
                    <p><?php echo esc_html($brand['street']); ?> · <?php echo esc_html($brand['hours']); ?></p>
                </div>
                <a href="<?php echo esc_url($brand['maps']); ?>" target="_blank" rel="noopener noreferrer" class="btn-callout">Como chegar <span class="arrow">➔</span></a>
            </div>

            <div class="callout-card">
                <div>
                    <span class="tag"><img src="<?php echo esc_url($logo); ?>" class="brand-crown-icon" width="16" height="16" alt=""> Delivery do Rei</span>
                    <h3>Peça no iFood ou fale no WhatsApp</h3>
                    <p>Os doces da loja na sua casa, com o mesmo padrão gourmet.</p>
                </div>
                <a href="<?php echo esc_url($brand['ifood']); ?>" target="_blank" rel="noopener noreferrer" class="btn-callout">Pedir agora <span class="arrow">➔</span></a>
            </div>
        </div>
    </section>

<?php
get_footer();
