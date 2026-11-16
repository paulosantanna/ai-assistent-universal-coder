# cloud-architecture-mcp

Dois servidores MCP somente leitura, um para AWS e outro para Azure. Eles revisam arquiteturas, mapeiam APIs locais e estimam custo mensal, sempre com fonte e regra registradas. Não usam credenciais de nuvem, não escrevem na nuvem e não fazem deploy.

- `providers/aws/server.mjs`: `aws-architecture-mcp`
- `providers/azure/server.mjs`: `azure-architecture-mcp`

## Ferramentas (as mesmas nos dois servidores)

| Ferramenta | Para que serve | Falha quando |
| --- | --- | --- |
| `list_patterns` | Lista padrões verificados (id, título, categoria, quando usar) | — |
| `get_pattern` | Detalha um padrão com componentes, alavancas de custo e claims (URL, rótulo final) | id desconhecido |
| `list_pitfalls` | Erros conhecidos: premissa errada, fato correto, regra que detecta, claims rejeitados | — |
| `review_architecture` | Revisa um modelo JSON contra 27 regras (17 AWS, 10 Azure) | modelo de outro provedor |
| `map_local_api` | Mapeia uma API ou componente local para serviços do provedor, com restrições e proibições | tipo ou estado desconhecido |
| `estimate_monthly_cost` | Estima custo mensal a partir do snapshot versionado de preços | SKU desconhecido ou de outro provedor |

Todas as ferramentas têm `annotations.readOnlyHint: true` e schema de entrada.

## Como rodar

```powershell
cd e:\Github\ai-assistent-universal-coder\cloud-architecture-mcp
node providers\aws\server.mjs      # stdio; uma mensagem JSON-RPC por linha
npm test                           # 39 testes: conhecimento, armadilhas, custo, protocolo
```

Registro no cliente MCP (exemplo; não grava nada automaticamente):

```json
{
  "mcpServers": {
    "aws-architecture": { "command": "node", "args": ["e:\\Github\\ai-assistent-universal-coder\\cloud-architecture-mcp\\providers\\aws\\server.mjs"] },
    "azure-architecture": { "command": "node", "args": ["e:\\Github\\ai-assistent-universal-coder\\cloud-architecture-mcp\\providers\\azure\\server.mjs"] }
  }
}
```

## Garantias de desenho

- **Decisão é código**: a revisão e o mapeamento são regras determinísticas. A triagem do JEV fica nos metadados das claims e nunca decide.
- **Falha fechada**: tipo de API desconhecido, estado desconhecido, SKU sem preço e claim sem fonte geram erro, não palpite.
- **Armadilhas viram regra**: cada regra tem um modelo-armadilha nos testes (`tests/engine.test.mjs`). Se a regra deixar de disparar, o teste quebra. Esse é o mecanismo para não repetir erros.
- **Protocolo**: JSON-RPC 2.0 por stdio, na revisão `2025-11-25`, sem SDK novo (mesma convenção dos outros MCPs do workspace). Se o cliente exigir outra revisão, ajustar em `shared/stdio-mcp.mjs`.

## Dados e proveniência

| Arquivo | Conteúdo | Gerado por |
| --- | --- | --- |
| `evidence/claims.json` | 65 claims com URL, trecho, rótulo JEV e rótulo final | `scripts/build_evidence.py` (entrada: dossiê em `.work/cloud-research/`, fora do git) |
| `providers/aws/knowledge.json` | 10 padrões e 15 armadilhas AWS, com claims | escrito à mão, validado por `validateKnowledge` |
| `providers/azure/knowledge.json` | 9 padrões e 12 armadilhas Azure, com claims | escrito à mão, validado por `validateKnowledge` |
| `providers/aws/prices.json` | 46 SKUs (23 por região: sa-east-1 e us-east-1), com hash do arquivo de origem | `scripts/build_prices.py` (entrada: Price List pública) |
| `providers/azure/prices.json` | 13 SKUs (brazilsouth e eastus) | `scripts/build_prices.py` (entrada: Retail Prices API) |

Regenerar: `python scripts/build_evidence.py --claims <claims.py> --triage <jev-triage.json> --out evidence/claims.json` e `python scripts/build_prices.py --aws <aws-prices.json> --azure <azure-prices.json> --root .`.

Rótulos finais: `supported` (JEV ≥ 0,7), `supported_historical` e `supported_manual` (dois casos limítrofes verificados à mão, com motivo), `not_supported` (JEV ≤ 0,3, inclui controles-armadilha). Claims de controle nunca são usadas como evidência de apoio; são listadas como `rejected_claims`.

## Limites

- Preços são de lista (sem Savings Plans, reservas, Spot nem impostos). Itens sem linha no snapshot não são estimados.
- Não há cliente de nuvem: a ferramenta não consulta preços em tempo real nem valida recursos reais.
- O servidor oficial do Azure MCP (`microsoft/mcp`) faz operações; este aqui só revisa e orienta. Não substitui.
- Atualizar o dossiê exige nova rodada de pesquisa e de JEV; `as_of` está em cada `knowledge.json`.
