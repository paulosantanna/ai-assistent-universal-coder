---
name: documentary-factory
description: "Runs the documentary factory: six gated roles and a reject-restart loop. Use for full documentary production. Do NOT use for one role or publishing."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Fábrica de documentários — super-skill de orquestração

Governança: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill de `codenavi-agent`; herda `AGENTS.md`. Lentes são internas; sem novas identidades de agente; sem burlar gates de segredo ou permissão.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar áudio/vídeo. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

Playbook canônico: [`science-studio/PLAYBOOK-FACTORY.md`](../../../science-studio/PLAYBOOK-FACTORY.md).

Existe **uma** identidade de agente: `codenavi-agent`. Os seis papéis são contratos de trabalho
(executados como unidades de sessão, cada uma com contexto próprio), **não** identidades de agente.
Especialização mora em skills, playbooks e lentes — nunca em personas novas.

## Os seis papéis

| # | Papel | Skill do contrato | Entrega |
| --- | --- | --- | --- |
| 1 | Aquisição de áudio sem copyright | `documentary-music-curator` | trilha com licença comprovada |
| 2 | Engenharia de áudio (música calma) | `documentary-audio-engineer` | mix -16 LUFS com ducking |
| 3 | Audiovisual sem marca d'água | `documentary-visual-curator` | assets no tema + ledger |
| 4 | Vídeo para internet | `documentary-social-video-expert` | pacote YouTube/IG/TikTok |
| 5 | Especialista do assunto | `documentary-subject-expert` | fontes + enredo + cenas |
| 6 | Juiz adversarial (The-Fool) | `documentary-adversarial-judge` | veredito com notas ≥ 9,5 |

O papel 6 **não herda contexto** de nenhum outro papel. Ele recebe artefato e evidência, e mais nada.

## Procedimento

1. **BRIEFING**: tema, domínio, duração, identidade e regras invioláveis do operador. Ler o
   `.notebook/` e o playbook da fábrica. Duração define perfil e canvas no contrato do projeto.
2. **RECON**: confirmar motores reais disponíveis (TTS local, geração de imagem, FFmpeg) e
   capacidade de disco/GPU. Nunca prometer motor que não foi verificado no ambiente.
3. **PLAN**: congelar arco de capítulos e orçamento de palavras ANTES de escrever cena. Longo prazo
   sem outline global produz colcha de retalhos. Semear o checklist e os gates.
4. **EXECUTE** nas etapas do playbook: evidência → enredo → assets → voz → render → mix → gates.
   Cada etapa falha fechada: sem fonte a cena bloqueia; sem licença o asset bloqueia; sem motor a
   etapa bloqueia. Conservar o trabalho válido das etapas anteriores.
5. **VERIFY**: rodar os gates determinísticos e depois submeter o pacote ao papel 6, com contexto
   virgem e evidência real. Gate técnico não substitui o julgamento adversarial.
6. **LOOP**: nota < 9,5 em qualquer dimensão → `REPROVADO`. Descartar os papéis de produção,
   registrar a causa raiz, recriar os papéis do zero e reiniciar a produção a partir da etapa que a
   causa raiz exige (roteiro reprovado não volta da mixagem). **Máximo 3 tentativas**; na terceira,
   escalar para o operador com as causas raiz, em vez de girar.
7. **DEBRIEF**: entrega local em `D:\Git\dark-videos`, quarteto atualizado, aprovação artística
   final do operador solicitada. Publicação é ação separada e só sob pedido explícito.

## Contrato e verificação

Entrada: tema/domínio, duração, regras do operador, capacidades reais do ambiente, fontes.
Saída: documentário renderizado + mixado + pacote de publicação + veredito do juiz + entrega local.
Verificação: todos os gates determinísticos passam; o papel 6 emite notas ≥ 9,5 com evidência;
as cinco dimensões de revisão do Science Studio e os direitos estão aprovados; hash de entrega
registrado; arquivo revisado é o arquivo exportado.
Riscos: repetir causas raiz já conhecidas, asset com marca d'água, trilha inaudível, cena
subnarrada, silêncio por flag errada, aprovar por nota estrutural, loop infinito de reprovação,
publicar sem pedido.
Bloquear a fábrica quando faltar evidência, licença, motor ou aprovação humana requerida.
Error handling: reprovação é insumo de causa raiz, não motivo de novo chute; motor ausente bloqueia
a etapa dependente em vez de substituir por silêncio, quadro vazio ou clipe repetido.
Cartelas textuais são somente placeholders identificados; não contam como visuais documentais. GIFs
com fonte/licença aprovadas devem ser codificados mantendo o movimento e o crédito. O manifesto de
render registra por cena: vídeo/GIF, imagem estática ou cartela provisória.
Quadros-fonte/tomadas não podem se repetir: deduplicar por hash de imagem renderizada, não apenas
por nome de arquivo. Preservar a proporção original; sem direção expressa para full-bleed, manter o
quadro inteiro com barras neutras. Se for exigido full-bleed sem fundo, usar escala uniforme e corte
central somente nas bordas; registrar corte/ampliação. Ampliação não cria detalhe e pode suavizar.
Segredos são referências de runtime; nunca persistir cookies, tokens ou credenciais.
Não criar agentes, não baixar gates para aprovar, não publicar automaticamente.

## Módulos por necessidade

- Ler o [playbook da fábrica](../../../science-studio/PLAYBOOK-FACTORY.md) antes de executar etapas.
- Ler [política de reinício](references/restart-policy.md) ao instanciar os seis papéis e ao aplicar
  reprovação e limite de tentativas.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
