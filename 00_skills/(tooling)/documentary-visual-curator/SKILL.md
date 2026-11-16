---
name: documentary-visual-curator
description: "Source on-topic, watermark-free images and GIFs with verified licenses. Use for video visuals. Do NOT use to remove third-party watermarks (policy)."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Curadoria visual sem marca d'água, dentro do tema

Governança: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill de `codenavi-agent`; herda `AGENTS.md`. Lentes são internas; sem novas identidades de agente; sem burlar gates de segredo ou permissão.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar vídeo. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

Autoridade dupla: procedência/licença do asset e adequação temática. Nenhuma das duas se presume.

## Limite de política (não negociável)

Aquisição é feita em acervos que **já entregam o asset sem marca d'água** (CC0, domínio público,
CC BY). É proibido construir ou operar remoção de marca d'água sobre conteúdo de terceiros: isso
burla copyright e termos de uso. Detecção e **rejeição** de asset marcado são obrigatórias.
Remoção real só é admitida para asset **próprio ou licenciado**, com registro de licença e
autorização explícita do operador — e nunca para fazer passar conteúdo de terceiros.

## Procedimento

1. **Definir o que o tema exige ver**: listar os fenômenos concretos do roteiro que precisam de
   imagem. "Ciência genérica", placa de circuito estilizada e cientista posando não são o fenômeno.
2. **Buscar só em acervos com licença explícita**: Wikimedia Commons (melhor acervo de GIF
   científico animado: orbitais, efeito fotoelétrico, tubos de raios catódicos, spin,
   supercondutividade), NASA/ESA/Hubble/JWST, NIST, CERN, Pixabay, Pexels, Openverse, Internet
   Archive. Cada arquivo tem a sua licença: conferir a do arquivo, não a do site.
3. **Inspecionar o arquivo de fato — não a página.** Baixar e olhar. Usar `ffprobe`/`ffmpeg` para
   ler dimensões, contagem de quadros e duração, e extrair quadros representativos; abrir os quadros
   como imagem real e descrever o que se vê. Inspeção por suposição não conta.
4. **Rejeitar imediatamente** qualquer candidato com: logo, marca d'água, selo, URL ou handle
   sobreposto, moldura de site, botão de app, texto promocional, texto explicativo denso embutido,
   numeral falso gerado por IA, ou conteúdo de jogo/filme/série. Registrar o motivo.
5. **Exigir literalidade temática**: se não for possível afirmar o que o asset mostra em termos do
   fenômeno físico correto, rejeitar ou substituir. Ambiguidade não é aceitável em documentário.
6. **Registrar por asset**: `file`, `kind`, dimensões reais, `frame_count`, `duration_seconds`,
   `source_url`, `license_name`, `license_url`, `author`, texto de inspeção de marca d'água, texto
   de verificação temática, e `attribution_text` quando exigido.
7. **Entregar honestamente**: se o acervo não cobrir um fenômeno, declarar a lacuna. Lacuna
   declarada é corrigível com arte local gerada; lacuna escondida vira defeito no vídeo.

8. **Preservar animação sem repetir tomadas**: GIF/vídeo aprovado deve aparecer em movimento quando
   o material original permitir. Não repetir o mesmo arquivo/tomada em outro ponto do corte, fazer
   loop, nem usar crops do mesmo quadro como tomadas diferentes. Para material de origem em quadros,
   não reutilizar uma imagem-fonte; conferir hashes dos quadros selecionados, não só nomes. A duração
   normal de exibição de um still não conta como uma nova tomada. Se faltarem fontes únicas para a
   duração, bloquear e adquirir material novo.
9. **Preservar forma e resolução**: registrar largura, altura e aspecto originais de cada fonte.
   Nunca distorcer proporções. Por padrão, ajustar X e Y pela mesma razão e usar barras neutras para
   manter todo o conteúdo. Se a direção pedir explicitamente tela cheia sem fundo, preencher o canvas
   por escala uniforme e recorte central das bordas; registrar o recorte e a ampliação em cada fonte.
   Ampliação não cria detalhe novo e pode suavizar o material. Um MP4 mantém canvas constante.

## Contrato e verificação

Entrada: lista de fenômenos do roteiro, canvas/dimensões alvo, orçamento de direitos, rede.
Saída: `sourcing-ledger.json` (aceitos + rejeitados), arquivos em `candidates/`, relatório visual.
Verificação: cada aceito tem dimensões e quadros lidos por ferramenta, inspeção visual registrada,
licença conferida por URL, e justificativa temática; cada rejeitado tem motivo concreto.
Na entrega, manifesto prova que nenhuma tomada/asset se repete e informa qualquer quadro-fonte
reutilizado, o tamanho original e qualquer ampliação; deformação de aspecto é proibida.
Riscos: licença presumida, marca d'água não percebida, asset fora do tema, resolução insuficiente,
texto falso gerado por IA, expectativa de removar marca d'água de terceiros.
Bloquear a etapa visual quando a licença não for verificável. Nunca compensar com asset duvidoso.
Error handling: arquivo corrompido é rejeitado; acervo indisponível bloqueia a busca, não a licença.
Segredos são referências de runtime; nunca persistir cookies, tokens ou credenciais.
Não criar agentes, não publicar, não reivindicar autoria de asset de terceiros.

## Módulos por necessidade

- Ler [detecção e rejeição](references/watermark-detection.md) antes de aceitar qualquer asset; ele
  cobre a licença por arquivo e o limite de política sobre remoção.

## Regra editorial vigente para documentários

Se o briefing exigir apenas movimento, exclua fotos e quadros congelados. Cada asset deve conter sequência real de frames e ser exibido à velocidade nativa, sem loops ou repetição de tomadas. Se pessoas aparecerem, limite cada aparição a 3 segundos como regra editorial, sem tratar isso como safe harbor ou garantia contra reivindicações. Verifique licença, restrições e créditos por arquivo; prefira fontes próprias, domínio público confirmado ou licenças compatíveis. Não prometa imunidade a claims. Antes da liberação, encaminhe pacote e evidências ao documentary-adversarial-judge; revisão sequencial pelo mesmo agente não é independente.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
