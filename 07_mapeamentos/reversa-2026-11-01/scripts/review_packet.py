import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
records = [json.loads(line) for line in (OUT / 'candidatos.jsonl').read_text(encoding='utf-8').splitlines()]
lines = ['# Revisão humana — candidatos Reversa', '',
         'Para cada item, confira pergunta, resposta e fonte. Marque aprovado, rejeitado ou correção e escreva seu nome; devolva as decisões aqui na conversa ou edite este arquivo. Não marque como aprovado automaticamente.',
         '', 'Os exemplos são rascunhos do mesmo repositório; sua aprovação não cria uma amostra independente nem resolve separação de famílias. Os hashes referem-se ao checkout registrado no manifesto.', '']
for item in records:
    src = item['source']
    link = '../../02_repositorios/reversa/' + src['path']
    lines += [f"## {item['id']}", '', f"**Pergunta:** {item['question']}", '', f"**Resposta proposta:** {item['answer_draft']}", '',
              f"**Fonte:** [{src['path']}]({link}), linha {src['line']}; SHA-256 `{src['sha256']}`.", '',
              '**Decisão:** pendente  ', '**Correção/observação:**  ', '**Revisor:**  ', '']
(OUT / 'REVISAO-HUMANA.md').write_text('\n'.join(lines), encoding='utf-8')
print(len(records), 'itens preparados; nenhum marcado aprovado')
