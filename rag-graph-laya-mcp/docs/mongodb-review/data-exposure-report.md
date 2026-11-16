# Dados e proveniência
Updated: 2026-10-15. Owner: codenavi-agent.
Entry point: [revisão do fluxo](README.md). Evidência: [agregados](evidence.json).

## Tratamento aplicado

A leitura autorizada utilizou a instância local ligada ao diretório D:/MongoDB/data. Títulos, autores, URLs dos documentos, termos específicos, textos e valores de payload não foram exportados. O script publica contagens, tipos, status conhecidos, flags, comprimentos, integridade e hash agregado. Os arquivos WiredTiger não foram copiados nem abertos por outra instância.

Os agregados comparam contagens antes/depois; não demonstram isolamento transacional nem ausência de modificações de outros processos. O código da consulta contém apenas operações de leitura; não foi criado usuário, índice, coleção ou checkpoint no MongoDB. A consulta utilizou um cliente novo sobre localhost, sem credenciais persistidas nos artefatos.

## R5 — Alta: direitos de treino não verificados

O único documento observado tem proveniência, URL HTTP(S), `is_open_access=true` e `license=null`. Isso indica disponibilidade registrada e ausência de licença explícita no documento, sem estabelecer permissão de treino. `application/training/dataset.py:20` usa aceitação como filtro, sem gate separado para licença. `application/gates/evidence_gate.py:55` avalia sinais de qualidade/relevância; não valida direitos de treino.

Antes de gerar amostras, registrar a política aplicável ao documento/trecho, sua evidência e permissão por finalidade. Aceitação científica, acesso para leitura, indexação e treino são decisões distintas. Licença ausente fica `unverified`; não preencher uma licença por inferência a partir de acesso aberto. O MCP deve manter `training_allowed=false` até verificação, caso essa fonte seja integrada.

## Integridade e fronteiras

Hash SHA256 do chunk confere com a fórmula documento+texto. Referência pai, limites e correspondência normalizada conferem. Ausência de igualdades literais com o resumo é explicada pelo chunker: ele une título e frases com espaços enquanto mantém offsets do corpo original.

A base observada não demonstra exposição de dados pessoais ou conteúdo de pacientes; também não foi realizada análise completa de PII/PHI. Qualquer futura importação deve manter documentos em estado local ignorado, evitar logs com texto e preservar origem/versão/revogação. Evidência biomédica não deve ser misturada às fontes técnicas usadas nos experimentos anteriores do MCP.
