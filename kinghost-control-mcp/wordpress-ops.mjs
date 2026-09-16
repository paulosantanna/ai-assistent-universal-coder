const USER_SQL = "SELECT ID, user_login, user_email, user_registered, display_name FROM ?? LIMIT 500";
const META_SQL = "SELECT user_id, meta_value FROM ?? WHERE meta_key = ? AND user_id IN (?)";

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
