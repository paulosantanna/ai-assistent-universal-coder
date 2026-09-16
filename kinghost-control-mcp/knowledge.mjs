const RETRIEVED_AT = "2026-09-16";

const WORDPRESS_PLUGIN_CATALOG = [
  {
    slug: "woocommerce",
    title: "WooCommerce",
    kind: "ecommerce",
    path: "wp-content/plugins/woocommerce",
    tables: ["woocommerce_order_items", "woocommerce_order_itemmeta", "woocommerce_sessions", "woocommerce_tax_rates", "wc_orders"],
    notes: "Official WordPress e-commerce plugin. Products live in posts/postmeta; orders may use HPOS (wc_orders) or legacy shop_order posts. Change via plugin/theme APIs before direct SQL."
  },
  {
    slug: "woocommerce-payments",
    title: "WooCommerce Payments",
    kind: "ecommerce-payments",
    path: "wp-content/plugins/woocommerce-payments"
  },
  {
    slug: "woocommerce-paypal-payments",
    title: "WooCommerce PayPal Payments",
    kind: "ecommerce-payments",
    path: "wp-content/plugins/woocommerce-paypal-payments"
  },
  {
    slug: "woocommerce-mercadopago",
    title: "Mercado Pago for WooCommerce",
    kind: "ecommerce-payments",
    path: "wp-content/plugins/woocommerce-mercadopago"
  },
  {
    slug: "jetpack",
    title: "Jetpack",
    kind: "platform",
    path: "wp-content/plugins/jetpack"
  },
  {
    slug: "elementor",
    title: "Elementor",
    kind: "builder",
    path: "wp-content/plugins/elementor"
  },
  {
    slug: "wordpress-seo",
    title: "Yoast SEO",
    kind: "seo",
    path: "wp-content/plugins/wordpress-seo"
  },
  {
    slug: "akismet",
    title: "Akismet Anti-spam",
    kind: "security",
    path: "wp-content/plugins/akismet"
  },
  {
    slug: "classic-editor",
    title: "Classic Editor",
    kind: "editing",
    path: "wp-content/plugins/classic-editor"
  },
  {
    slug: "contact-form-7",
    title: "Contact Form 7",
    kind: "forms",
    path: "wp-content/plugins/contact-form-7"
  }
];

const ARTICLES = [
  {
    id: "panel-login",
    title: "Painel de Controle KingHost — login com cookie do workspace",
    topics: ["painel", "login", "cookie", "cookier", "2fa", "hospedagem"],
    source_url: "https://king.host/wiki/artigo/como-acessar-painel-de-controle/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "URL oficial do painel: https://painel.kinghost.com.br.",
      "Login padrão: e-mail da conta + senha + 2FA (e-mail, SMS, app authenticator ou WhatsApp). Login Google dispensa 2FA do painel.",
      "AEOS não digita senha do painel nem extrai cookies do navegador. O workspace autentica consumindo um cookie-jar externo (Netscape/JSON) em absoluto, fora do Git, via kinghost_control.panel.session.open_cookie_file.",
      "O modelo só vê panel_session_ref, hosts permitidos e cookie_count. Valores de cookie nunca saem do processo.",
      "Se o GET autenticado devolver a tela ENTRAR NO PAINEL, a sessão expirou: renovar o jar e reabrir.",
      "Hosts permitidos para o jar: painel.kinghost.com.br, *.kinghost.com.br, king.host, *.kinghost.net."
    ].join(" ")
  },
  {
    id: "domains",
    title: "Domínios existentes na Hospedagem KingHost",
    topics: ["dominio", "domínios", "domains", "hospedagem", "selecionar"],
    source_url: "https://king.host/wiki/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "No painel, a página inicial lista os produtos de Hospedagem. Cada site/domínio é selecionado antes de abrir FTP, MySQL, PHP ou WordPress.",
      "Várias instalações WordPress no mesmo domínio (raiz vs subdomínio) exigem o seletor de instalação no Gerenciar WordPress.",
      "AEOS lista domínios por: (1) KINGHOST_DOMAINS ou params.domains, (2) HTML autenticado do painel com cookie, (3) pastas de domínio no FTP.",
      "kinghost_control.domain.list + domain.select amarram o domínio escolhido ao change_id/FSM. Ambiente local|staging|production continua obrigatório para mutação.",
      "Não inventar API privada de listagem. Sem cookie válido, env ou FTP, a listagem falha fechado."
    ].join(" ")
  },
  {
    id: "ftp",
    title: "FTP da Hospedagem KingHost — clone e publicação",
    topics: ["ftp", "sftp", "clone", "publicar", "upload", "public_html", "file manager"],
    source_url: "https://king.host/wiki/base-de-conhecimento/gerenciar-ftp/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Após selecionar o domínio no painel, abra Gerenciar FTP. Dados: host (principal ou alternativo — preferir o alternativo), usuário e senha já provisionados.",
      "Usuários FTP adicionais existem e ficam restritos a uma pasta. AEOS lê o username já criado; nunca raspa a senha da UI.",
      "Raiz web típica: public_html. WordPress: public_html ou subpasta/subdomínio escolhido na instalação.",
      "Clone: kinghost_control.site.clone / ftp.tree.download copia a árvore remota para o workspace, pulando wp-config.php e dumps com segredo.",
      "Publicação: ftp.tree.upload ou deploy.workspace_to_production (dry-run default, approved+change_id+rollback_ref). Escopo padrão wp-content; core/wp-config exigem high_risk_approved.",
      "Políticas de IP no Gerenciar FTP podem bloquear o cliente: o operador libera o IP de saída antes de bind."
    ].join(" ")
  },
  {
    id: "mysql",
    title: "MySQL KingHost e integração PHP/WordPress",
    topics: ["mysql", "banco", "phpmyadmin", "wp-config", "database", "integracao"],
    source_url: "https://king.host/wiki/artigo/como-criar-um-banco-de-dados-mysql/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Painel → selecionar domínio → Gerenciar bancos MySQL → criar/listar bases, senha, observação e política de IP.",
      "Acesso externo: fechado (só o web server), qualquer IP (inseguro) ou allowlist de IPs. Workspace remoto precisa da allowlist do IP de saída.",
      "Host MySQL costuma ser mysql.<dominio> a partir da rede externa; a partir do PHP no mesmo host frequentemente localhost. Confirmar no painel, nunca adivinhar.",
      "Usuários MySQL adicionais: no máximo 5 por base; o nome é atribuído pela KingHost, não escolhido. Listar usernames já criados; senhas só via env/secret bind.",
      "WordPress liga PHP↔MySQL em wp-config.php (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, table_prefix). AEOS não devolve esses segredos. Prefixo é detectado via SHOW TABLES.",
      "phpMyAdmin do painel é canal humano; o MCP usa mysql2 com credential_ref opaco. SELECT/SHOW/DESCRIBE/EXPLAIN por padrão; mutação com EXPLAIN, dry-run, approved, rollback."
    ].join(" ")
  },
  {
    id: "mysql-extra-users",
    title: "Usuários MySQL adicionais já criados",
    topics: ["usuarios", "users", "mysql", "credencial"],
    source_url: "https://king.host/wiki/artigo/como-criar-usuario-adicional-para-mysql/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Painel → Gerenciar bancos MySQL → Editar → Gerenciar Usuários lista usuários adicionais já criados.",
      "kinghost_control.users.list une usernames de credenciais ligadas, WordPress wp_users (redigido) e inventário informado pelo operador. Nunca password hash ou cookie.",
      "Usuários adicionais acessam phpMyAdmin, SSH, MySQL Workbench e o MCP, sujeitos à política de IP da base."
    ].join(" ")
  },
  {
    id: "wordpress-panel",
    title: "Gerenciar WordPress no painel KingHost",
    topics: ["wordpress", "wp-admin", "plugins", "temas", "php", "instalador"],
    source_url: "https://king.host/wiki/artigo/como-gerenciar-o-wordpress-no-painel-de-controle-da-kinghost/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Hospedagem → Gerenciar WordPress: seletor de instalação, versão WP, versão PHP, atualizações automáticas, plugins, temas, desinstalação.",
      "Instalador automático: domínio, pasta FTP ou subdomínio; e-mail/senha do wp-admin. Login automático pelo painel não substitui cookie wp-admin do workspace.",
      "Desinstalar remove arquivos do WordPress e dados da instalação; irreversível; high-risk e fora do fluxo padrão de publicação.",
      "Mutação de feature: child theme / plugin de site no workspace, depois FTP em wp-content. Core, wp-admin, wp-includes e wp-config exigem high_risk_approved."
    ].join(" ")
  },
  {
    id: "wordpress-install",
    title: "Instalar WordPress na Hospedagem",
    topics: ["wordpress", "instalar", "criar", "hospedagem"],
    source_url: "https://king.host/wiki/artigo/instale-o-wordpress-facilmente-com-o-instalador-automatico/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Painel → Hospedagem do domínio → Gerenciar WordPress → Instalar WordPress.",
      "Escolher URL (domínio, pasta ou subdomínio), idioma, e-mail e senha forte. Aguardar conclusão e guardar o link wp-admin — a senha não entra em evidência AEOS.",
      "Alternativa manual: FTP de core oficial para public_html + base MySQL + wp-config localmente gerado sem commit de senha."
    ].join(" ")
  },
  {
    id: "php-runtime",
    title: "PHP na Hospedagem KingHost",
    topics: ["php", "php-fpm", "memory_limit", "configuracao php", "runtime"],
    source_url: "https://king.host/wiki/artigo/tecnologias-web-duvidas-frequentes/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Após selecionar o domínio: Configuração PHP altera versão e processos/memória FPM conforme o plano.",
      "Hospedagem compartilhada não expõe php.ini; phpinfo em webNNN.kinghost.net/phpinfo.php. Cloud Web documenta PHP 7.4–8.3; confirmar no painel o plano real.",
      "WordPress memory exhausted: ajustar slider FPM e, se high-risk aprovado, WP_MEMORY_LIMIT em wp-config.php alinhado ao painel.",
      "AEOS planeja a troca via cookie/Playwright no ícone Configuração PHP. Sem API privada."
    ].join(" ")
  },
  {
    id: "woocommerce",
    title: "WooCommerce e plugins de e-commerce em KingHost",
    topics: ["woocommerce", "ecommerce", "e-commerce", "plugin", "loja", "publicar", "publish"],
    source_url: "https://developer.wordpress.org/plugins/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "WooCommerce é plugin WordPress em wp-content/plugins/woocommerce, não um produto KingHost separado.",
      "Inventário: FTP da pasta plugins + option active_plugins (PHP serialized) + SHOW TABLES LIKE '%woocommerce%'.",
      "Produtos: post type product. Pedidos: HPOS wc_orders ou posts shop_order. Checkout/páginas: opções woocommerce_*_page_id; verificar a rota HTTP, não só o option.",
      "Pagamentos (Mercado Pago, PayPal, Stripe) guardam segredos em options: nunca dump de option_value com chave/token.",
      "Publicar tema/plugin custom via FTP scoped; ativação preferencialmente wp-admin/REST autenticado com cookie, não SQL em wp_options.",
      "wordpress-expert usa o universo completo de plugins instalados (wp-content/plugins e mu-plugins), não só WooCommerce nem um catálogo estático.",
      "Publish one-command: código em wp-content por padrão, incluindo todos os plugins locais. Pedidos, clientes, siteurl/home e segredos de pagamento da produção não são sobrescritos pelo site local. --replace-database é high-risk e fora do comando único."
    ].join(" ")
  },
  {
    id: "wordpress-users",
    title: "Usuários WordPress já criados",
    topics: ["usuarios", "users", "wp_users", "wordpress", "roles"],
    source_url: "https://developer.wordpress.org/plugins/users/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "kinghost_control.wordpress.users.list lê ID, user_login, display_name, user_registered e papéis em usermeta. E-mail mascarado. user_pass nunca retorna.",
      "Não persistir PII em beta-map, notebook ou evidência. Roles summary é permitido.",
      "Criar/alterar usuário: wp-admin/REST com cookie, não INSERT em wp_users."
    ].join(" ")
  },
  {
    id: "clone-deploy",
    title: "Clonar o site da Hospedagem e subir alteração local",
    topics: ["clone", "deploy", "workspace", "producao", "produção", "sync", "publicar", "comando", "one-command", "publish"],
    source_url: "https://king.host/wiki/base-de-conhecimento/gerenciar-ftp/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Fluxo: cookie do painel → listar/selecionar domínio → bind FTP/MySQL → FSM → inventário → clone para workspace → editar local → diff → dry-run → backup → APPLY → smoke → CLOSE.",
      "Clone grava arquivos no workspace_root escolhido; manifesto sem segredos. wp-config.php e dumps SQL com senha são skipped.",
      "Upload devolve só a árvore aprovada. Uploads/mídia grandes exigem include_uploads=true. Dry-run é o default de produção.",
      "Comando único do site já alterado localmente: npm run aeos:kinghost:publish -- --local-dir <árvore> --domain <domínio-já-hospedado>. Playbook kinghost-wordpress-publish.",
      "PASS exige HTTP/Playwright do estado resultante, não só código FTP 226."
    ].join(" ")
  },
  {
    id: "ssl-dns-email",
    title: "DNS, SSL, e-mail, backup e cron",
    topics: ["dns", "ssl", "email", "backup", "cron", "logs"],
    source_url: "https://king.host/wiki/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Com o domínio selecionado o painel expõe DNS, SSL, e-mail, backups, cron e logs. Mutação DNS/SSL não é default do MCP de controle.",
      "Backup KingHost ou snapshot FTP+SQL é obrigatório antes de APPLY. rollback_ref aponta para esse snapshot.",
      "Cron do painel dispara PHP/URL no plano; não usar cron não documentado."
    ].join(" ")
  },
  {
    id: "credentials-policy",
    title: "Credenciais já criadas — bind opaco",
    topics: ["credencial", "password", "secret", "env", "ftp user", "mysql user"],
    source_url: "https://king.host/wiki/artigo/como-acessar-painel-de-controle/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Fontes aprovadas: env_reference (KINGHOST_FTP_USER/PASSWORD, KINGHOST_MYSQL_*), secret_reference via runtime-auth, runtime_memory, cookie_session_panel.",
      "Proibido: scrape, brute-force, stuffing, dump de cookie, persistir senha em Git/notebook/PHP/SQL/evidência.",
      "Retorno: credential_ref, username, host, port, environment_id, has_secret. Nunca password."
    ].join(" ")
  }
];

const PANEL_TOOLS = [
  { id: "ftp", family: "publish", title: "Gerenciar FTP" },
  { id: "sftp", family: "publish", title: "SFTP" },
  { id: "ssh", family: "publish", title: "SSH (quando o plano expõe)" },
  { id: "file-manager", family: "files", title: "Gerenciador de arquivos" },
  { id: "mysql", family: "database", title: "Gerenciar bancos MySQL" },
  { id: "phpmyadmin", family: "database", title: "phpMyAdmin" },
  { id: "postgres", family: "database", title: "PostgreSQL (se o plano incluir)" },
  { id: "php-version", family: "runtime", title: "Configuração PHP" },
  { id: "wordpress", family: "application", title: "Gerenciar WordPress" },
  { id: "dns", family: "network", title: "DNS" },
  { id: "ssl", family: "network", title: "SSL" },
  { id: "email", family: "network", title: "E-mail" },
  { id: "backup", family: "operations", title: "Backups" },
  { id: "cron", family: "operations", title: "Cron" },
  { id: "logs", family: "operations", title: "Logs" },
  { id: "resources", family: "operations", title: "Performance / recursos" },
  { id: "git-deploy", family: "publish", title: "Git" },
  { id: "domains", family: "network", title: "Domínios e subdomínios" }
];

function tokenize(value) {
  return String(value || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .split(/[^a-z0-9]+/)
    .filter((token) => token.length >= 2);
}

export function pluginCatalog() {
  return {
    panel_tools: PANEL_TOOLS,
    wordpress_plugins: WORDPRESS_PLUGIN_CATALOG,
    note: "Panel catalog is the documented KingHost Hospedagem surface. WordPress plugin slugs are official-directory identities; live inventory uses FTP/MySQL, not this static list. Undocumented private panel APIs are unsupported."
  };
}

export function knowledgeSearch(query, { limit = 8 } = {}) {
  const tokens = tokenize(query);
  if (tokens.length === 0) {
    return {
      status: "OK",
      query: "",
      matches: ARTICLES.slice(0, limit).map(summarize),
      source_registry: "aeos/knowledge/kinghost-control.sources.yaml",
      official: ["https://painel.kinghost.com.br", "https://king.host/wiki/", "https://king.host/"]
    };
  }
  const scored = ARTICLES.map((article) => {
    const hay = tokenize([article.id, article.title, article.topics.join(" "), article.body].join(" "));
    const score = tokens.reduce((sum, token) => sum + hay.filter((item) => item.includes(token) || token.includes(item)).length, 0);
    return { article, score };
  }).filter((row) => row.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((row) => summarize(row.article, row.score));
  return {
    status: "OK",
    query: String(query || ""),
    matches: scored,
    source_registry: "aeos/knowledge/kinghost-control.sources.yaml",
    freshness_policy: "aeos/policies/kinghost-commerce-freshness.policy.md",
    official: ["https://painel.kinghost.com.br", "https://king.host/wiki/", "https://king.host/"]
  };
}

function summarize(article, score) {
  return {
    id: article.id,
    title: article.title,
    topics: article.topics,
    source_url: article.source_url,
    retrieved_at: article.retrieved_at,
    score: score ?? undefined,
    body: article.body
  };
}

export { ARTICLES, PANEL_TOOLS, WORDPRESS_PLUGIN_CATALOG, RETRIEVED_AT };
