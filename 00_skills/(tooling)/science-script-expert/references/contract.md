# Contrato — science-script-expert

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Aplicar os seis estágios do ciclo e consultar `.notebook/INDEX.md` e o quarteto do projeto antes de missão material. Checklist e evidências ficam em PROGRESS; fatos duráveis na MEMORY, transferência na HANDOFF e lições comprovadas na LEARNING. Não duplicar os quatro artefatos.

Padrão: [especificação](../../../../.specs/features/science-studio/SPEC.md). Execução: [playbook](../../../../science-studio/PLAYBOOK.md). Dados/limites: [contrato JSON e providers](../../../../science-studio/CONTRACT.md). Configuração de sessão: [SESSION](../../../../science-studio/SESSION.md).

## Decisões Staff e aceitação

- Consumir fontes verificadas e definir pergunta central, promessa honesta, explicação visual e conclusão; abertura deve funcionar sem clickbait nem afirmação falsa.
- Para 60 s usar abertura curta, desenvolvimento e conclusão. Para 10 min construir progressão causal. Para 60/90 min criar capítulos e transições de assunto; outline global deve preceder geração em lotes.
- Criar cenas de 5–15 s inicialmente e até 60 s só quando motivado; narration, visual, duration, claims e transition obrigatórios. O visual mostra o fenômeno mencionado naquele intervalo.
- Planejar 110–145 palavras/minuto como estimativa editorial, medir o TTS de fato e reescrever para caber. Não declarar sincronização com base apenas na contagem de palavras.
- Em cena de buraco negro: distinguir horizonte, disco/nuvem e lente; câmera revela material em acreção enquanto a fala explica sua dinâmica. Não mostrar ingestão indiscriminada do Universo.
- Preservar pronúncias, unidades e transições contextualizadas; manter legendas discretas separadas da arte; sem balões. Validar somas de tempo e claims antes de pedir ativos.

O aceite da etapa exige caminhos existentes, claims ligados a fontes realmente inspecionadas e inspeção do resultado. Quando houver helper, executar e guardar retorno com escopo verdadeiro. Uma chamada de ferramenta aceita não implica qualidade audiovisual aceita.

## Falhas e retomada

- Fonte inválida/contraditória: bloquear claim e reformular; não usar a autoconfiança do modelo como prova.
- Modelo/FFmpeg ausente: doctor e erro concreto; informar o que precisa ser configurado sem instalar silenciosamente.
- Render interrompido: conservar cache válido; repetir cena incompleta, montar e revisar novamente.
- Conteúdo modificado: invalidar aprovação por hash; não reutilizar recibo antigo.
- GPU/disco insuficiente: reduzir lote/resolução de preview com registro explícito; não prometer deadline ou tempo real.
- Rede/publicador indisponível: conservar entrega local; não marcar publicado nem tentar outra conta automaticamente.
