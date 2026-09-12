<?php
declare(strict_types=1);

$environment = getenv('WP_ENVIRONMENT_TYPE') ?: 'production';
$is_local = $environment === 'local';

function reidoabc_runtime_value(string $name, bool $is_local, string $local_default = ''): string {
    $value = getenv($name);
    if (is_string($value) && $value !== '') {
        return $value;
    }
    if ($is_local && $local_default !== '') {
        return $local_default;
    }
    http_response_code(503);
    exit('Configuration unavailable.');
}

define('DB_NAME', reidoabc_runtime_value('WORDPRESS_DB_NAME', $is_local, 'reidoabc_local'));
define('DB_USER', reidoabc_runtime_value('WORDPRESS_DB_USER', $is_local, 'reidoabc_local'));
define('DB_PASSWORD', reidoabc_runtime_value('WORDPRESS_DB_PASSWORD', $is_local, 'local-only'));
define('DB_HOST', reidoabc_runtime_value('WORDPRESS_DB_HOST', $is_local, 'db:3306'));
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

foreach (['AUTH_KEY', 'SECURE_AUTH_KEY', 'LOGGED_IN_KEY', 'NONCE_KEY', 'AUTH_SALT', 'SECURE_AUTH_SALT', 'LOGGED_IN_SALT', 'NONCE_SALT'] as $name) {
    define($name, reidoabc_runtime_value('WORDPRESS_' . $name, $is_local, 'local-' . strtolower($name)));
}

$site_url = getenv('WORDPRESS_SITEURL') ?: '';
$home_url = getenv('WORDPRESS_HOME') ?: $site_url;
if ($site_url !== '') { define('WP_SITEURL', $site_url); }
if ($home_url !== '') { define('WP_HOME', $home_url); }

$table_prefix = getenv('WORDPRESS_TABLE_PREFIX') ?: 'wp_';
define('WP_ENVIRONMENT_TYPE', $environment);
define('WP_DEBUG', filter_var(getenv('WP_DEBUG') ?: 'false', FILTER_VALIDATE_BOOL));
define('WP_DEBUG_DISPLAY', false);
define('WP_DEBUG_LOG', WP_DEBUG);
define('DISALLOW_FILE_EDIT', true);
define('DISALLOW_FILE_MODS', !$is_local);
define('WP_MEMORY_LIMIT', '256M');
define('WP_MAX_MEMORY_LIMIT', '512M');
define('WP_POST_REVISIONS', 5);
define('AUTOSAVE_INTERVAL', 120);
define('EMPTY_TRASH_DAYS', 14);
define('REIDOABC_DISABLE_APPLICATION_PASSWORDS', true);
define('REIDOABC_DATA_ENCRYPTION', reidoabc_runtime_value('REIDOABC_DATA_ENCRYPTION', $is_local, 'local-development'));

if (!$is_local) {
    define('FORCE_SSL_ADMIN', true);
    define('DISABLE_WP_CRON', true);
}

if (!defined('ABSPATH')) { define('ABSPATH', __DIR__ . '/'); }
require_once ABSPATH . 'wp-settings.php';
