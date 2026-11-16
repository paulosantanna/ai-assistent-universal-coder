# Fontes e proveniência

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Conteúdo original AEOS, CC-BY-4.0, solicitado pelo usuário; formato do workspace inspirado nas convenções TLC locais. Não é pacote oficial publicado pelo Tech Leads Club e não copia snapshot upstream. Requisitos: PT-BR, voz masculina documental profunda, HQ sem balões, camadas/parallax/VFX e revisão antes de publicação.

Referências técnicas oficiais inspecionadas em 2026-10-27:
- [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html): overlay, zoompan, gblur, fade, atempo e loudnorm. Conferir também `ffmpeg -h filter=...` da instalação efetiva; documentação web não prova build local.
- [ComfyUI routes](https://docs.comfy.org/development/comfyui-server/comms_routes): prompt, history e view; workflows/nós/pesos devem existir localmente.
- [Ollama chat](https://docs.ollama.com/api/chat): JSON, message.content e stream=false; escolha de modelo depende dos instalados.
- [Piper CLI](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md): modelo local, arquivo WAV e texto como argumentos; licença do motor difere da licença de cada voz.

Fontes científicas são específicas do tema e devem ser verificadas na execução, com acesso/data/trecho e limites. Nunca inferir verdade científica das referências técnicas acima. Especificações das redes devem ser revalidadas antes de publicar.
