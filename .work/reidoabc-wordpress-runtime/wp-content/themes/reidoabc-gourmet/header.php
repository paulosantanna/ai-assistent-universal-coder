<?php
if (!defined('ABSPATH')) { exit; }
$theme_uri = get_stylesheet_directory_uri();
$cart_url = function_exists('wc_get_cart_url') ? wc_get_cart_url() : home_url('/');
$account_url = function_exists('wc_get_page_permalink') ? wc_get_page_permalink('myaccount') : wp_login_url();
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header class="top-header-bar">
    <a href="<?php echo esc_url(home_url('/')); ?>" class="top-crown-brand" aria-label="<?php echo esc_attr(get_bloginfo('name')); ?>"><img src="<?php echo esc_url($theme_uri . '/assets/images/Logo-Simples-Dourado.png'); ?>" alt="<?php echo esc_attr(get_bloginfo('name')); ?>"></a>
    <div class="top-user-actions"><a href="<?php echo esc_url($cart_url); ?>">Carrinho: <span><?php echo esc_html(reidoabc_gourmet_cart_label()); ?></span></a><a href="<?php echo esc_url($account_url); ?>"><?php echo is_user_logged_in() ? 'Minha Conta' : 'Entrar'; ?></a></div>
</header>
<div class="search-nav-bar"><div class="search-container"><a href="#produtos" class="btn-category-dropdown">Produtos</a><form class="search-form" action="<?php echo esc_url(home_url('/')); ?>" method="get" role="search"><label class="screen-reader-text" for="reidoabc-search">Pesquisar produtos</label><input id="reidoabc-search" type="search" name="s" placeholder="Pesquise produtos aqui..." value="<?php echo esc_attr(get_search_query()); ?>"><input type="hidden" name="post_type" value="product"><select name="product_cat" aria-label="Categoria"><option value="">Selecionar categoria</option><option value="pedacos-de-tortas">Pedaços de Tortas</option><option value="barras-de-chocolate">Barras de Chocolate</option></select><button type="submit">Buscar</button></form></div></div>
