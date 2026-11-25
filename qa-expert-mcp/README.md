# qa-expert-mcp

Servidor MCP somente leitura. Não havia esta pasta no workspace nem um repositório com esse nome na conta `paulosantanna` em 2026-11-25. O conteúdo é o que foi lido nessa data, mais o contrato do operador.

`python server.py` fala JSON-RPC 2.0 no stdio, revisão `2025-11-25`. No CI o binário é `python`, o mesmo dos outros MCPs. Sem categoria, `plan_checks` devolve a lista e não escolhe. Categoria sem fonte não ganha check inventado. Não há pontuação JEV: a chave TypeSafe não estava configurada.

Não grave este comando num `mcp.json` daqui. O inventário é `quality/capabilities.json`.
