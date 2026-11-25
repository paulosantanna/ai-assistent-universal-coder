# Playbook fixall

Updated: 2026-11-25. Entry point: este arquivo. Owner: `codenavi-agent`. Herda `AGENTS.md` e CodENavi Full Workspace v2. O perfil de engenheiro staff é uma lente, não uma identidade nova.

Objetivo: levar uma mudança do pedido até done, com especificação, crítica, teste e, se o pedido chamar, revisão de segurança. Nenhuma etapa declara done com nota abaixo de 9/10. Dado que não está no repositório, no MCP ou numa página lida não entra. Dúvida para a etapa e pergunta.

## Escopo

Antes de editar, leia `07_mapeamentos`. Não altere arquivo que o pedido não relacione. O mapa não é licença para refatorar o catálogo inteiro.

## Lente staff

A lente usa a skill que já existe quando a mudança toca a linguagem:

| Pedido | Skill já no catálogo |
| --- | --- |
| Rust | `rust-expert` |
| Python | `python-expert` |
| Java 17, 21, 25, 26 | `java-17-expert`, `java-21-expert`, `java-25-expert`, `java-26-expert` |
| JavaScript | `javascript-expert` |
| Angular | `angular-20-expert` |
| React | `react-expert` |
| C# / .NET | `csharp-expert` |
| RAG | `rag-expert` |
| BM25 | `bm25-expert` |
| LoRA, QLoRA, DoRA | `lora-qlora-dora-expert` |
| Avaliação de LLM | `ai-evals-expert` |

Não há, neste catálogo, skill própria para Angular 22, TypeScript separado, C, C++, CUDA, kernel ou DLL. Não invente essa skill no meio da etapa. Pergunte.

Conhecimento fora de `qa-expert-mcp/knowledge.json` e `pentexpert-mcp/knowledge.json` só entra se `workspace-brain/src/jev.mjs` devolver `mode=jev` e `confidence` maior que 0,9. Sem chave TypeSafe, a leitura externa para e a etapa pergunta. Não baixe repositório. Ler pela API, quando o JEV passar, não é clone. Não declare pontuação que o JEV não devolveu.

## Etapas

Cada etapa grava um attempt em `.aeos/fixall/run.json` (gitignored). `the-fool` e `the-judge` leem a evidência da etapa, não o texto de intenção. Nota falta, evidência falta ou nota menor que 9 reinicia a etapa. Na terceira nota abaixo de 9, pare e pergunte. Não suba a nota para fechar.

1. `spec-driven` ou `spec-driven-lean`. Use lean quando o pedido já é um plano curto sem lista de tarefas. Use driven quando houver specify, design e tarefas. Não use os dois para produzir dois planos concorrentes. A saída é o plano e os checks observáveis, com caminho dos arquivos lidos.
2. Execute só o que o plano da etapa 1 nomeou.
3. `qa-expert` (`test-expert`). Sem categoria de teste, pare e pergunte. Funcional e ponta a ponta continuam no charter de `tests-expert`. Não invente um check que passe.
4. `pentests-expert`, somente se o pedido chamar pentest, segurança ofensiva ou o nome da skill. Sem autorização escrita, o resultado é o checklist. Payload, comando e reprodução são recusa.
5. `the-fool` e `the-judge` em toda etapa, inclusive QA e pentest. O juiz nativo continua APPROVE, COMMENT ou REQUEST_CHANGES; a nota 0–10 é o portão deste playbook e precisa citar o achado. Abaixo de 9, a etapa volta para o passo 1 dela.
6. Semgrep, antes de qualquer envio ao GitHub: `python quality/prepush/prepush.py --repo .`. O backend `sast` é o alinhado às regras do Semgrep. Não existe skill de id `semgrep` no catálogo; não crie uma para desviar deste comando. Achado ou fonte velha bloqueia o envio.

## GitHub

Subir é decisão do usuário, não deste playbook.

- Se o pedido já disse que não sobe, não pergunte de novo e não suba.
- Se o pedido não disse, pergunte. Sem resposta, não suba.
- Se o pedido já disse que sobe, só suba depois das notas, do prepush e da resposta registrada em `run.json`.

## Done

Done exige todas as etapas obrigatórias com as duas notas em 9 ou mais, evidência em disco, `invented` falso e `push_performed` coerente com a regra acima. O validador é `python playbooks/fixall/validate_fixall.py`. Ele reprova; não dá nota no lugar de the-fool e the-judge.

## Falha

Fonte fechada, JEV ausente para fato novo, categoria de teste não escolhida ou autorização de pentest ausente não são completados com suposição. A etapa fica aberta.
