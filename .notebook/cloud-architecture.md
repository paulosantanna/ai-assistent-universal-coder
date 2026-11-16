# cloud-architecture — pesquisa AWS/Azure, MCPs e modelos (2026-11-14)

Updated: 2026-11-14. Entry point: `cloud-architecture-mcp/README.md` (servidores) e `cloud-architecture/README.md` (modelos e docs). Evidence: `.work/cloud-research/` (fora do git).

- Fact: dois MCPs somente leitura (`providers/aws/server.mjs`, `providers/azure/server.mjs`), 6 ferramentas, 27 regras (17 AWS, 10 Azure), 39 testes verdes. Sem credenciais de nuvem.
- Fact: AIHealthResearch as-is (CFN) US$ 6.046,85/mês em sa-east-1; alvo US$ 2.735,52 (-54,8%). Maior custo: endpoint SageMaker sempre ligado (US$ 3.495/mês).
- Fact: MyDigitalBuddy sem backend (app Rust, sem HTTP nem telemetria); nuvem para distribuição, cerca de US$ 0,05/mês.
- Fact: App Runner fechado a novos clientes; ECS Express Mode com ALB interno em sub-redes privadas.
- Fact: Brazil South (PostgreSQL): HA zonal bloqueado para servidor novo e sem backup geo. Artifact Signing não cobre publicador individual no Brasil.
- Decision pendente do dono: Object Lock compliance (ADR), janela de inferência, região sa-east-1 ou us-east-1, certificado Windows, Spot 70% como premissa.
- Pointer: regras e armadilhas em `cloud-architecture-mcp/providers/*/knowledge.json`; claims com triagem JEV em `cloud-architecture-mcp/evidence/claims.json`; preços em `providers/*/prices.json`; modelos em `cloud-architecture/models/`.
- Limit: JEV é triagem (48/50 positivos; 15/15 negativos). Preços de lista. Nada implantado.
- Tags: aws, azure, cost, architecture
