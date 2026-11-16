import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[1]
snapshot = json.loads((OUT / 'inventory.json').read_text(encoding='utf-8'))
old = json.loads((ROOT / '07_mapeamentos/mapeamento-beta-3.0.0/mapa.json').read_text(encoding='utf-8'))
previous = {r['name']: r for r in old['repositories']}
notes = OUT / 'repositorios'
notes.mkdir(exist_ok=True)
rows = []
for repo in snapshot['repositories']:
    name = repo['name']
    files = repo['files']
    prior = previous.get(name)
    unchanged = bool(prior and prior['source_fingerprint'] == repo['source_fingerprint'])
    git = repo['git']
    head = git.get('head', 'sem Git próprio')
    status = git.get('status', '')
    dirty = 'não aplicável' if not git['own_git'] else ('não verificado' if isinstance(status, dict) else ('com alterações' if status else 'limpo'))
    signals = Counter(k for f in files for k in f['signals'])
    manifests = [f['path'] for f in files if f['manifest'] or f['lockfile']]
    ci = [f['path'] for f in files if f['ci']]
    tests = [f['path'] for f in files if f['test_candidate']]
    top = Counter(f['path'].split('/')[0] for f in files if '/' in f['path'])
    p = [f'# {name}', '', 'Updated: 2026-11-01', f'Entry point: [diretório](../../../02_repositorios/{name}/).', '',
         f'- Arquivos inventariados: {len(files)}; exclusões: {len(repo["excluded"])}; erros: {len(repo["errors"])}.',
         f'- Git HEAD: `{head}`; estado: {dirty}. Fingerprint: `{repo["source_fingerprint"]}`.',
         '- Diretórios por quantidade de arquivos: ' + (', '.join(f'{k} ({v})' for k,v in top.most_common(20)) or 'nenhum.'),
         '- Manifests e lockfiles: ' + (', '.join(f'`{v}`' for v in manifests) or 'nenhum no escopo.'),
         f'- Candidatos a teste: {len(tests)}; workflows: {len(ci)}. Presença não prova execução.',
         '- Sinais textuais por quantidade de arquivos: ' + (', '.join(f'{k}: {v}' for k,v in signals.items()) or 'nenhum.')]
    if prior:
        p += ['', '## Análise anterior', '', f'[Nota beta 3.0.0](../../mapeamento-beta-3.0.0/repositorios/{name}.md). Fingerprint da fonte: {"igual ao snapshot anterior" if unchanged else "alterado; conclusões anteriores exigem revalidação"}.']
    else:
        p += ['', '## Arquitetura e fluxo', '', 'O README descreve uma ferramenta para transformar software legado em especificações. O package.json declara versão 1.3.6, Node >=18.20.2 e CLI `bin/reversa.js`. A CLI despacha para módulos em `lib/commands`: install, update, status, uninstall, add-engine e export-diagrams. O README descreve instalação de instruções e criação de estruturas no projeto analisado; isso deve ser reconciliado com a regra de agente único deste workspace antes de qualquer uso.', '', 'Dependências declaradas: chalk, inquirer, ora e semver. O script verify declara verificações Python e Node; sua presença não comprova aprovação. Não foram executados instalador, testes nem código do projeto.', '', f'[README](../../../02_repositorios/{name}/README.md) · [manifest](../../../02_repositorios/{name}/package.json) · [CLI](../../../02_repositorios/{name}/bin/reversa.js).']
    p += ['', 'Detalhes de arquivos, hashes, exclusões, indicadores e erros: [inventory.json](../inventory.json).', '']
    (notes / (name + '.md')).write_text('\n'.join(p), encoding='utf-8')
    rows.append((name, len(files), dirty, unchanged, len(repo['errors'])))
lines = ['# Mapeamento local — 02_repositorios', '', 'Updated: 2026-11-01', 'Entry point: esta página → nota individual → fontes locais.', '', f'Escopo: {len(rows)} diretórios imediatos; {sum(r[1] for r in rows)} arquivos inventariados. Snapshot estático local, sem executar código dos projetos ou consultar remotos.', '', '| Diretório | Arquivos | Git | Fingerprint igual ao beta 3 | Erros |', '|---|---:|---|---|---:|']
lines += [f'| [{n}](repositorios/{n}.md) | {count} | {dirty} | {"sim" if same else "não ou sem baseline"} | {err} |' for n,count,dirty,same,err in rows]
lines += ['', '## Relações e limites', '', 'O mapa anterior reúne análise das capacidades e possíveis relações entre projetos: [conhecimento consolidado](../mapeamento-beta-3.0.0/CONHECIMENTO.md). Relações históricas em diretórios com fingerprint alterado precisam ser revalidadas; nomes semelhantes não comprovam dependência.', '', 'O inventário registra caminhos, hashes, indicadores textuais, exclusões e estado Git em [inventory.json](inventory.json). A busca de indicadores não comprova comportamento. Foram excluídos credenciais por nome, links, dados, caches, dependências instaladas, binários e arquivos acima de 2 MB; confira as regras em [scan.py](scripts/scan.py). Não houve testes, execução, auditoria de segurança ou verificação de serviços externos.', '']
(OUT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
print('Relatório:', len(rows), 'diretórios;', sum(r[1] for r in rows), 'arquivos; erros:', sum(r[4] for r in rows))
