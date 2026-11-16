# Equivalente Azure: AIHealthResearch (e os demais componentes locais)

Status: mapeamento e modelo, não implantação. Modelo lido pelo MCP: `cloud-architecture/models/azure/aihealthresearch.target.model.json`. Mapeamento automático de cada componente local: `cloud-architecture/local-apis.json` (saída de `map_local_api`).

## 1. Mapeamento dos componentes locais

| Componente local (fonte) | Azure (região brazilsouth) | Restrições e fontes |
| --- | --- | --- |
| API FastAPI do AIHealthResearch (30+ rotas, SSE) | **Container Apps** com ingresso interno (VNet) | Escala a zero só por HTTP ou evento (não CPU/memória). SSE: validar ingresso e keepalive. |
| Governança transacional (Aurora no CFN) | **PostgreSQL Flexible Server** em VNet, acesso público negado | **HA com redundância de zona bloqueado para servidor novo em brazilsouth** (temporário). Usar HA na mesma zona. Backup de 35 dias. |
| Recuperação híbrida (OpenSearch no CFN) | **Azure AI Search** (BM25 + vetor, RRF) | Consulta híbrida em uma requisição. Preço não extraído neste snapshot. |
| Evidências imutáveis (S3 Object Lock no CFN) | **Blob com política WORM por tempo, bloqueada** + versionamento | Sem cobrança extra de capacidade. Política bloqueada não pode ser encurtada. Política por versão exige versionamento. |
| Inferência do modelo local (SageMaker no CFN) | **Azure ML online** agendado (carga com p95 de 15 s) | Cobra compute e rede; sem sobretaxa. **Escala a zero não documentada** no extrato. Batch escala a zero: a verificar. |
| Workers e fetchers agendados (Lambda + EventBridge no CFN) | **Container Apps Jobs** (agendados) | Visão geral oficial do Container Apps. |
| Sink OTLP local (porta 14318) | **Azure Monitor OpenTelemetry Distro para Java** + Application Insights | Recomendação oficial para Java. Custo de Log Analytics: US$ 4,60/GB de ingestão em brazilsouth. |
| Aplicativo desktop MyDigitalBuddy | Blob estático + Front Door (**a verificar**) | Sem backend. Assinatura: Artifact Signing **não elegível** para publicador brasileiro individual (verificado). |
| `rag-graph-laya-mcp` (FastAPI, SSE) | Container Apps | Backend do grafo (graphiti) não verificado. |
| `science-studio/integration/dark_api.py` (FastAPI, 5 rotas, jobs com subprocessos) | Container Apps com ingresso interno para a API; executor de vídeo em job batch (não mapeado) | Voz do Google é opcional e externa: fora do desenho até decisão. Roteiro e assets são locais (Ollama e ComfyUI). |
| `rag-graph-laya-mcp/model_server.py` (FastAPI, GPU, 5 rotas no formato OpenAI) | Azure ML online (premissa de p95 de 15 s) | Pesos vêm do Hugging Face no primeiro carregamento: empacotar com hash no cloud. |

## 2. Restrições de Brazil South (verificadas em 2026-11-14)

- HA com redundância de zona: **bloqueado temporariamente para novos servidores** (a tabela oficial marca com cifrão).
- Backup geo-redundante: **indisponível**. DR exige outra região (decisão pendente).
- Artifact Signing: recurso existe em brazilsouth, mas a validação pública não cobre indivíduos no Brasil.

Por isso o modelo alvo declara `ha: same-zone` e `backup_geo_redundant: false`, e a revisão mostra o risco de região como configuração (regra AZ-001 e AZ-002 passam porque o desenho não viola).

## 3. Preços verificados (brazilsouth, snapshot de 2026-11-14)

| Item | Preço de lista | Comparação |
| --- | --- | --- |
| Container Apps, consumo, vCPU ativa | US$ 0,000024 por segundo (cerca de US$ 0,0864/h) | Dedicado: US$ 0,057/h por vCPU, mais US$ 0,10/h de gestão |
| Container Apps, consumo, memória ativa | US$ 0,000003 por GiB-s (cerca de US$ 0,0108/h) | Dedicado: US$ 0,0050 por GiB-h |
| PostgreSQL General Purpose Ddsv5, 2 vCore | US$ 0,24/h | — |
| PostgreSQL Memory Optimized Eadsv5, 2 vCore (16 GB) | US$ 0,525/h | Aurora r6g.large (16 GB) em sa-east-1: US$ 0,537/h |
| PostgreSQL backup LRS | US$ 0,095/GB-mês | — |
| Blob hot LRS | US$ 0,0326/GB-mês (faixa mais alta da API) | S3 Standard sa-east-1: US$ 0,0405/GB-mês |
| Log Analytics, ingestão analítica | US$ 4,60/GB | CloudWatch Logs sa-east-1: US$ 0,90/GB |
| GPU NV36ads A10 v5 (36 vCPU) | US$ 6,40/h (eastus: US$ 3,20/h) | ml.g5.xlarge sa-east-1: US$ 2,394/h (4 vCPU). **Não equivalentes.** |
| Artifact Signing Basic | US$ 9,99/mês (até 5.000 assinaturas) | Página oficial |

Sem total Azure nesta rodada: a comparação completa exige a calculadora oficial e regras de cobrança ociosa (não verificadas), além de AI Search, Private Endpoint, Key Vault e Front Door (não extraídos).

## 4. Achados do modelo alvo (revisão do MCP)

- Status: **pass**, sem erro e sem achado.
- Os riscos de região ficam em `constraints` do mapeamento e no `unverified_costs` do modelo, para que não sumam.
- SSE no ingresso do Container Apps não foi testado com carga.

## 5. O que não fazer (armadilhas registradas)

- Assumir HA zonal ou backup geo-redundante em Brazil South (P-AZ-01, P-AZ-02).
- Assumir escala a zero de Container Apps por CPU ou memória (P-AZ-04).
- Assumir escala a zero do endpoint online do Azure ML (P-AZ-05).
- Usar Azure OpenAI como LLM, contra a regra do projeto (P-AZ-09).
- Usar Artifact Signing para publicador brasileiro individual (P-AZ-03).
