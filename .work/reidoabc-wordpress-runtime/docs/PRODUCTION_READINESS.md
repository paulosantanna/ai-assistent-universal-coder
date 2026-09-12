# Prontidão para Produção

## Antes de publicar

1. Obter backup íntegro de arquivos e banco da produção, testar a restauração e definir rollback.
2. Migrar a base real para staging, incluindo mídia privada, configurações de frete, impostos, e-mail e meios de pagamento.
3. Definir os segredos em um cofre do provedor e preencher as variáveis de `config/production.env.example` fora do Git.
4. Configurar Mercado Pago/PIX com credenciais oficiais. O PIX local de demonstração não pode ser usado em produção.
5. Configurar SMTP/transacional autenticado com domínio verificado, SPF, DKIM e DMARC. O ambiente local suprime e-mails para não depender de `sendmail`.
6. Fazer testes de conta, recuperação de senha, carrinho, cupom, frete, checkout, pagamento, e-mail de pedido, cancelamento e reembolso.

## Escala e DDoS

Milhões de acessos simultâneos exigem camada de borda e capacidade horizontal; uma única máquina PHP/MySQL não é suficiente. Use CDN com cache de páginas anônimas e ativos, WAF com regras gerenciadas, rate limit por IP e desafio para tráfego anômalo, balanceador com múltiplas instâncias PHP, Redis compartilhado para objeto/sessão, MySQL gerenciado com réplicas de leitura e monitoramento de latência, erros, taxa de checkout e fila de e-mails. `wp-cron` deve ser executado por cron do servidor, não por visita.

## Dados e privacidade

Exija TLS 1.2+ entre cliente, CDN, aplicação e banco; criptografia de volume/tablespace e backup com KMS; acesso de banco por rede privada; rotação de credenciais; MFA no painel; menor privilégio; retenção mínima de pedidos e logs; e processo de exportação/eliminação de dados pessoais. Não grave tokens de pagamento, senhas, cookies ou chaves na base WordPress.

## Publicação na KingHost

Valide primeiro se o plano oferece PHP 8.5, MySQL compatível, TLS, cron, WAF/CDN e backup criptografado. Caso algum desses pontos não exista, mantenha a aplicação em um ambiente que os forneça. Não executar deploy sem staging, backup e rollback aprovados.
