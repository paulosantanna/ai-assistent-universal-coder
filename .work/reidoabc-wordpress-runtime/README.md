# Rei do ABC WordPress

Aplicação WordPress completa para avaliação local. A página gourmet foi migrada para um tema filho Storely e os dados de catálogo, clientes, endereços e pedidos são persistidos pelo WooCommerce no MySQL.

## Executar localmente

```powershell
.\scripts\start-local.ps1
.\scripts\bootstrap-local-wordpress.ps1
```

Abra `http://localhost:8088/`. O administrador local é `reidoabc_admin`; a senha é gerada somente em `.env.local`, arquivo ignorado pelo Git.

O bootstrap é idempotente e configura WordPress 7.1, PHP 8.5, MySQL 8.4, WooCommerce 11.1, HPOS, BRL, cadastro de conta, checkout e oito produtos locais de avaliação. A chave PIX criada localmente é apenas para teste; configure uma chave e um provedor de pagamentos reais antes de qualquer produção.

## Estrutura

- `wp-content/themes/reidoabc-gourmet` contém o storefront, a paleta `#302c9b` e a reserva para a primeira imagem do carrossel.
- `wp-content/plugins/reidoabc-commerce` restringe o catálogo a Pedaços de Tortas e Barras de Chocolate e adiciona o PIX manual persistido pelo WooCommerce.
- `wp-content/mu-plugins/reidoabc-hardening.php` mantém bloqueio de XML-RPC, limitação de login/REST, proteção de enumeração e cabeçalhos de segurança.
- `wp-content/uploads/seed-products` contém as imagens de demonstração usadas localmente pelo catálogo.
- `docs/PRODUCTION_READINESS.md` define a infraestrutura necessária antes de uma publicação na KingHost.

## Limites de produção

Não publique este diretório diretamente sem seguir `docs/PRODUCTION_READINESS.md`. O código reduz riscos no aplicativo, mas criptografia de banco, backups, CDN, WAF, mitigação DDoS e escala horizontal precisam ser aplicados na infraestrutura de produção. Nenhuma publicação na KingHost é feita por este projeto.
