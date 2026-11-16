# Contrato — science-video-review-expert

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Aplicar os seis estágios do ciclo e consultar `.notebook/INDEX.md` e o quarteto do projeto antes de missão material. Checklist e evidências ficam em PROGRESS; fatos duráveis na MEMORY, transferência na HANDOFF e lições comprovadas na LEARNING. Não duplicar os quatro artefatos.

Padrão: [especificação](../../../../.specs/features/science-studio/SPEC.md). Execução: [playbook](../../../../science-studio/PLAYBOOK.md). Dados/limites: [contrato JSON e providers](../../../../science-studio/CONTRACT.md). Configuração de sessão: [SESSION](../../../../science-studio/SESSION.md).

## Decisões Staff e aceitação

- Verificar preview real, projeto, fontes e licenças; identificar perfil e plataformas. Conferir especificações atuais oficiais quando publicar; perfis editoriais locais não representam garantia de aceitação.
- Revisar cinco dimensões: science (cada claim/fonte), visual (HQ, alpha/camadas, movimentos/VFX), voice (PT-BR/timbre/pronúncia), subtitles (texto/tempo/contraste/safe area), rights (arte/modelos/música/fontes).
- Checar duração, A/V streams, resolução, fps, codificação, corrupção, início/fim e sync. Inspecionar timeline completa na revisão final; amostra de frames não certifica documentário inteiro.
- Registrar falhas por cena e correção mínima; novo conteúdo/áudio/legenda/MP4 invalida aprovação anterior. Gerar review.html, evidence e hashes. Revisão sequencial pela mesma identidade é self-review, não revisão independente.
- O operador identifica reviewer e confirma os cinco checks após assistir; jamais inventar aprovação humana nem executar review em nome do usuário sem instrução. Gate técnico atesta integridade, não verdade científica automática.
- Exportar delivery local com MP4, SRT, projeto/fontes e approval/handoff. Publicação requer ação explícita separada e gates do publicador; não inserir automaticamente na fila ativa do Dark-videos.

O aceite da etapa exige caminhos existentes, claims ligados a fontes realmente inspecionadas e inspeção do resultado. Quando houver helper, executar e guardar retorno com escopo verdadeiro. Uma chamada de ferramenta aceita não implica qualidade audiovisual aceita.

## Falhas e retomada

- Fonte inválida/contraditória: bloquear claim e reformular; não usar a autoconfiança do modelo como prova.
- Modelo/FFmpeg ausente: doctor e erro concreto; informar o que precisa ser configurado sem instalar silenciosamente.
- Render interrompido: conservar cache válido; repetir cena incompleta, montar e revisar novamente.
- Conteúdo modificado: invalidar aprovação por hash; não reutilizar recibo antigo.
- GPU/disco insuficiente: reduzir lote/resolução de preview com registro explícito; não prometer deadline ou tempo real.
- Rede/publicador indisponível: conservar entrega local; não marcar publicado nem tentar outra conta automaticamente.
