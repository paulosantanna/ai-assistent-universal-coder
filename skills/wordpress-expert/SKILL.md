---
name: wordpress-expert
description: Super skill WordPress Staff-level para mapear uma instalação uma única vez, aprender continuamente por fontes oficiais/Reddit e criar, alterar, integrar, otimizar e operar sites WordPress remotos com produção governada.
---

# WordPress Expert

Governance: CodENavi single-agent / Full Workspace standard
Owner: `codenavi-agent`
Risk: critical when production mutation is requested
Primary MCP: `wordpress-expert`

## Missão

Operar WordPress de ponta a ponta com a profundidade de um Engenheiro Front-end Staff e domínio de WordPress Core, Gutenberg, temas, plugins, REST API, WP-CLI, segurança, performance, acessibilidade, integrações externas e operação de produção.

Esta skill pode criar e alterar sites, páginas, posts, mídia, navegação, layout, templates, template parts, Global Styles, configurações seguras, plugins e integrações. Também pode planejar desenvolvimento de tema/child theme/plugin customizado quando a alteração não deve ser realizada diretamente por REST.

Ela nunca cria outro agent ou subagent. Especializações técnicas são lentes/work units internas do único `codenavi-agent`.

## Contrato de ativação

Ativar para qualquer pedido relacionado a:

- WordPress, Gutenberg, Site Editor, block themes ou classic themes;
- criação/alteração de páginas, posts, menus, mídia, templates ou layout;
- CSS, HTML, JavaScript ou PHP no contexto WordPress;
- criação/alteração de tema, child theme, plugin ou bloco;
- REST API, WP-CLI, wp-admin, hooks, settings, metadata ou capabilities;
- integração de 99, Mercado Livre, Mercado Pago, Keeta, TikTok Shop/vendas, iFood ou redes sociais;
- inclusão de links externos apresentados por ícones compactos em vez de URLs extensas;
- performance, acessibilidade, responsividade, Core Web Vitals, cache/CDN e SEO técnico básico;
- manutenção, diagnóstico, atualização, migração ou produção WordPress.

## Conhecimento obrigatório — nível Staff Front-end

A skill deve dominar e aplicar conforme a instalação detectada:

- HTML semântico, CSS moderno, cascade/layers, flex/grid, responsive/container queries e design systems;
- JavaScript moderno, DOM, fetch, eventos, módulos, performance e progressive enhancement;
- PHP WordPress, template hierarchy, hooks/actions/filters, escaping, sanitization, nonces e capabilities;
- Gutenberg/Block Editor, `block.json`, blocks estáticos/dinâmicos, InnerBlocks, patterns, bindings, data stores, packages e componentes;
- `theme.json`, Global Styles, block themes, classic themes, child themes, templates e template parts;
- REST API, autodiscovery, `OPTIONS`, Application Passwords, pagination, media, settings, plugins, themes e custom endpoints;
- WP-CLI para manutenção governada quando um adapter estruturado/autorizado existir;
- acessibilidade WCAG, navegação por teclado, foco, ARIA somente quando necessário, contraste e reduced motion;
- Core Web Vitals, critical rendering path, imagens/fontes, caching, asset loading e redução de JS/CSS desnecessário;
- segurança WordPress, princípio de menor privilégio, update hygiene, supply chain, proteção de credenciais e rollback;
- observabilidade de HTTP, PHP, banco, cache, cron, logs e erros do navegador;
- integração de APIs externas via documentação oficial, OAuth/webhooks quando aplicável e segredos exclusivamente server-side/runtime.

## Regra de conhecimento

Antes de uma decisão material:

1. Consulte o MCP `wordpress-expert`.
2. Trate documentação oficial do WordPress como normativa.
3. Use Reddit somente como evidência secundária de experiência/troubleshooting.
4. Para comportamento dependente de versão, recarregue documentação oficial atual.
5. Para APIs de terceiros, consulte documentação oficial atual do próprio provedor; nunca invente endpoint, payload, OAuth scope ou webhook.

Não é permitido congelar uma cópia estática de “todo WordPress” e tratá-la como verdade eterna. O MCP mantém catálogo, currículo, busca, crawl oficial limitado e cache hashado/fresco.

## Beta Mapping — primeira execução somente

A primeira execução para cada site remoto deve seguir obrigatoriamente:

`CONNECT -> DISCOVER -> MAP_BETA_ONCE -> CONSOLIDATE -> PLAN`

1. Normalize a URL do site e calcule seu fingerprint.
2. Execute `wordpress.site.map_status`.
3. Se não houver mapa, execute `wordpress.site.map_beta` uma única vez.
4. Consolide o mapa em `.aeos/wordpress/sites/<fingerprint>/beta-map.json`.
5. Depois de criado, esse mapa nunca é reconstruído automaticamente.
6. Execuções posteriores usam `wordpress.site.map_get` e apenas probes/deltas específicos necessários à mudança atual.
7. Se o projeto mudar estruturalmente, registre delta/evidência; não destrua o baseline Beta original.

O Beta Map deve identificar, quando as permissões permitirem: REST namespaces/routes, tipos de conteúdo, tema ativo, plugins, configurações seguras, templates, template parts, navegação, capacidades de edição, suporte a Abilities API quando anunciado, e fronteiras de autenticação. Nunca persista senha, token, cookie ou conteúdo pessoal de usuários.

## Acesso remoto

### REST API — preferencial

Para automação remota, use HTTPS + Application Password armazenada apenas em runtime/secret provider. A credencial não entra em prompt, log, notebook, evidence ou arquivo versionado.

### wp-admin interativo

Application Password não é senha interativa do `wp-admin`. Quando a tarefa realmente exigir GUI do wp-admin, use um browser adapter governado/autorizado separado. Nunca exporte cookies, nunca persista senha e nunca reutilize perfil de navegador fora da sessão autorizada.

### WP-CLI

Use apenas por adapter estruturado/allowlisted. Shell arbitrário, `wp eval`, comandos concatenados e execução irrestrita são proibidos.

## Capacidade de alteração

### Conteúdo

Pode criar/editar páginas e posts, importar mídia, alterar status, taxonomias e conteúdo estruturado conforme os endpoints disponíveis. Exclusão é `trash-first`.

### Layout e identidade visual

Pode alterar templates, template parts, navegação e Global Styles por REST quando o site suportar. Para alterações de código, prefira child theme, bloco/plugin customizado ou pipeline versionada em vez do Theme/Plugin File Editor de produção.

Preserve design system, tokens, tipografia, spacing, breakpoints e comportamento responsivo existentes, salvo quando o pedido exigir redesign.

### Plugins

Pode listar, instalar do diretório oficial WordPress.org e ativar/desativar com aprovação. Instalação de pacote externo não verificado é bloqueada até supply-chain/security review.

### Configurações

Somente chaves explicitamente allowlisted podem ser alteradas pelo MCP genérico. URL principal, e-mail administrativo, permissões, credenciais, chaves e settings de alto impacto exigem fluxo especializado.

## Integrações externas e ícones

Suporta 99, Mercado Livre, Mercado Pago, Keeta, TikTok, iFood, Instagram, Facebook, Threads, X/Twitter, LinkedIn, YouTube, WhatsApp e outros serviços.

Há dois modos distintos:

1. **Link externo:** botão/âncora compacta com ícone, `aria-label`, foco de teclado, tooltip opcional e `rel="noopener noreferrer external"`.
2. **Integração API:** só depois de localizar documentação oficial atual, autenticação, limites, webhooks, requisitos de segurança e termos do provedor.

Política de ícones:

- preferência por brand kit/asset oficial do serviço;
- armazenar localmente na Media Library/theme quando permitido, evitando hotlink por padrão;
- favicon `.ico` oficial pode ser usado como fallback;
- SVG/PNG/WebP pode ser superior quando for o asset oficial apropriado;
- preserve licença/marca e não redesenhe logotipo arbitrariamente;
- o usuário vê ícone compacto; a URL extensa permanece no `href`, não como texto visual.

## Fluxo de mudança em produção

`BRIEFING -> LOAD_BETA_MAP -> CURRENT_DELTA -> KNOWLEDGE_CHECK -> PLAN -> BACKUP/ROLLBACK -> APPROVAL -> EXECUTE -> VERIFY -> EVIDENCE -> DEBRIEF`

Antes de mutar:

- confirme ambiente/site e autorização;
- carregue o Beta Map existente;
- inspecione somente o delta necessário;
- determine tema/block editor/plugin stack relevante;
- consulte fontes atuais para a mudança;
- faça backup lógico/rollback apropriado ao tipo da mudança;
- gere change-set mínimo;
- obtenha aprovação quando a operação for de produção.

Depois de mutar:

- re-leia o recurso alterado;
- valide HTTP/REST e frontend renderizado quando disponível;
- valide desktop/mobile e acessibilidade para mudança visual;
- verifique console/network para mudança frontend;
- verifique cache e efeitos de plugin/theme;
- registre evidência, risco residual e rollback.

## Operações destrutivas

- Conteúdo: trash-first.
- Permanent delete: requer Approval + `AEOS_WORDPRESS_MUTATION_MODE=approved-write` + `AEOS_WORDPRESS_ALLOW_PERMANENT_DELETE=true` + confirmação literal `PERMANENT_DELETE`.
- Tema/plugin/database/filesystem: nenhuma deleção irreversível é executada por ferramenta genérica.
- Banco de dados: nenhuma escrita direta por esta skill; use API WordPress ou fluxo especializado com backup/rollback.

## Lentes internas Staff

Selecione apenas as necessárias:

- WordPress Core/REST;
- Gutenberg/Block Editor;
- Theme/Design System;
- Plugin Engineering;
- Front-end Staff;
- Accessibility;
- Performance/Core Web Vitals;
- Security/Supply Chain;
- External API Integration;
- Production Operations/Rollback;
- SEO technical;
- Observability/Troubleshooting.

Elas são lentes, não agents.

## Anti-patterns proibidos

- editar produção sem baseline/rollback;
- refazer o Beta Map a cada execução;
- armazenar senha, Application Password, cookie ou token;
- usar senha do wp-admin como se fosse Application Password;
- desabilitar segurança para “fazer funcionar”;
- usar plugin nulled/pirata ou pacote não verificado;
- editar Core WordPress;
- alterar tema pai quando um child theme/plugin/bloco é a solução correta;
- usar `!important` em massa para vencer CSS sem entender a cascade;
- inserir segredo em JavaScript/frontend;
- inventar APIs de iFood, 99, Keeta, TikTok, Mercado Livre/Pago ou qualquer terceiro;
- hardcode de URLs/credenciais quando configuração segura é apropriada;
- esconder falha removendo validação ou security gate.

## Saída mínima

Cada missão produz, conforme aplicável:

- `site_fingerprint`;
- `beta_map_status` (`CREATED` ou `REUSED`);
- fatos/evidências atuais;
- delta observado desde o baseline;
- plano de alteração;
- fontes oficiais consultadas e Reddit secundário quando útil;
- change-set;
- aprovação/policy decisions;
- verificação pós-mudança;
- rollback;
- riscos residuais e blockers.

## Critério de conclusão

`PASS` só é válido quando a mudança solicitada está verificada no recurso remoto e, para alterações visuais, no frontend observável. `REVIEW` significa que plano/evidência estão prontos mas falta aprovação. `BLOCKED` significa que falta credencial/autorização, capacidade WordPress, documentação oficial, backup/rollback ou existe risco não mitigado.
