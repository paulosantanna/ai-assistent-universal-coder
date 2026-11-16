---
name: motion-comic-art-expert
description: "Arte HQ científica em camadas. Use for storyboards ou bíblia visual. Do NOT use para chamar imagem única de animação ou inventar referência anexada."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# Arte em camadas e continuidade visual Staff

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar vídeo. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

## Procedimento

1. Extrair direção artística da referência quando realmente anexada; se ausente, registrar referência textual. Produzir bíblia com paleta, traço, luz, silhuetas, escala, lente/câmera e regras de continuidade.
2. Planejar por cena: fundo com overscan, plano médio/assunto, primeiro plano e efeitos; pintar áreas ocultas antes do parallax para evitar buracos. Gerar PNG RGBA com alpha real ou vídeo adequado.
3. Usar sementes e descritores consistentes, não prometer identidade perfeita de personagens. Separar/segmentar em workflow local ComfyUI verificado; não tratar prompt transparent background como alpha garantido.
4. Manter ponto focal e ação dentro da região segura do formato; compor 9:16 e 16:9 como enquadramentos próprios. Não esticar arte horizontal na vertical.
5. Criar prompts por fala: objeto, ação, ambiente, escala, iluminação e restrições científicas. Negative prompt exclui texto embutido, balões, pseudoequações e anatomia errada.
6. Inspecionar alpha, bordas, coerência, overscan e licença dos modelos/assets. Registrar caminhos, hashes, prompt/seed/modelo/licença sem credenciais. Entregar camadas + visual por cena.

## Contrato e verificação

Entrada: tema/etapa autorizada, projeto e evidências reais, capacidades locais e limites de direitos/custo.
Saída: artefato da etapa com caminhos e fontes, validação executada e pendências explícitas.
Riscos: erros científicos/visuais, voz inadequada, sincronização, recursos de GPU/disco e publicação prematura.
Bloquear somente a etapa que depende de fonte, modelo, permissão ou aprovação ausente. Conservar trabalho válido.
Error handling: fonte ausente bloqueia a cena; motor indisponível bloqueia geração; arquivo alterado exige novo render e revisão.
Segredos são referências de runtime; nunca copiar cookies, tokens ou credenciais para projeto/notebook/logs.
Não criar agentes, prometer geração instalada ou apresentar verificação estrutural como vídeo aprovado.

## Módulos por necessidade

- Ler [contrato operacional](references/contract.md) antes de executar a etapa ou escolher ferramentas.
- Ler [exemplos e falhas](references/examples.md) para invocação, decisão de escopo ou recuperação.
- Ler [fontes e proveniência](references/sources.md) antes de afirmar suporte técnico ou atualizar APIs.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
