# Mapeamento BETA e conhecimento local do workspace

Updated: 2026-10-13
Owner: codenavi-agent

## Objetivo e limites
Mapear todos os projetos presentes em `02_repositorios`, sem alterar seus arquivos, executar scripts de manutenção, iniciar aplicações ou publicar dados. Entregar inventário contabilizado, mapas por projeto, relações com evidência, busca/RAG local e preparação de fine-tuning. O usuário escolheu preparar pipeline local e selecionar modelo depois da avaliação; nenhum treino de LLM deve ser alegado nesta etapa.

## Premissas e riscos
- BETA significa cobertura estática rastreável; presença de código/documentação não comprova funcionamento em produção.
- Dependências, Git internals, binários, dados operacionais/pessoais, credenciais, backups e código de terceiros são inventariados por metadados e excluídos do corpus.
- Diretório sem Git próprio é pacote de trabalho, não um repositório Git herdado do pai.
- Skills são instruções/lentes da identidade única. O runtime AEOS removido não será recriado nem alegado; catálogo inteiro recebe decisão de aplicabilidade, sem executar skills sem relação com a missão.
- Não adicionar dependências silenciosamente. SQLite FTS5 e biblioteca padrão Python formam a baseline offline; LoRA tem pré-requisitos explícitos.
- Detecção de segredos é conservadora e não garante ausência de toda informação sensível. Corpus permanece local/ignorado pelo Git. Revisão humana de dados/licenças é obrigatória antes de treino/exportação.

## Entregas e aceitação
- [ ] Inventário de todos os arquivos enumeráveis, com motivo das exclusões, hashes de cada texto lido, erros e cobertura por projeto.
- [ ] Onze mapas BETA: propósito declarado, estrutura, stack/versionamento declarado, dependências, entrypoints, fluxos, contratos/dados, testes/CI, riscos, lacunas e fontes.
- [ ] Grafo de imports/referências com distinção de relação observada, menção e semelhança; nenhuma integração inventada.
- [ ] RAG extrativo local: BM25, filtro por projeto, citações linha/hash, abstenção e recusa de fonte alterada; nenhuma dependência de nuvem.
- [ ] Avaliação congelada de consultas reais por projeto, fontes esperadas, negativos, precisão/recall/MRR, isolamento e latência.
- [ ] Dataset candidato contextual com origem, deduplicação e divisão por grupos de conteúdo, sem sobreposição entre treino/validação/teste; candidatura não equivale a curadoria aprovada.
- [ ] Pipeline LoRA offline com dry-run, pré-requisitos/modelo/licença/avaliação/budget explícitos e manifesto de experimento; treino bloqueado até gates satisfeitos.
- [ ] Relatório navegável offline, instruções de atualização/consulta/treino e evidência de preservação das fontes.
- [ ] Continuidade atualizada e limitações declaradas.

## Documentação oficial consultada
- https://www.sqlite.org/fts5.html
- https://docs.python.org/3.14/library/sqlite3.html
- https://huggingface.co/docs/peft/en/quicktour
- https://huggingface.co/docs/transformers/en/trainer

## Verificação
Baseline de metadados/hashes antes das escritas. Verificar contratos da ferramenta com fixtures temporárias e corpus real. Não executar suites dos 11 projetos: suas aplicações permanecem inalteradas. Verificar corpus, cobertura, filtros, redaction, fontes obsoletas, splits e artefatos. Treino/inferência neural não será marcado como validado sem runtime/modelo selecionados.
