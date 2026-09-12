# Auditoria de Segurança Local

## Controles implementados

- WordPress 7.1, PHP 8.5 e MySQL 8.4 no ambiente local.
- Storely 29.2 e WooCommerce 11.1.0 no clone, substituindo as versões públicas mapeadas anteriormente.
- Senhas de usuários seguem o hash nativo do WordPress; não há login ou cadastro em `localStorage`.
- Salts, senhas de banco e senha de administrador local são gerados em `.env.local` e não entram no Git.
- XML-RPC, edição de arquivos no painel e Application Passwords são desativados.
- Cabeçalhos, bloqueio de leitura de arquivos sensíveis, bloqueio de PHP em uploads, limitação de tentativas de login e limitação de chamadas REST em lote estão ativos.
- Consultas de catálogo usam APIs do WooCommerce/WordPress, com escaping na saída e sem SQL manual.

## CVEs e atualizações

O tema Storely público mapeado na produção original estava na versão 7.1, afetada por CVE-2024-10847 e CVE-2024-51794 em versões anteriores à correção. O clone usa Storely 29.2. O WooCommerce 10.3.8 da produção estava corrigido para o aviso Store API de março de 2026 em sua linha, mas o clone usa WooCommerce 11.1.0 para a validação atualizada. Atualizações futuras exigem nova revisão de CVEs e teste em staging.

## Controles que dependem da hospedagem

Não há forma correta de prometer criptografia integral de dados do WooCommerce apenas com código PHP. Para produção, a infraestrutura deve fornecer TLS fim a fim, disco e backups criptografados com chave gerenciada, banco acessível apenas por rede privada/TLS, rotação de segredos e logs sem dados pessoais. O valor `REIDOABC_DATA_ENCRYPTION` é obrigatório fora do ambiente local para impedir inicialização com configuração incompleta, mas a criptografia em repouso é responsabilidade comprovável do provedor de banco/backup.
