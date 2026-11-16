# Política de reinício e unidades de sessão

Updated: 2026-10-31. Módulo de [`documentary-factory`](../SKILL.md).

## Unidades de sessão (não identidades)

Os seis papéis são **contratos de trabalho** executados como unidades de sessão com contexto
próprio. Existe uma identidade de agente: `codenavi-agent`. Nenhum papel cria persona, agente
filho ou agente pai. Cada unidade recebe: o contrato da sua skill, os artefatos de entrada e o
critério de aceitação. Cada unidade devolve: artefato + evidência + pendências explícitas.

O papel 6 (juiz) é instanciado em contexto **virgem**, sem herdar nada dos papéis 1–5.

## Quando reprovar exige reiniciar

Reprovação não é "refazer tudo por reflexo". A causa raiz determina a etapa de reinício:

| Causa raiz | Reinicia de |
| --- | --- |
| erro factual, certeza falsa, claim sem fonte | evidência → enredo (papel 5) |
| repetição, fragmento, cena subnarrada | enredo (papel 5) → voz → render |
| silêncio, mudez, legenda divergente, voz robótica | voz → render → mix |
| música inaudível, agitada, abafando, licença inválida | trilha (papel 1) → mix (papel 2) |
| asset fora do tema, marca d'água, orientação errada | assets (papel 3) → render |
| licença/atribuição ausente | papel da fonte (1 ou 3) → créditos → export |
| loudness fora do alvo, ducking ausente | mix (papel 2) |
| capítulo sem fechamento, arco quebrado | enredo (papel 5) → voz → render |

Reiniciar em etapa mais ampla que a causa raiz desperdiça trabalho válido. Reiniciar em etapa mais
estreita faz o defeito voltar. A causa raiz aponta a etapa — não o nervosismo.

## Papéis de produção são descartados

Ao reprovar, as unidades de sessão dos papéis 1–5 são **descartadas** (encerradas) e recriadas do
zero, sem carregar o contexto que produziu o defeito. O que se preserva é o **aprendizado sobre a
causa raiz** e os artefatos ainda válidos que a causa raiz não contamina.

O papel 6 nunca é descartado por reprovar: ele cumpriu o trabalho ao reprovar.

## Limite de tentativas

**Máximo 3 tentativas** de produção por missão. Contagem por pacote reprovado.

Na terceira reprovação, a fábrica **para e escala para o operador** com:
- as três notas por dimensão em cada tentativa (evolução ou estagnação);
- as causas raiz priorizadas que restaram;
- o que foi tentado e por que não resolveu;
- a decisão que o operador precisa tomar (mudar escopo, aceitar um limite, fornecer recurso ausente).

Girar indefinidamente não é rigor, é desperdício. O limite existe para transformar reprovação
repetida em decisão humana, não em loop.

## Falha fechada

Sem fonte, sem licença, sem motor ou sem evidência, a etapa dependente **bloqueia**. Nunca
substituir por quadro vazio, silêncio, clipe repetido, licença suposta ou nota arredondada.
