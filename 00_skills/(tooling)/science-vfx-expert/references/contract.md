# Contrato — science-vfx-expert

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Aplicar os seis estágios do ciclo e consultar `.notebook/INDEX.md` e o quarteto do projeto antes de missão material. Checklist e evidências ficam em PROGRESS; fatos duráveis na MEMORY, transferência na HANDOFF e lições comprovadas na LEARNING. Não duplicar os quatro artefatos.

Padrão: [especificação](../../../../.specs/features/science-studio/SPEC.md). Execução: [playbook](../../../../science-studio/PLAYBOOK.md). Dados/limites: [contrato JSON e providers](../../../../science-studio/CONTRACT.md). Configuração de sessão: [SESSION](../../../../science-studio/SESSION.md).

## Decisões Staff e aceitação

- Classificar efeito como diagrama, ilustração artística ou simulação quantitativa. Se quantitativo, exigir equações, unidades, condições e validação numérica; composição artística recebe rótulo apropriado.
- Para lente gravitacional: planejar desvio da luz e imagens/arcos coerentes com geometria qualitativa; distorcer fundo por mapa radial ou clipe/shader previamente validado. FFmpeg lenscorrection modela lente óptica e não certifica relatividade.
- Para acreção: partículas em órbita/fluxo motivado, disco emissivo fora do horizonte e distribuição visual plausível; não mostrar brilho material saindo de dentro do horizonte sem explicar a ilustração.
- Separar emissivo, glow e partículas do objeto principal. Limitar exposição, número/tamanho/velocidade e flicker; glow complementa forma em vez de lavar contraste. Ruído aleatório não vira fenômeno científico.
- Entregar efeitos como camadas RGBA/clipes pré-renderizados compatíveis com timeline; compositor local suporta overlay/blur, não um solver científico nem geração procedural completa. Para distorções avançadas usar workflow/clipe real.
- Verificar frames e movimento em escala de cinza/áreas claras, não ofuscar legendas; revisar com fonte científica e registrar simplificações. Se ferramenta/modelo ausente, bloquear efeito dependente, conservar a timeline.

O aceite da etapa exige caminhos existentes, claims ligados a fontes realmente inspecionadas e inspeção do resultado. Quando houver helper, executar e guardar retorno com escopo verdadeiro. Uma chamada de ferramenta aceita não implica qualidade audiovisual aceita.

## Falhas e retomada

- Fonte inválida/contraditória: bloquear claim e reformular; não usar a autoconfiança do modelo como prova.
- Modelo/FFmpeg ausente: doctor e erro concreto; informar o que precisa ser configurado sem instalar silenciosamente.
- Render interrompido: conservar cache válido; repetir cena incompleta, montar e revisar novamente.
- Conteúdo modificado: invalidar aprovação por hash; não reutilizar recibo antigo.
- GPU/disco insuficiente: reduzir lote/resolução de preview com registro explícito; não prometer deadline ou tempo real.
- Rede/publicador indisponível: conservar entrega local; não marcar publicado nem tentar outra conta automaticamente.
