# Contrato — ptbr-documentary-voice-expert

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Aplicar os seis estágios do ciclo e consultar `.notebook/INDEX.md` e o quarteto do projeto antes de missão material. Checklist e evidências ficam em PROGRESS; fatos duráveis na MEMORY, transferência na HANDOFF e lições comprovadas na LEARNING. Não duplicar os quatro artefatos.

Padrão: [especificação](../../../../.specs/features/science-studio/SPEC.md). Execução: [playbook](../../../../science-studio/PLAYBOOK.md). Dados/limites: [contrato JSON e providers](../../../../science-studio/CONTRACT.md). Configuração de sessão: [SESSION](../../../../science-studio/SESSION.md).

## Decisões Staff e aceitação

- Verificar motor/modelo local, licença, amostra real PT-BR e capacidade do hardware. Masculina/documental/profunda é um critério auditivo; não garantir por identificador de voz ou queda artificial de pitch.
- Preparar texto falável e glossário de siglas, unidades e nomes; SSML só se suportado de fato. Fracionar por cena com identidade vocal estável e pausas entre ideias.
- Usar adapter Piper se instalado/configurado ou outro provider argv autorizado. Não baixar dependências/pesos silenciosamente. Selecionar modelo e speaker pela amostra e licença, não inventar uma voz aprovada.
- Medir áudio com ffprobe e comparar à cena; adapter permite atempo 0.85–1.2, normalização e padding. Fora disso reescrever/retimar; nunca acelerar o documentário inteiro para encaixar.
- Aplicar loudness consistente e true peak com critério auditivo; meta editorial inicial -16 LUFS/-1.5 dBTP é configuração interna, não regra universal das plataformas. Para mix final crítico usar duas passagens e medir saída.
- Gerar SRT a partir do alinhamento quando disponível; fallback por palavras é estimado e deve ser revisado. Escutar pronúncia, pausas, sibilância, clipping e continuidade antes da aprovação voice.

O aceite da etapa exige caminhos existentes, claims ligados a fontes realmente inspecionadas e inspeção do resultado. Quando houver helper, executar e guardar retorno com escopo verdadeiro. Uma chamada de ferramenta aceita não implica qualidade audiovisual aceita.

## Falhas e retomada

- Fonte inválida/contraditória: bloquear claim e reformular; não usar a autoconfiança do modelo como prova.
- Modelo/FFmpeg ausente: doctor e erro concreto; informar o que precisa ser configurado sem instalar silenciosamente.
- Render interrompido: conservar cache válido; repetir cena incompleta, montar e revisar novamente.
- Conteúdo modificado: invalidar aprovação por hash; não reutilizar recibo antigo.
- GPU/disco insuficiente: reduzir lote/resolução de preview com registro explícito; não prometer deadline ou tempo real.
- Rede/publicador indisponível: conservar entrega local; não marcar publicado nem tentar outra conta automaticamente.
