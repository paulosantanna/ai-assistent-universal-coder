# Contrato — motion-comic-animation-expert

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Aplicar os seis estágios do ciclo e consultar `.notebook/INDEX.md` e o quarteto do projeto antes de missão material. Checklist e evidências ficam em PROGRESS; fatos duráveis na MEMORY, transferência na HANDOFF e lições comprovadas na LEARNING. Não duplicar os quatro artefatos.

Padrão: [especificação](../../../../.specs/features/science-studio/SPEC.md). Execução: [playbook](../../../../science-studio/PLAYBOOK.md). Dados/limites: [contrato JSON e providers](../../../../science-studio/CONTRACT.md). Configuração de sessão: [SESSION](../../../../science-studio/SESSION.md).

## Decisões Staff e aceitação

- Consumir scene manifest e áudio medido; confirmar fps/resolução/aspecto e arquivos locais. Criar hierarquia conceitual de câmera e offsets por profundidade; manter movimentos de elementos independentes.
- Definir keyframes com unidades e limites, easing na implementação quando suportado, overscan e pontos focais. Evitar velocidade excessiva, deriva de borda e clipping; usar menor movimento no fundo e maior no primeiro plano.
- Usar studio.py para offsets lineares, zoom centrado por camada, blur e cut/fade. Movimentos avançados/rotação/easing/oclusão exigem clipe pré-renderizado ou extensão verificada: não inventar suporte.
- Aceitar clipes IA como kind=video sem loop silencioso; validar duração, continuidade temporal, anatomia e coerência científica antes de inserir. Não sobrescrever takes bons numa retomada.
- Renderizar cenas individualmente com cache por conteúdo/ativos/parâmetros/versão FFmpeg; montar concat com timestamps e codecs uniformes. Longos usam capítulos e checkpoints, sem carregar todos os frames em RAM.
- Verificar frames no começo/meio/fim, independência das camadas, A/V e duração real via ffprobe; relato distingue fixture de qualidade cinematográfica avaliada por humano.

O aceite da etapa exige caminhos existentes, claims ligados a fontes realmente inspecionadas e inspeção do resultado. Quando houver helper, executar e guardar retorno com escopo verdadeiro. Uma chamada de ferramenta aceita não implica qualidade audiovisual aceita.

## Falhas e retomada

- Fonte inválida/contraditória: bloquear claim e reformular; não usar a autoconfiança do modelo como prova.
- Modelo/FFmpeg ausente: doctor e erro concreto; informar o que precisa ser configurado sem instalar silenciosamente.
- Render interrompido: conservar cache válido; repetir cena incompleta, montar e revisar novamente.
- Conteúdo modificado: invalidar aprovação por hash; não reutilizar recibo antigo.
- GPU/disco insuficiente: reduzir lote/resolução de preview com registro explícito; não prometer deadline ou tempo real.
- Rede/publicador indisponível: conservar entrega local; não marcar publicado nem tentar outra conta automaticamente.
