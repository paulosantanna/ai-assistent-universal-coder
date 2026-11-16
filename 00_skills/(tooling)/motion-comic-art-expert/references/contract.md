# Contrato — motion-comic-art-expert

Updated: 2026-10-27. Entry point: [skill](../SKILL.md).

Aplicar os seis estágios do ciclo e consultar `.notebook/INDEX.md` e o quarteto do projeto antes de missão material. Checklist e evidências ficam em PROGRESS; fatos duráveis na MEMORY, transferência na HANDOFF e lições comprovadas na LEARNING. Não duplicar os quatro artefatos.

Padrão: [especificação](../../../../.specs/features/science-studio/SPEC.md). Execução: [playbook](../../../../science-studio/PLAYBOOK.md). Dados/limites: [contrato JSON e providers](../../../../science-studio/CONTRACT.md). Configuração de sessão: [SESSION](../../../../science-studio/SESSION.md).

## Decisões Staff e aceitação

- Extrair direção artística da referência quando realmente anexada; se ausente, registrar referência textual. Produzir bíblia com paleta, traço, luz, silhuetas, escala, lente/câmera e regras de continuidade.
- Planejar por cena: fundo com overscan, plano médio/assunto, primeiro plano e efeitos; pintar áreas ocultas antes do parallax para evitar buracos. Gerar PNG RGBA com alpha real ou vídeo adequado.
- Usar sementes e descritores consistentes, não prometer identidade perfeita de personagens. Separar/segmentar em workflow local ComfyUI verificado; não tratar prompt transparent background como alpha garantido.
- Manter ponto focal e ação dentro da região segura do formato; compor 9:16 e 16:9 como enquadramentos próprios. Não esticar arte horizontal na vertical.
- Criar prompts por fala: objeto, ação, ambiente, escala, iluminação e restrições científicas. Negative prompt exclui texto embutido, balões, pseudoequações e anatomia errada.
- Inspecionar alpha, bordas, coerência, overscan e licença dos modelos/assets. Registrar caminhos, hashes, prompt/seed/modelo/licença sem credenciais. Entregar camadas + visual por cena.

O aceite da etapa exige caminhos existentes, claims ligados a fontes realmente inspecionadas e inspeção do resultado. Quando houver helper, executar e guardar retorno com escopo verdadeiro. Uma chamada de ferramenta aceita não implica qualidade audiovisual aceita.

## Falhas e retomada

- Fonte inválida/contraditória: bloquear claim e reformular; não usar a autoconfiança do modelo como prova.
- Modelo/FFmpeg ausente: doctor e erro concreto; informar o que precisa ser configurado sem instalar silenciosamente.
- Render interrompido: conservar cache válido; repetir cena incompleta, montar e revisar novamente.
- Conteúdo modificado: invalidar aprovação por hash; não reutilizar recibo antigo.
- GPU/disco insuficiente: reduzir lote/resolução de preview com registro explícito; não prometer deadline ou tempo real.
- Rede/publicador indisponível: conservar entrega local; não marcar publicado nem tentar outra conta automaticamente.
