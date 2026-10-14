# Ambiente local de atas

Updated: 2026-10-13
Entry point: ../SKILL.md. Fonte: IMG_2749–IMG_2755.

Helpers locais implementam os contratos descritos; os arquivos originais fotografados não foram fornecidos. Nenhum ambiente CPU/CUDA, modelo ou espelho Artifactory foi instalado nesta missão.
Extração: --ffmpeg explícito → ACTA_FFMPEG → PATH → imageio-ffmpeg instalado; sem executável, usa PyAV instalado. Requer decoder real, sem download automático. Produz WAV mono PCM16/16kHz e metadata/source hash. Exemplos de path Santander são históricos, não diretórios deste projeto.
Transcrição: usar vox-aurum e pesos locais verificados, com --srt. GPU somente quando autorizado e disponível. Diarização: NumPy, scikit-learn e Resemblyzer com pesos já locais; --engine mfcc é alternativa explícita com librosa, não fallback silencioso nem qualidade equivalente.
Não instalar CUDA, pacote ou modelo sem escopo/razão concreta. Verificar versões do ambiente real antes de setup. Não relaxar TLS nem criar stubs para encobrir imports ausentes.
O build usa apenas a biblioteca padrão Python. HTML é autocontido e permite selecionar vídeo por File API; MKV/codecs dependem do navegador. Falha de codec não implica falha da ata e deve ser relatada; conversão de cópia compatível é ação separada autorizada.
Fonte oficial do encoder: [Resemblyzer](https://github.com/resemble-ai/Resemblyzer). Similaridade não prova identidade; áudio sobreposto/comprimido pode impedir separação. Com pouquíssimas âncoras longas, bloqueie multi-speaker em vez de inventar locutores.
