<?php
/**
 * Plugin Name: Rei do ABC Runtime Hardening
 * Description: Security controls that must remain active independently of theme state.
 */

declare(strict_types=1);

if (!defined('ABSPATH')) { exit; }

function reidoabc_client_ip(): string {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    return filter_var($ip, FILTER_VALIDATE_IP) ? $ip : 'unknown';
}

function reidoabc_rate_limited(string $scope, int $limit, int $window): bool {
    $key = 'reidoabc_rl_' . substr(hash('sha256', $scope . '|' . reidoabc_client_ip()), 0, 40);
    $state = get_transient($key);
    $count = is_array($state) ? (int) ($state['count'] ?? 0) : 0;
    if ($count >= $limit) { return true; }
    set_transient($key, ['count' => $count + 1], $window);
    return false;
}

add_filter('xmlrpc_enabled', '__return_false');
add_filter('login_errors', static fn (): string => 'Não foi possível autenticar com os dados informados.');
add_filter('wp_is_application_passwords_available', '__return_false');

if (wp_get_environment_type() === 'local') {
    add_filter('pre_wp_mail', static function (): bool {
        return true;
    });
}

add_action('init', static function (): void {
    remove_action('wp_head', 'wp_generator');
    remove_action('wp_head', 'wlwmanifest_link');
    remove_action('wp_head', 'rsd_link');
    remove_action('wp_head', 'rest_output_link_wp_head');
});

add_filter('authenticate', static function ($user, string $username) {
    if ($username !== '' && reidoabc_rate_limited('login', 8, 900)) {
        return new WP_Error('reidoabc_rate_limited', 'Tente novamente mais tarde.');
    }
    return $user;
}, 1, 2);

add_action('wp_login', static function (): void {
    $key = 'reidoabc_rl_' . substr(hash('sha256', 'login|' . reidoabc_client_ip()), 0, 40);
    delete_transient($key);
});

add_filter('rest_pre_dispatch', static function ($result, WP_REST_Server $server, WP_REST_Request $request) {
    $route = $request->get_route();
    if (str_starts_with($route, '/wp/v2/users') && !current_user_can('list_users')) {
        return new WP_Error('rest_forbidden', 'Recurso indisponível.', ['status' => 403]);
    }
    if (str_contains($route, '/batch') && reidoabc_rate_limited('rest-batch', 30, 60)) {
        return new WP_Error('rest_rate_limited', 'Tente novamente mais tarde.', ['status' => 429]);
    }
    return $result;
}, 10, 3);

add_action('send_headers', static function (): void {
    if (headers_sent()) { return; }
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: SAMEORIGIN');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
    if (is_ssl()) { header('Strict-Transport-Security: max-age=31536000; includeSubDomains'); }
    header("Content-Security-Policy-Report-Only: default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https:; script-src 'self' 'unsafe-inline'; font-src 'self' data: https:; connect-src 'self' https://viacep.com.br");
});
