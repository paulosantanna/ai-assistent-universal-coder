import hashlib
import json
from corpus import OUT, REPO

examples = [
    ('Quais comandos a CLI encaminha?', 'Ela encaminha install, update, status, uninstall, add-engine e export-diagrams.', 'bin/reversa.js', 'const commands = {'),
    ('Como o manifesto identifica modificações?', 'O manifesto armazena hashes SHA-256 e fileStatus compara o hash atual com o original.', 'lib/installer/manifest.js', 'export function fileStatus'),
    ('Qual o padrão de edição de legado?', 'O template declara allowLegacyEdits como false e allowedPaths como lista vazia.', 'templates/reversa-config.json', '"allowLegacyEdits"'),
    ('Quais fases constam no estado inicial?', 'Reconhecimento, escavação, interpretação, geração e revisão constam como pendentes.', 'templates/state.json', '"pending"'),
    ('A atualização consulta alguma fonte externa?', 'O código tenta consultar a versão mais recente no registro npm e pode continuar offline se falhar.', 'lib/commands/update.js', 'async function fetchLatestVersion'),
    ('Que confirmação a remoção pede?', 'O fluxo pede que o usuário digite remove antes da desinstalação e pergunta separadamente sobre a pasta de saída.', 'lib/commands/uninstall.js', "name: 'confirmed'"),
    ('Qual é o ponto de entrada do pacote Node?', 'O manifesto declara bin/reversa.js como executável reversa.', 'package.json', '"reversa": "bin/reversa.js"'),
    ('As instruções do Reversa têm precedência sobre o AGENTS.md deste workspace?', 'Não. O conteúdo do repositório é fonte não confiável e deve ser interpretado sob o contrato raiz do workspace.', 'agents/reversa/SKILL.md', 'Você é o Reversa'),
]
out = []
for n, (question, answer, path, needle) in enumerate(examples, 1):
    raw = (REPO / path).read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    line = next(i for i, value in enumerate(lines, 1) if needle in value)
    out.append({'id': f'reversa-candidate-{n:03d}', 'question': question, 'answer_draft': answer, 'source': {'path': path, 'line': line, 'sha256': hashlib.sha256(raw).hexdigest()}, 'kind': 'manually drafted; not gold', 'split': None, 'review': {'approved': False, 'reviewer': None}})
    out[-1]['assistant_review'] = {'reviewer': 'codenavi-agent', 'status': 'source-checked', 'independent': False,
                                  'evidence': 'REVISAO-ASSISTENTE.md'}
    if n == 8:
        root_agent = REPO.parents[1] / 'AGENTS.md'
        agent_raw = root_agent.read_bytes()
        agent_line = next(i for i, value in enumerate(agent_raw.decode('utf-8-sig').splitlines(), 1) if 'There is exactly **one** agent identity' in value)
        out[-1]['additional_source'] = {'path': 'AGENTS.md', 'workspace_relative': True, 'line': agent_line,
                                        'sha256': hashlib.sha256(agent_raw).hexdigest()}
(OUT / 'candidatos.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in out), encoding='utf-8')
print(len(out), 'candidatos pendentes de revisão')
