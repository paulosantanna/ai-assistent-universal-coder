const RETRIEVED_AT = "2026-09-16";

const WORDPRESS_PLUGIN_CATALOG = [
  { slug: "woocommerce", title: "WooCommerce", kind: "ecommerce", path: "wp-content/plugins/woocommerce", tables: ["woocommerce_order_items", "woocommerce_order_itemmeta", "woocommerce_sessions", "woocommerce_tax_rates", "wc_orders"], notes: "Prefer WooCommerce/WordPress APIs before direct SQL; HPOS may store orders in wc_orders." },
  { slug: "woocommerce-payments", title: "WooCommerce Payments", kind: "ecommerce-payments", path: "wp-content/plugins/woocommerce-payments" },
  { slug: "woocommerce-paypal-payments", title: "WooCommerce PayPal Payments", kind: "ecommerce-payments", path: "wp-content/plugins/woocommerce-paypal-payments" },
  { slug: "woocommerce-mercadopago", title: "Mercado Pago for WooCommerce", kind: "ecommerce-payments", path: "wp-content/plugins/woocommerce-mercadopago" },
  { slug: "jetpack", title: "Jetpack", kind: "platform", path: "wp-content/plugins/jetpack" },
  { slug: "elementor", title: "Elementor", kind: "builder", path: "wp-content/plugins/elementor" },
  { slug: "wordpress-seo", title: "Yoast SEO", kind: "seo", path: "wp-content/plugins/wordpress-seo" },
  { slug: "akismet", title: "Akismet Anti-spam", kind: "security", path: "wp-content/plugins/akismet" },
  { slug: "classic-editor", title: "Classic Editor", kind: "editing", path: "wp-content/plugins/classic-editor" },
  { slug: "contact-form-7", title: "Contact Form 7", kind: "forms", path: "wp-content/plugins/contact-form-7" }
];

const ARTICLES = [
  {
    id: "panel-hosting-surface",
    title: "Painel de Controle KingHost e superfície de Hospedagem",
    topics: ["painel", "login", "cookie", "hospedagem", "dominio", "ftp", "mysql", "ssl", "email", "performance"],
    source_url: "https://king.host/wiki/artigo/manual-de-primeiros-passos/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "O Painel de Controle KingHost é a superfície operacional para selecionar o domínio e administrar DNS, FTP, bancos, WordPress, PHP, SSL, e-mail, backup, cron, antivírus, performance e outros recursos disponibilizados pelo plano.",
      "AEOS autentica o painel por cookie/cookie-jar externo e só expõe panel_session_ref; valores de cookie, senhas e nonces não entram em Git, notebook ou evidência.",
      "Vídeos do canal oficial KingHost são fonte educacional. Qualquer operação mutável aprendida em vídeo deve ser corroborada pela Wiki atual ou pelo painel ao vivo antes da execução."
    ].join(" ")
  },
  {
    id: "domains-dns-subdomains",
    title: "Domínios, subdomínios e Zona DNS",
    topics: ["dominio", "dominios", "subdominio", "dns", "a", "cname", "mx", "txt", "cdn", "restore"],
    source_url: "https://www.youtube.com/watch?v=6cqy_R7OGu8",
    retrieved_at: RETRIEVED_AT,
    body: [
      "O canal oficial demonstra gerenciamento de Zona DNS com registros A, CNAME, MX e TXT, criação de apontamentos para e-mail, subdomínios/CDN e restauração das configurações padrão.",
      "Subdomínio é associado a conteúdo/pasta ou redirecionamento conforme a configuração de hospedagem.",
      "Mudança DNS é operação de infraestrutura: capturar estado anterior, TTL quando visível, diff, rollback e verificação autoritativa antes de declarar PASS. Não inventar API privada do painel."
    ].join(" ")
  },
  {
    id: "ftp-ssh-webftp",
    title: "FTP, WebFTP, SSH e publicação de arquivos",
    topics: ["ftp", "webftp", "ssh", "sftp", "arquivo", "clone", "upload", "publish", "usuario adicional"],
    source_url: "https://king.host/wiki/base-de-conhecimento/gerenciar-ftp/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Gerenciar FTP informa host, usuário e senha, permite alterar senha, política de IP, habilitar/desabilitar serviço e criar usuário adicional restrito a uma pasta.",
      "SSH pode ser usado quando o plano expõe o recurso; a documentação KingHost o descreve como acesso criptografado ao ambiente e ao console de banco em cenários suportados.",
      "AEOS usa credential_ref opaco, ftp.tree.download/site.clone para clone e ftp.tree.upload/deploy.workspace_to_production para publicação. wp-config.php e core WordPress ficam fora do upload padrão.",
      "Usuários adicionais devem seguir least privilege e escopo de pasta. Nunca descobrir ou extrair senhas existentes."
    ].join(" ")
  },
  {
    id: "git-publish",
    title: "Publicação via GitHub, GitLab e Bitbucket",
    topics: ["git", "github", "gitlab", "bitbucket", "deploy", "publish", "webhook", "master"],
    source_url: "https://king.host/wiki/base-de-conhecimento/git/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "A ferramenta Publicação via Git integra o projeto ao Painel de Controle e sincroniza conteúdo do branch configurado para o FTP/diretório escolhido.",
      "A documentação cita GitHub, GitLab e Bitbucket e integração por chaves/autorizações do painel.",
      "Diretório de publicação precisa atender aos pré-requisitos documentados; aplicações Node.js, Rails e Python usam diretórios específicos.",
      "Em AEOS, Git publish não substitui backup, dry-run, rollback e smoke de produção."
    ].join(" ")
  },
  {
    id: "mysql-database",
    title: "MySQL KingHost, phpMyAdmin e acesso governado",
    topics: ["mysql", "banco", "database", "phpmyadmin", "usuario", "query", "wordpress", "backup"],
    source_url: "https://king.host/wiki/base-de-conhecimento/mysql/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "MySQL é disponibilizado nos planos Linux compatíveis e pode ser criado/gerenciado pelo Painel de Controle. Confirmar host, porta, database e política de IP no painel; não deduzir valores.",
      "phpMyAdmin é canal administrativo humano. O MCP usa mysql2 com credential_ref opaco: SELECT/SHOW/DESCRIBE/EXPLAIN por padrão; mutação exige approval, change_id, rollback_ref e dry-run.",
      "Usuário adicional de MySQL deve ser provisionado no painel e limitado ao necessário. Senhas nunca retornam do MCP.",
      "WordPress usa DB_NAME, DB_USER, DB_PASSWORD, DB_HOST e table_prefix em wp-config.php; esses valores são secretos e não devem ser persistidos em evidência."
    ].join(" ")
  },
  {
    id: "backup-recovery",
    title: "Backup e recuperação de site, FTP, bancos e e-mails",
    topics: ["backup", "restore", "recovery", "ftp", "site", "mysql", "postgres", "mssql", "firebird", "email", "dump"],
    source_url: "https://king.host/wiki/artigo/como-solicitar-backup/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "A KingHost documenta retenção padrão de até 7 dias para FTP/web, bancos e e-mails no fluxo de backup do painel.",
      "FTP/web e e-mails usam backup diferencial; bancos são copiados por dump completo. A restauração deve ser tratada como mudança de produção com snapshot do estado atual e verificação pós-restore.",
      "E-mail recuperável depende de conteúdo preservado no servidor: IMAP ou POP configurado para manter cópia.",
      "Backup solicitado pelo painel pode ser enviado ao FTP conforme o tipo selecionado. O fluxo AEOS registra somente referências/metadados, nunca conteúdo sensível do dump em prompts.",
      "Antes de qualquer APPLY destrutivo: confirmar restore path e rollback_ref."
    ].join(" ")
  },
  {
    id: "antivirus-malware",
    title: "Antivírus KingHost, malware e quarentena",
    topics: ["antivirus", "virus", "malware", "scan", "varredura", "quarentena", "security", "ftp"],
    source_url: "https://king.host/wiki/artigo/escanear-seu-site-antivirus/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "O Painel de Controle permite escanear todos os arquivos presentes no FTP. A documentação informa limite de até 3 varreduras por dia.",
      "Arquivos detectados podem ser movidos automaticamente para diretório de quarentena acima da pasta web. A KingHost alerta para falsos positivos e possível indisponibilidade do site.",
      "Para conteúdo acima de 2 GB, a documentação recomenda varredura na fonte/repositório local.",
      "AEOS deve capturar inventário/hashes antes da varredura, executar smoke após o scan e nunca excluir automaticamente o conteúdo da quarentena sem análise e aprovação."
    ].join(" ")
  },
  {
    id: "waf-security",
    title: "Smart WAF e proteção da aplicação",
    topics: ["waf", "firewall", "security", "monitoramento", "protecao", "ataque", "http"],
    source_url: "https://king.host/wiki/artigo/como-configurar-e-utilizar-o-smart-waf/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "O Smart WAF filtra requisições da aplicação web e disponibiliza regras prontas, ajuste de abrangência e modo de monitoramento antes da proteção efetiva.",
      "Mudanças de WAF podem gerar bloqueio indevido. Preferir monitoramento/canary, registrar exceções de forma mínima e verificar login, checkout, APIs e webhooks após mudança.",
      "Não desabilitar proteção globalmente para contornar um falso positivo sem diagnóstico e rollback."
    ].join(" ")
  },
  {
    id: "ssl-https",
    title: "SSL Let's Encrypt, HTTPS e SSL de e-mail",
    topics: ["ssl", "https", "lets encrypt", "certificate", "email ssl", "tls", "wordpress"],
    source_url: "https://king.host/wiki/artigo/instalar-certificado-ssl-lets-encrypt/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Let's Encrypt pode ser ativado pelo painel quando os requisitos de DNS/hospedagem documentados são atendidos; a renovação é automática conforme o produto.",
      "Após ativar HTTPS, verificar mixed content e referências HTTP na aplicação/banco antes de declarar PASS.",
      "SSL personalizado para e-mail também depende de pré-requisitos de DNS documentados.",
      "Mudança de SSL exige smoke externo, cadeia válida e confirmação de hostname."
    ].join(" ")
  },
  {
    id: "email-professional",
    title: "E-mail profissional, Webmail, IMAP/POP e backup",
    topics: ["email", "e-mail", "webmail", "imap", "pop", "smtp", "outlook", "thunderbird", "backup", "mx"],
    source_url: "https://www.youtube.com/watch?v=OzTvUGCMLtg",
    retrieved_at: RETRIEVED_AT,
    body: [
      "O canal oficial demonstra criação de conta de e-mail após selecionar o domínio no painel e acesso por Webmail ou clientes como Outlook/Thunderbird/celular.",
      "Registro de domínio e DNS/MX corretos fazem parte do fluxo de e-mail profissional.",
      "Backup de e-mails é diferencial e recupera conteúdo mantido no servidor; confirmar IMAP ou POP com cópia no servidor.",
      "Senhas de caixas postais são secrets de runtime e nunca devem ser armazenadas em notebooks, relatórios ou repositório."
    ].join(" ")
  },
  {
    id: "php-cron-runtime",
    title: "PHP, Composer e Cronjob",
    topics: ["php", "composer", "cron", "cronjob", "runtime", "versao", "fpm", "script"],
    source_url: "https://king.host/wiki/artigo/como-configurar-cronjob/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Versão PHP é configurada por domínio no painel. Sempre confirmar as versões realmente oferecidas pelo plano atual; páginas antigas da Wiki podem listar versões obsoletas.",
      "Atualização PHP deve passar por compatibilidade, backup, staging quando possível, testes de aplicação e rollback.",
      "Cronjob permite executar comandos/processos em horários ou intervalos definidos e pode servir a relatórios, newsletters e backups periódicos.",
      "Composer é suportado em cenários documentados; dependências devem permanecer reproduzíveis e versionadas por lockfile quando aplicável."
    ].join(" ")
  },
  {
    id: "performance-varnish",
    title: "Performance, consumo, Varnish e otimização",
    topics: ["performance", "varnish", "cache", "pagespeed", "cpu", "memoria", "latencia", "otimizacao", "stats"],
    source_url: "https://king.host/wiki/artigo/varnish-cache/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Varnish fica entre usuário e servidor web e pode reduzir requisições ao backend. A configuração permite TTL, exceções por URL/querystring/cookie e limpeza explícita de cache.",
      "A ativação pode alterar apontamentos DNS do host segundo a documentação; capturar DNS customizado antes de ativar e revalidar depois.",
      "WordPress/Loja Virtual podem ter cache previamente otimizado pelo produto; não duplicar camada sem verificar o plano.",
      "A ferramenta Performance mostra consumo e realtime. Otimização deve priorizar medição: PHP suportado, compressão quando aplicável, minificação/build, cache, imagens, consultas SQL/índices e PageSpeed/Core Web Vitals.",
      "Após publish, limpar somente os caches necessários e validar conteúdo dinâmico, sessão, login e checkout."
    ].join(" ")
  },
  {
    id: "wordpress-hosting",
    title: "WordPress na KingHost",
    topics: ["wordpress", "wp-admin", "plugin", "theme", "woocommerce", "instalador", "update", "publish"],
    source_url: "https://king.host/wiki/artigo/como-gerenciar-o-wordpress-no-painel-de-controle-da-kinghost/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Gerenciar WordPress permite selecionar instalação e administrar recursos documentados como versão, PHP, atualizações, plugins e temas conforme o produto.",
      "Instalação automática define domínio/pasta/subdomínio, idioma e credenciais wp-admin. Senhas não entram em evidência AEOS.",
      "wordpress-expert governa alterações de tema/plugin/bloco; core, wp-admin, wp-includes e wp-config.php não são editados para feature work.",
      "WooCommerce é plugin WordPress. Preservar pedidos, clientes, siteurl/home e segredos de pagamento de produção no publish padrão."
    ].join(" ")
  },
  {
    id: "production-publish",
    title: "Clone, alteração local e publicação segura",
    topics: ["clone", "deploy", "publish", "producao", "rollback", "dry-run", "ftp", "wordpress", "woocommerce"],
    source_url: "https://king.host/wiki/base-de-conhecimento/gerenciar-ftp/",
    retrieved_at: RETRIEVED_AT,
    body: [
      "Fluxo AEOS: autenticar painel → listar/selecionar domínio → bind FTP/MySQL → inventário → snapshot → diff → dry-run → backup → APPLY → VERIFY → CLOSE.",
      "Comando existente: npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <dominio>. O playbook é kinghost-wordpress-publish.",
      "Git publish do painel é alternativa quando apropriada, mas não elimina os gates de backup/rollback/smoke.",
      "PASS exige estado HTTP/WordPress funcional após a mudança, não somente FTP 226 ou webhook concluído."
    ].join(" ")
  }
];

const PANEL_TOOLS = [
  { id: "domains", family: "network", title: "Domínios e subdomínios" },
  { id: "dns", family: "network", title: "Zona DNS" },
  { id: "ssl", family: "security", title: "Certificado SSL / HTTPS" },
  { id: "ftp", family: "publish", title: "Gerenciar FTP" },
  { id: "webftp", family: "files", title: "WebFTP" },
  { id: "ssh", family: "publish", title: "SSH quando disponível no plano" },
  { id: "git-deploy", family: "publish", title: "Publicação via Git" },
  { id: "mysql", family: "database", title: "Gerenciar bancos MySQL" },
  { id: "phpmyadmin", family: "database", title: "phpMyAdmin" },
  { id: "wordpress", family: "application", title: "Gerenciar WordPress" },
  { id: "php-version", family: "runtime", title: "Configuração PHP" },
  { id: "cron", family: "runtime", title: "Cronjob" },
  { id: "email", family: "messaging", title: "E-mail / Webmail" },
  { id: "email-ssl", family: "security", title: "SSL de e-mail" },
  { id: "backup", family: "operations", title: "Backup e recuperação" },
  { id: "antivirus", family: "security", title: "Antivírus / quarentena" },
  { id: "waf", family: "security", title: "Smart WAF" },
  { id: "varnish", family: "performance", title: "Varnish Cache" },
  { id: "performance", family: "performance", title: "Performance / consumo / realtime" },
  { id: "logs", family: "operations", title: "Logs" }
];

function tokenize(value) {
  return String(value || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .split(/[^a-z0-9]+/)
    .filter((token) => token.length >= 2);
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

export function pluginCatalog() {
  return {
    panel_tools: PANEL_TOOLS,
    wordpress_plugins: WORDPRESS_PLUGIN_CATALOG,
    note: "Panel catalog is the documented KingHost Hospedagem surface. Live availability depends on the contracted plan and selected domain. Undocumented private panel APIs are unsupported."
  };
}

export function knowledgeSearch(query, { limit = 10 } = {}) {
  const tokens = tokenize(query);
  const matches = tokens.length === 0
    ? ARTICLES.slice(0, limit).map((article) => summarize(article))
    : ARTICLES.map((article) => {
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
    matches,
    source_registry: "aeos/knowledge/kinghost-control.sources.yaml",
    freshness_policy: "aeos/policies/kinghost-commerce-freshness.policy.md",
    official: [
      "https://painel.kinghost.com.br",
      "https://king.host/wiki/",
      "https://site.king.host/hospedagem-de-sites",
      "https://www.youtube.com/@kinghost"
    ],
    rule: "Video-derived claims are educational evidence; mutable behavior must be corroborated by current official docs or the live panel."
  };
}

export { ARTICLES, PANEL_TOOLS, WORDPRESS_PLUGIN_CATALOG, RETRIEVED_AT };
