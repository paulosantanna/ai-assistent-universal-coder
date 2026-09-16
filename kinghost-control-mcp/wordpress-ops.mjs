import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const USER_SQL = "SELECT ID, user_login, user_email, user_registered, display_name FROM ?? LIMIT 500";
const META_SQL = "SELECT user_id, meta_value FROM ?? WHERE meta_key = ? AND user_id IN (?)";

export const DEFAULT_PUBLISH_SCOPES = [
  "wp-content/themes",
  "wp-content/plugins",
  "wp-content/mu-plugins"
];

export const WOOCOMMERCE_PUBLISH_POLICY = {
  id: "woocommerce-preserve-live-commerce",
  code_allowed_default: DEFAULT_PUBLISH_SCOPES,
  preserve_on_production: [
    "orders (wc_orders / shop_order)",
    "customers",
    "payment gateway secrets",
    "siteurl",
    "home",
    "user_pass hashes"
  ],
  optional_high_risk: ["product catalog SQL", "wp-content/uploads"],
  never_upload: ["wp-config.php", "wp-admin", "wp-includes"],
  verify_http_routes: ["/cart/", "/checkout/", "/my-account/", "/shop/"]
};

export const KINGHOST_PUBLISH_ENV_NAMES = [
  "KINGHOST_DOMAINS",
  "KINGHOST_FTP_USER",
  "KINGHOST_FTP_PASSWORD",
  "KINGHOST_FTP_HOST",
  "KINGHOST_MYSQL_USER",
  "KINGHOST_MYSQL_PASSWORD",
  "KINGHOST_MYSQL_HOST",
  "KINGHOST_COOKIE_JAR"
];

function pathIsDir(candidate) {
  try {
    return existsSync(candidate) && statSync(candidate).isDirectory();
  } catch {
    return false;
  }
}

function pathIsFile(candidate) {
  try {
    return existsSync(candidate) && statSync(candidate).isFile();
  } catch {
    return false;
  }
}

export function woocommercePublishPolicy() {
  return { ...WOOCOMMERCE_PUBLISH_POLICY };
}

const SKIP_PLUGIN_NAMES = new Set([".", "..", "index.php", ".htaccess"]);
const MAX_LOCAL_PLUGINS = 500;

function readPluginHeader(filePath) {
  try {
    const text = readFileSync(filePath, "utf8").slice(0, 8192);
    const name = /Plugin Name:\s*(.+)/i.exec(text)?.[1]?.trim() || null;
    const version = /Version:\s*(.+)/i.exec(text)?.[1]?.trim() || null;
    return { name, version };
  } catch {
    return { name: null, version: null };
  }
}

function directoryBootstrap(dir, slug) {
  const conventional = join(dir, `${slug}.php`);
  if (pathIsFile(conventional)) return `${slug}.php`;
  try {
    const phpFiles = readdirSync(dir).filter((name) => name.endsWith(".php") && pathIsFile(join(dir, name)));
    for (const file of phpFiles) {
      if (readPluginHeader(join(dir, file)).name) return file;
    }
    return phpFiles[0] || null;
  } catch {
    return null;
  }
}

export function listLocalWordpressPlugins(contentRoot, options = {}) {
  const limit = Math.min(Math.max(Number(options.limit || MAX_LOCAL_PLUGINS), 1), 2000);
  const installed = [];
  const pluginsDir = join(contentRoot, "plugins");
  const muDir = join(contentRoot, "mu-plugins");

  if (pathIsDir(pluginsDir)) {
    for (const name of readdirSync(pluginsDir)) {
      if (installed.length >= limit) break;
      if (SKIP_PLUGIN_NAMES.has(name) || name.startsWith(".")) continue;
      const full = join(pluginsDir, name);
      if (pathIsDir(full)) {
        const bootstrap = directoryBootstrap(full, name);
        const header = bootstrap ? readPluginHeader(join(full, bootstrap)) : { name: null, version: null };
        installed.push({
          slug: name,
          kind: "regular",
          path: `wp-content/plugins/${name}`,
          bootstrap,
          name: header.name,
          version: header.version
        });
      } else if (name.endsWith(".php") && pathIsFile(full)) {
        const header = readPluginHeader(full);
        installed.push({
          slug: name.replace(/\.php$/i, ""),
          kind: "file",
          path: `wp-content/plugins/${name}`,
          bootstrap: name,
          name: header.name,
          version: header.version
        });
      }
    }
  }

  if (pathIsDir(muDir)) {
    for (const name of readdirSync(muDir)) {
      if (installed.length >= limit) break;
      if (SKIP_PLUGIN_NAMES.has(name) || name.startsWith(".")) continue;
      const full = join(muDir, name);
      if (pathIsDir(full)) {
        const bootstrap = directoryBootstrap(full, name);
        const header = bootstrap ? readPluginHeader(join(full, bootstrap)) : { name: null, version: null };
        installed.push({
          slug: name,
          kind: "must-use",
          path: `wp-content/mu-plugins/${name}`,
          bootstrap,
          name: header.name,
          version: header.version
        });
      } else if (name.endsWith(".php") && pathIsFile(full)) {
        const header = readPluginHeader(full);
        installed.push({
          slug: name.replace(/\.php$/i, ""),
          kind: "must-use",
          path: `wp-content/mu-plugins/${name}`,
          bootstrap: name,
          name: header.name,
          version: header.version
        });
      }
    }
  }

  const slugs = installed.map((plugin) => plugin.slug);
  return {
    installed,
    count: installed.length,
    slugs,
    mu_plugin_count: installed.filter((plugin) => plugin.kind === "must-use").length,
    woocommerce_plugin_present: slugs.includes("woocommerce"),
    truncated: installed.length >= limit
  };
}

export function inspectLocalWordpressTree(workspaceRoot, options = {}) {
  const root = resolve(workspaceRoot || ".");
  const includeUploads = options.include_uploads === true;
  const hasWpContent = pathIsDir(join(root, "wp-content"));
  const isWpContentRoot = pathIsDir(join(root, "themes")) && (
    pathIsDir(join(root, "plugins")) || pathIsDir(join(root, "mu-plugins"))
  );
  const wordpress = hasWpContent
    || isWpContentRoot
    || pathIsFile(join(root, "wp-load.php"))
    || pathIsFile(join(root, "index.php"));
  const contentRoot = hasWpContent ? join(root, "wp-content") : (isWpContentRoot ? root : null);
  const pluginInventory = contentRoot
    ? listLocalWordpressPlugins(contentRoot)
    : { installed: [], count: 0, slugs: [], mu_plugin_count: 0, woocommerce_plugin_present: false, truncated: false };
  const woocommercePluginPresent = pluginInventory.woocommerce_plugin_present;
  const layout = hasWpContent ? "wordpress_root" : isWpContentRoot ? "wp_content" : wordpress ? "php_or_partial" : "unknown";
  const localDir = layout === "wordpress_root" ? join(root, "wp-content") : root;
  const excluded = [
    "wp-config.php",
    "wp-admin",
    "wp-includes",
    ...(includeUploads ? [] : ["wp-content/uploads"])
  ];
  const presentScopes = DEFAULT_PUBLISH_SCOPES.filter((scope) => {
    if (layout === "wordpress_root") return pathIsDir(join(root, ...scope.split("/")));
    if (layout === "wp_content") {
      const leaf = scope.replace(/^wp-content\//, "");
      return pathIsDir(join(root, leaf));
    }
    return false;
  });

  return {
    workspace_root: root,
    wordpress,
    layout,
    local_dir: localDir,
    remote_root: "wp-content",
    woocommerce_plugin_present: woocommercePluginPresent,
    plugins: pluginInventory,
    wp_config_present: pathIsFile(join(root, "wp-config.php")),
    default_scopes: presentScopes.length ? presentScopes : DEFAULT_PUBLISH_SCOPES,
    excluded_by_default: excluded,
    playbook_id: "kinghost-wordpress-publish",
    one_command: "npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <existing-kinghost-domain>"
  };
}

export function publishCredentialPresence() {
  const present = [];
  const missing = [];
  for (const name of KINGHOST_PUBLISH_ENV_NAMES) {
    if (String(process.env[name] || "").trim()) present.push(name);
    else missing.push(name);
  }
  return { present_env_names: present, missing_env_names: missing };
}

export function maskEmail(email) {
  const value = String(email || "");
  const at = value.indexOf("@");
  if (at <= 0) return "***";
  return `${value.slice(0, 1)}***@${value.slice(at + 1)}`;
}

export function parsePhpSerializedPluginList(value) {
  if (typeof value !== "string" || !value.includes("s:")) return [];
  const plugins = [];
  const re = /s:\d+:"([^"]+\.php)"/g;
  let match;
  while ((match = re.exec(value))) plugins.push(match[1]);
  return plugins;
}

export async function detectTablePrefix(db) {
  const [rows] = await db.execute("SHOW TABLES");
  const names = rows.map((row) => Object.values(row)[0]).map(String);
  const usersTable = names.find((name) => /(^|_)users$/.test(name) && !/usermeta$/.test(name));
  if (!usersTable) return { prefix: "wp_", tables: names, wordpress: false };
  const prefix = usersTable.replace(/users$/, "");
  return { prefix, tables: names, wordpress: true, users_table: usersTable };
}

function rolesFromCapabilities(metaValue) {
  const raw = String(metaValue || "");
  const roles = [];
  const re = /s:\d+:"([^"]+)"/g;
  let match;
  while ((match = re.exec(raw))) {
    const key = match[1];
    if (["administrator", "editor", "author", "contributor", "subscriber", "shop_manager", "customer"].includes(key)) {
      roles.push(key);
    }
  }
  return roles;
}

export async function listWordpressUsers(db, { prefix } = {}) {
  const detected = prefix ? { prefix, wordpress: true, users_table: `${prefix}users` } : await detectTablePrefix(db);
  if (!detected.wordpress) return { wordpress: false, users: [], note: "No WordPress users table found" };
  const usersTable = `${detected.prefix}users`;
  const metaTable = `${detected.prefix}usermeta`;
  const [users] = await db.execute(`SELECT ID, user_login, user_email, user_registered, display_name FROM \`${usersTable.replace(/`/g, "")}\` LIMIT 500`);
  let rolesById = new Map();
  try {
    const ids = users.map((row) => row.ID);
    if (ids.length) {
      const placeholders = ids.map(() => "?").join(",");
      const [meta] = await db.execute(
        `SELECT user_id, meta_value FROM \`${metaTable.replace(/`/g, "")}\` WHERE meta_key = ? AND user_id IN (${placeholders})`,
        [`${detected.prefix}capabilities`, ...ids]
      );
      rolesById = new Map(meta.map((row) => [Number(row.user_id), rolesFromCapabilities(row.meta_value)]));
    }
  } catch {
    rolesById = new Map();
  }
  return {
    wordpress: true,
    table_prefix: detected.prefix,
    users: users.map((row) => ({
      id: row.ID,
      user_login: row.user_login,
      display_name: row.display_name,
      user_registered: row.user_registered,
      email: maskEmail(row.user_email),
      roles: rolesById.get(Number(row.ID)) || []
    })),
    never_returned: ["user_pass", "session_tokens", "unmasked email"]
  };
}

export async function listWordpressPlugins(db, { prefix } = {}) {
  const detected = prefix ? { prefix, wordpress: true } : await detectTablePrefix(db);
  if (!detected.wordpress && !prefix) {
    return { wordpress: false, active_plugins: [], note: "No WordPress options table found" };
  }
  const optionsTable = `${detected.prefix}options`;
  const [rows] = await db.execute(
    `SELECT option_name, option_value FROM \`${optionsTable.replace(/`/g, "")}\` WHERE option_name IN ('active_plugins','stylesheet','template','siteurl','home') LIMIT 20`
  );
  const map = Object.fromEntries(rows.map((row) => [row.option_name, row.option_value]));
  return {
    wordpress: true,
    table_prefix: detected.prefix,
    active_plugins: parsePhpSerializedPluginList(String(map.active_plugins || "")),
    stylesheet: map.stylesheet || null,
    template: map.template || null,
    siteurl: map.siteurl || null,
    home: map.home || null
  };
}

export async function wordpressInventory(db) {
  const detected = await detectTablePrefix(db);
  const users = detected.wordpress ? await listWordpressUsers(db, { prefix: detected.prefix }) : { users: [] };
  const plugins = detected.wordpress ? await listWordpressPlugins(db, { prefix: detected.prefix }) : { active_plugins: [] };
  const commerceTables = detected.tables.filter((name) => /woocommerce|wc_orders/i.test(name));
  return {
    wordpress: detected.wordpress,
    table_prefix: detected.prefix,
    table_count: detected.tables.length,
    commerce_tables: commerceTables.slice(0, 100),
    users: users.users,
    active_plugins: plugins.active_plugins,
    theme: { stylesheet: plugins.stylesheet || null, template: plugins.template || null },
    siteurl: plugins.siteurl || null,
    never_returned: ["passwords", "option secrets", "unmasked emails"]
  };
}

export { USER_SQL, META_SQL };
