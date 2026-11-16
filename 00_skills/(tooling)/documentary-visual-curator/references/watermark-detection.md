# Detecção de marca d'água, licença por arquivo e limite de remoção

Updated: 2026-10-31. Módulo de [`documentary-visual-curator`](../SKILL.md).

## Por que a página não serve como prova

Página de acervo descreve, promete e às vezes mente. O arquivo baixado é a verdade. A inspeção
tem de ocorrer sobre os bytes que entram no vídeo.

## Procedimento de inspeção

1. Ler o arquivo com ferramenta real antes de qualquer julgamento:

```powershell
ffprobe -v error -show_entries stream=width,height,nb_frames,avg_frame_rate,duration -of json arquivo.gif
```

2. Extrair quadros representativos — o primeiro, um do meio e um do fim. GIF com sobreposição
   costuma revelar a marca em alguns quadros e não em outros:

```powershell
ffmpeg -i arquivo.gif -frames:v 1 quadro_inicial.png
ffmpeg -ss <meio> -i arquivo.gif -frames:v 1 quadro_meio.png
```

3. **Abrir os quadros como imagem de verdade e olhar.** Descrever o que se vê. Inspeção declarada
   sem observação real é fraude de evidência.

## Rejeitar imediatamente ao ver

- logo, marca d'água, selo, sinete, carimbo do acervo;
- URL, domínio, arroba, handle de rede social sobreposto;
- moldura de site, botão de app, barra de interface, cursor gravado;
- texto promocional ("subscribe", "download", nome de canal);
- texto explicativo denso embutido na imagem;
- numeral, rótulo ou legenda gerada por IA com aparência falsa;
- conteúdo de jogo, filme, série, ou captura de tela de mídia de terceiros;
- marca d'água parcial ou semi-transparente (é a mais comum e a mais fácil de passar).

Registrar em `rejected` com o motivo concreto e o quadro onde o defeito aparece.

## Licença por arquivo, não por site

Um acervo com política CC0 abriga arquivos CC BY e arquivos com restrição. Conferir a licença
**do arquivo**: `license_name`, `license_url`, `author`, e `attribution_required` com o texto exato
quando exigido. Sem URL de licença conferida para aquele arquivo, o asset é rejeitado.

## Limite de política sobre remoção

**Proibido** construir ou operar remoção de marca d'água sobre conteúdo de terceiros: burla
copyright e termos de uso, e é exatamente o motivo pelo qual o asset marcado deve ser **rejeitado**
em vez de "limpo".

**Permitido** remoção real apenas quando o asset é **próprio ou licenciado**, com:
- registro da licença que autoriza a modificação (`derivatives_allowed` verdadeiro);
- autorização explícita do operador registrada;
- antes/depois preservados como evidência;
- declaração no ledger de que houve remoção.

A ferramenta `assetguard` (Rust, em `D:\Git\dark-videos\tools\assetguard`) implementa a detecção
e a remoção com registro. A detecção é obrigatória para todo asset; a remoção exige licença própria.
