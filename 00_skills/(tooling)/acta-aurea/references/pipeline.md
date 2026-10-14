# Pipeline e contrato call.json

Updated: 2026-10-13
Entry point: ../SKILL.md. Fonte: IMG_2751–IMG_2754.

INTAKE → EXTRACT → TRANSCRIBE → DIARIZE → NOMES → TÓPICOS → OFF-TOPIC → ATA/RESUMO → BUILD → PRESENT. Fonte autorizada é leitura; outputs privados ficam no destino autorizado, nunca no Git/notebook. Resolver paths/interpreter/model local antes de processar.

```json
{
  "media": {"filename": "reuniao.mp4", "duration": 120, "sha256": "SOURCE_HASH"},
  "speakers": {"S1": {"name": "S1", "confirmed": false}},
  "segments": [{"start": 0, "end": 4, "speaker": "S1", "text": "Texto reconhecido.", "offtopic": false}],
  "topics": [{"title": "Abertura", "start": 0}],
  "meeting": {"participants": [], "resumo_md": "", "ata_md": "", "acoes": [], "glossario": []}
}
```

Nomes: sugerir só de evidência explícita e pedir confirmação; sem confirmed:true, o build usa o rótulo anônimo. Ações: tarefa/responsavel/prazo; glossário: sigla/expansao/nota. Não inventar participantes, decisão, prazo ou expansão de sigla.
Tópicos: start do primeiro segmento, títulos em PT-BR e timestamps crescentes. Off-topic: listar candidatos com timestamp/trecho e marcar true somente após escolha explícita; omitir do transcript/subtitles/documentos. O player liga ao vídeo ORIGINAL, que ainda contém tais trechos, e informa esta limitação; remoção do vídeo exigiria edição própria.
Diarização: âncoras contíguas >=4s, frames com energia de voz, embeddings normalizados, agrupamento e associação ao centroide. Energia VAD e âncoras contíguas podem misturar locutores; inspeção humana é obrigatória. Silhueta abaixo de .15/distribuição dominada sugere baixa separação; acima de .25 é indício, nunca prova de identidade/qualidade. Inspecionar trechos conhecidos de mesma/diferente pessoa e falas sobrepostas. --num-speakers pode melhorar a estimativa, mas não corrige áudio sem sinal de separação.
Build exige duração positiva, segmentos ordenados dentro do vídeo, speakers existentes, tópicos crescentes e offtopic booleano; não inclui texto removido. Produz os sete outputs, preserva conteúdo literal, escapa HTML e mantém os campos Markdown em painel de texto seguro. Rebuild do mesmo JSON é byte-determinístico.
Comandos usam o intérprete aprovado e caminhos entre aspas: scripts/extract_audio.py --video SOURCE --out WAV --meta-out META; vox-aurum/scripts/transcribe.py --audio WAV --model-dir MODELS --out-dir CACHE --srt; scripts/diarize.py --wav WAV --srt SRT --meta META --out CALL; scripts/build_deliverables.py --call CALL --out-dir OUTPUT.
Verificar documento e navegação real no navegador; seleção local, tópicos e nomes incertos são comportamentos de produto. Checagem estrutural não prova que a transcrição ou separação de locutores de uma gravação real é correta.
