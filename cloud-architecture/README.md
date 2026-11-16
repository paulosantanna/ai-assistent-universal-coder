# cloud-architecture

Pesquisa de arquitetura AWS e Azure (2026-11-14), modelos AWS exclusivos para o MyDigitalBuddy e o AIHealthResearch, mapeamento das APIs locais e testes de regressão. Os servidores MCP estão em `../cloud-architecture-mcp/`.

## Onde está cada coisa

| Caminho | Conteúdo |
| --- | --- |
| `docs/research-2026-11-14.md` | Pesquisa consolidada: princípios, padrões AWS e Azure, comparativo de preço, incertezas e fontes |
| `docs/aws-mydigitalbuddy.md` | Arquitetura AWS de distribuição e CI do aplicativo desktop (sem backend) |
| `docs/aws-aihealthresearch.md` | As-is do CloudFormation, alvo, cenários de custo, decisões pendentes e riscos |
| `docs/azure-aihealthresearch.md` | Equivalente Azure, restrições de Brazil South e preços |
| `models/aws/*.model.json` | Modelos lidos pelo MCP (revisão e custo) |
| `models/azure/aihealthresearch.target.model.json` | Modelo Azure alvo |
| `local-apis.json` | Oito APIs e componentes locais (varredura de rotas do workspace em 2026-11-14), com a fonte de cada campo |
| `tests/local-api-mapping.test.mjs` | Mapeamento das APIs locais e totais de custo dos modelos |

## Resultados principais

| Item | Resultado | Fonte |
| --- | --- | --- |
| AIHealthResearch as-is | US$ 6.046,85/mês | `models/aws/aihealthresearch.as-is.model.json` |
| AIHealthResearch alvo | US$ 2.735,52/mês (-54,8%) | `models/aws/aihealthresearch.target.model.json` |
| MyDigitalBuddy | cerca de US$ 0,05/mês (S3); CloudFront no free tier | `models/aws/mydigitalbuddy.model.json` |
| Armadilhas verificadas | App Runner fechado; CloudFront sem América do Sul; HA zonal bloqueado em Brazil South; Artifact Signing não elegível no Brasil; e outras 23 (27 no total) | `cloud-architecture-mcp/providers/*/knowledge.json` |
| Testes | 39 (MCP) + 16 (mapeamento e modelos) verdes | `npm test` nos dois pacotes |
| Custo reproduzido | diferença de até US$ 0,01 entre o motor Node e um cálculo independente em Python | `.work/cloud-research/verify_costs.py` (fora do git) |
| JEV (triagem) | positivos 48/50; negativos e ausência 15/15 (rodada final); rodada 1 com 43/50 mantida | `cloud-architecture-mcp/evidence/claims.json` |
| Harness de memória | recall@3 = 1,0 em 20 consultas (consultas escritas pelo mesmo agente: não independente) | `.work/cloud-research/evidence/brain-harness.json` |

## Como verificar

```powershell
cd e:\Github\ai-assistent-universal-coder\cloud-architecture-mcp; npm test
cd e:\Github\ai-assistent-universal-coder\cloud-architecture; node --test
```

## Decisões pendentes (dono)

1. Object Lock do arquivo de evidências do AIHealthResearch em **compliance** (irreversível no período). ADR.
2. Janela de inferência real (premissa de 8 h x 22 dias) e aceitação de latência sem escala a zero.
3. Região: sa-east-1 (residência, mais caro) ou us-east-1 (mais barato). ADR.
4. Certificado de assinatura Windows do MyDigitalBuddy (OV de CA ou token), já que Artifact Signing não cobre o Brasil.
5. Desconto Spot de 70% usado como premissa de planejamento; medir com a primeira campanha.
6. Aurora Serverless v2 com 0,5 ACU (lever B3): só após benchmark.

## Limites

- Nada foi implantado, nada foi commitado, nenhuma conta AWS ou Azure foi acessada.
- Preços de lista, sem reservas, Savings Plans, Spot ou impostos.
- O AIHealthResearch continua com a produção médica bloqueada pelo próprio projeto; este modelo não aprova produção.
- Os repositórios em `02_repositorios/` não foram alterados.
