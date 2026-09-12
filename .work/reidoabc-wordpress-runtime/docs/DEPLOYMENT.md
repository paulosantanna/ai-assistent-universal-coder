# Avaliação Local

1. Execute `scripts/start-local.ps1`.
2. Execute `scripts/bootstrap-local-wordpress.ps1`.
3. Abra `http://localhost:8088/` e avalie início, carrinho, Minha Conta, cadastro, checkout, PIX de teste e pedidos em `wp-admin`.
4. Para reiniciar o banco de avaliação, execute `docker compose --env-file .env.local down -v` e inicie novamente. Isso apaga somente o volume Docker local deste projeto.

O banco não tem cópia de dados privados da produção. Os oito produtos são conteúdo de avaliação, criado pelo bootstrap para que a experiência visual e o fluxo de compra possam ser testados.
