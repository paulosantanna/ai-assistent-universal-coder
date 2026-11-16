"""Build reviewed maps from the local inventory and hash-addressed evidence."""
import csv
import importlib.util
import json
import re
import tomllib
from pathlib import Path
from profiles import EXTRA, OVERRIDES, LLM, UPDATES, c
from scan import ROOT, OUT, TARGET, digest, save

DATE = '2026-10-27'
DIMS = {'purpose': 'Propósito', 'architecture': 'Arquitetura', 'flow': 'Fluxo',
        'data': 'Dados', 'interfaces': 'Interfaces', 'deployment': 'Configuração/deploy',
        'operation': 'Operação', 'fine_tuning': 'Fine-tuning', 'rag': 'RAG',
        'post_training': 'Pós-treino', 'inference': 'Inferência'}
EVIDENCE = {}


def write(name, text):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + '\n', encoding='utf-8', newline='\n')


def cite(repo, path, needle):
    full = TARGET / repo / path
    raw = full.read_bytes()
    rows = raw.decode('utf-8-sig').splitlines()
    line = next((i for i, text in enumerate(rows, 1) if needle in text), None)
    if line is None:
        raise ValueError(f'Locator absent: {repo}/{path} {needle!r}')
    key = f'{repo}/{path}:{line}'
    EVIDENCE[key] = {'id': key, 'path': full.relative_to(ROOT).as_posix(),
                     'line': line, 'sha256': digest(raw)}
    return key


def ref(key, depth=0):
    e = EVIDENCE[key]
    return f"[{key}]({'../'*(2+depth)}{e['path']})"


def versions(repo, files):
    result = []
    for f in files:
        if not f['manifest']:
            continue
        path = f['path']
        text = (TARGET / repo / path).read_text(encoding='utf-8-sig')
        entries = []
        name = Path(path).name
        if name in {'pyproject.toml', 'Cargo.toml'}:
            obj = tomllib.loads(text)
            if name == 'pyproject.toml':
                proj = obj.get('project', {})
                entries += [(key, str(proj[key])) for key in ('name', 'version', 'requires-python') if key in proj]
                for dep in proj.get('dependencies', []):
                    # Record package/version declarations, never direct credentials/URLs.
                    if re.fullmatch(r'[\w.\-\[\],<>=!~* ;"\'()]+', dep):
                        entries.append(('dependency', dep))
                for group, deps in proj.get('optional-dependencies', {}).items():
                    for dep in deps:
                        if re.fullmatch(r'[\w.\-\[\],<>=!~* ;"\'()]+', dep):
                            entries.append(('extra:' + group, dep))
            else:
                pkg = obj.get('package', obj.get('workspace', {}).get('package', {}))
                entries += [(key, str(pkg[key])) for key in ('name', 'version', 'edition', 'rust-version') if key in pkg and isinstance(pkg[key], (str, int))]
        elif name == 'package.json':
            obj = json.loads(text)
            entries += [(key, str(obj[key])) for key in ('name', 'version', 'packageManager') if key in obj]
            for field in ('engines', 'dependencies', 'devDependencies'):
                entries += [(field + ':' + k, v) for k, v in obj.get(field, {}).items() if isinstance(v, str) and not re.search(r'https?:|git\+|@.*:', v)]
        elif name in {'requirements.txt', 'go.mod', 'pubspec.yaml'}:
            for line in text.splitlines():
                value = line.strip()
                if name == 'requirements.txt' and re.fullmatch(r'[\w.\-\[\],<>=!~* ;"\'()]+', value):
                    entries.append(('dependency', value))
                elif name == 'go.mod' and line.startswith(('module ', 'go ')):
                    entries.append(('runtime', value))
                elif name == 'pubspec.yaml' and re.match(r'^\s*(version|sdk|flutter):', line):
                    entries.append(('runtime', value))
        for label, value in entries:
            # TOML escaping can change a literal; the key remains a precise declaration locator.
            needle = value if value in text else label.split(':')[-1]
            result.append({'label': label, 'value': value, 'evidence': cite(repo, path, needle), 'state': 'declarado; não instalado/verificado'})
    return result


def build():
    snapshot = json.loads((OUT / 'inventory.json').read_text(encoding='utf-8'))
    old_root = ROOT / '07_mapeamentos/repositorios-skills'
    old_map = json.loads((old_root / 'mapa.json').read_text(encoding='utf-8'))
    old_profiles = {r['name']: r for r in old_map['repositories']}
    old_evidence = json.loads((old_root / 'evidencias.json').read_text(encoding='utf-8'))['sources']
    old_refs = {e['id']: e for e in old_evidence}
    old_inventory = {r['name']: r for r in json.loads((old_root / 'inventory.json').read_text(encoding='utf-8'))}
    beta2_path = ROOT / '07_mapeamentos/mapeamento-beta-2.0/matriz-conhecimento.csv'
    with beta2_path.open(encoding='utf-8-sig') as handle:
        beta2 = {r['repositorio']: r for r in csv.DictReader(handle)}
    # Import only the workspace-owned, historical mapping data, never a target module.
    spec = importlib.util.spec_from_file_location('historical_profiles', old_root / 'scripts/profiles.py')
    historical = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(historical)
    repos, retired = [], []
    assert {r['name'] for r in snapshot['repositories']} == set(UPDATES)
    for inv in snapshot['repositories']:
        name = inv['name']
        claims = {}
        if name in historical.PROFILES:
            for dim in DIMS:
                if dim in historical.PROFILES[name]:
                    claims[dim] = dict(historical.PROFILES[name][dim])
        claims.update(EXTRA.get(name, {}))
        claims.update(OVERRIDES.get(name, {}))
        claims.update(LLM.get(name, {}))
        dimensions = {}
        for dim, title in DIMS.items():
            if dim not in claims:
                dimensions[dim] = {'title': title, 'state': 'não demonstrado na amostra',
                    'summary': 'Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.', 'evidence': []}
                continue
            claim = claims[dim]
            try:
                key = cite(name, *claim['source'])
            except (OSError, ValueError) as err:
                if dim in EXTRA.get(name, {}) or dim in OVERRIDES.get(name, {}) or dim in LLM.get(name, {}):
                    raise
                retired.append({'repository': name, 'dimension': dim, 'source': claim['source'], 'reason': type(err).__name__})
                dimensions[dim] = {'title': title, 'state': 'evidência histórica invalidada',
                    'summary': 'Ponteiro anterior não resolve na fonte atual; afirmação antiga não promovida.', 'evidence': []}
                continue
            dimensions[dim] = {'title': title, 'summary': claim['summary'], 'state': claim['state'], 'evidence': [key]}
        assert all(dimensions[d]['evidence'] for d in ('purpose', 'architecture', 'flow')), name
        ver = versions(name, inv['files'])
        dimensions['technology'] = {'title': 'Tecnologias/versões', 'state': 'declarado',
            'summary': 'Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.',
            'evidence': sorted({v['evidence'] for v in ver})}
        for d, title in [('vulnerabilities', 'Vulnerabilidades'), ('obsolescence', 'Obsolescência')]:
            dimensions[d] = {'title': title, 'state': 'não verificado', 'summary': 'Sem consulta de CVE/EOL nesta missão.', 'evidence': []}
        older = old_inventory.get(name)
        current_files = {f['path']: f for f in inv['files']}
        past_files = {f['path']: f for f in older['files']} if older else {}
        historical_comparison = []
        for e in old_evidence:
            if not e['path'].startswith('02_repositorios/' + name + '/'):
                continue
            full = ROOT / e['path']
            rel = full.relative_to(TARGET / name).as_posix()
            current = current_files.get(rel)
            state = ('unchanged' if current['sha256'] == e['sha256'] else 'changed') if current else ('outside_current_scope' if full.exists() else 'missing')
            historical_comparison.append({'path': rel, 'state': state, 'old_sha256': e['sha256'], 'current_sha256': current['sha256'] if current else None})
        delta = {'in_beta2': name in beta2, 'beta2_row': beta2.get(name),
            'beta1_evidence_hash_comparison': historical_comparison,
            'added_paths_vs_beta1_inventory': sorted(set(current_files) - set(past_files)) if older else None,
            'missing_paths_vs_beta1_inventory': sorted(p for p in past_files if not (TARGET / name / p).exists()) if older else None,
            'scope_difference_paths': sorted(p for p in past_files if p not in current_files and (TARGET / name / p).exists()) if older else None,
            'summary': UPDATES[name],
            'limitation': 'Beta 2 sem snapshot completo de conteúdo: sem diff exato 2→3. Inventários beta 1 e 3 possuem filtros diferentes; caminho novo no inventário pode ser mudança de escopo.'}
        quality = {'ci_files': [f['path'] for f in inv['files'] if f['ci']],
                   'test_candidate_files': [f['path'] for f in inv['files'] if f['test_candidate']],
                   'state': 'presença estática; testes e CI dos alvos não executados'}
        repos.append({'name': name, 'git': inv['git'], 'source_fingerprint': inv['source_fingerprint'],
            'files_hashed': len(inv['files']), 'bytes_read': sum(f['bytes'] for f in inv['files']),
            'dimensions': dimensions, 'versions': ver, 'quality': quality, 'delta': delta,
            'limits': ['Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.',
                       'Nenhum runtime, treino, publicação ou sincronização remota executado.',
                       'Fontes modificadas/não rastreadas fazem parte deste snapshot local.']})

    model = {'schema_version': 1, 'mapping_version': '3.0.0-beta', 'updated': DATE,
        'captured_at': snapshot['captured_at'], 'owner': 'codenavi-agent',
        'scope': snapshot['scope'], 'repositories': repos,
        'retired_historical_locators': retired,
        'assumptions': ['beta 3.0.0 nomeia o mapeamento, não versões dos produtos.', 'Atualizações = estado local disponível; upstream remoto não consultado.'],
        'risks': [{'severity': 'medium', 'description': 'HEAD não representa mudanças locais; conferir hash/fingerprint antes de reutilizar.'},
                  {'severity': 'medium', 'description': 'Corpus de saúde exige direitos, validação científica e avaliação próprios.'},
                  {'severity': 'high', 'description': 'Utilitários Windows removem recursos/dados se executados; somente leitura nesta missão.'}],
        'recommendations': [{'owner': 'codenavi-agent', 'action': 'Consultar nota do alvo e revalidar hashes antes de nova mudança.', 'impact': 'Evita operar sobre conhecimento obsoleto.'}],
        'blocking_conditions': []}
    save('mapa.json', model)
    save('evidencias.json', {'sources': sorted(EVIDENCE.values(), key=lambda e: e['id']),
                            'policy': 'Somente caminho, linha e hash; nenhum trecho de código ou credencial copiado.'})
    save('diferencas.json', {r['name']: r['delta'] for r in repos})
    for r in repos:
        git_state = r['git']
        text = [f"# {r['name']} — beta 3.0.0", '', f'Updated: {DATE}',
            'Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)', '',
            f"Arquivos com hash: {r['files_hashed']}; fingerprint: `{r['source_fingerprint']}`.",
            f"Git próprio: {git_state['own_git']}; HEAD: `{git_state.get('head', 'não aplicável')}`; branch: `{git_state.get('branch', 'não aplicável')}`.",
            f"Estado local: {'há alterações/não rastreados' if git_state.get('status') else 'limpo' if git_state['own_git'] else 'pacote sem Git próprio'}; detalhes em inventory.json.", '',
            '## Atualizações e reconciliação', '', r['delta']['summary'], '',
            '## Dimensões e evidências', '']
        for dim in r['dimensions'].values():
            text += [f"### {dim['title']}", '', f"**{dim['state']}** — {dim['summary']}", '']
            text += [ref(k, 1) for k in dim['evidence'][:8]] + ['']
        text += ['## Declarações de versão', '', '| Manifest / declaração | Valor | Evidência |', '|---|---|---|']
        text += [f"| {v['label']} | {v['value'].replace('|', '&#124;')} | {ref(v['evidence'], 1)} |" for v in r['versions']]
        text += ['', '## Qualidade e limites', '', f"Workflows: {len(r['quality']['ci_files'])}; arquivos candidatos a testes: {len(r['quality']['test_candidate_files'])}. Não executados.", '']
        text += ['- ' + s for s in r['limits']]
        write(f"repositorios/{r['name']}.md", '\n'.join(text))
    with (OUT / 'matriz-conhecimento.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['repositorio', 'dimensao', 'estado', 'conhecimento', 'evidencias'])
        writer.writeheader()
        for r in repos:
            for key, dim in r['dimensions'].items():
                writer.writerow({'repositorio': r['name'], 'dimensao': key, 'estado': dim['state'], 'conhecimento': dim['summary'], 'evidencias': '; '.join(dim['evidence'])})
    new = sorted(set(UPDATES) - set(beta2))
    own = sum(r['git']['own_git'] for r in repos)
    dirty = sum(bool(r['git'].get('status')) for r in repos)
    readme = ['# Mapeamento beta 3.0.0 — 02_repositorios', '', f'Updated: {DATE}',
      'Entry point: este índice → nota por repositório → fonte local.', '',
      f"Cobertura: **{len(repos)} diretórios**, {own} com Git próprio e {len(repos)-own} pacote sem Git; **{sum(r['files_hashed'] for r in repos)} arquivos com SHA-256**. {dirty} árvores Git têm alterações locais/não rastreados.", '',
      f"Novo em relação à lista do beta 2.0: **{', '.join(new)}**. A versão 3.0.0 identifica o mapa; não altera versões dos projetos.", '',
      '## Repositórios', '', '| Alvo | Arquivos | Git/HEAD local | Atualização do conhecimento |', '|---|---:|---|---|']
    for r in repos:
        head = r['git'].get('head')
        head_label = head[:10] if isinstance(head, str) else 'HEAD não resolvido' if head else 'sem Git'
        readme.append(f"| [{r['name']}](repositorios/{r['name']}.md) | {r['files_hashed']} | {head_label} | {r['delta']['summary']} |")
    readme += ['', '## Artefatos', '',
      '- [Conhecimento consolidado e reutilização](CONHECIMENTO.md).',
      '- [Diferenças e limites da comparação](ATUALIZACOES.md), com detalhes em diferencas.json.',
      '- [Matriz por dimensão](matriz-conhecimento.csv) e mapa.json para consulta estruturada.',
      '- inventory.json: arquivos, exclusões, hashes, fingerprint e estado Git local.',
      '- evidencias.json: locadores de fatos e declarações, sem cópia de trechos.',
      '- verificacao.json: resultado dos gates executados; checksums.json: hashes dos artefatos.', '',
      '## Método, escopo e limites', '',
      'BRIEFING/RECON: continuidade, mapas anteriores e fontes locais. PLAN: cobrir cada diretório e revalidar evidências. EXECUTE: inventário limitado, revisão seletiva e geração de notas. VERIFY: cobertura, referências, hashes e preservação do estado Git. DEBRIEF: conhecimento e continuidade.', '',
      'Leitura autorizada por ferramentas do ambiente. Os skills históricos citam um Tool Router AEOS removido na reorganização (MEMORY: Runtime pointer reconciliation); sua instalação não é presumida. O pedido e o AGENTS.md autorizam fontes locais e persistência em 07_mapeamentos/.', '',
      'Hash/busca textual em todos os arquivos do inventário não significa revisão semântica de todas as linhas. As notas distinguem código presente, documentação, bibliografia, não demonstrado e não verificado. A presença de testes/workflows não indica aprovação.', '',
      'Escopo exclui credenciais por nome, links/junctions, árvores de dados/cache/dependências/runtime, binários e arquivos acima de 2 MB; ver lista efetiva em inventory.json e regras em scripts/scan.py. Conteúdo do corpus, pesos, sessões e serviços externos não foram inspecionados. Nenhum fetch, pull, script dos alvos, treino, deploy, publicação, commit ou push foi executado.', '',
      'A comparação beta 2→3 é de conhecimento e cobertura: o beta 2 não tem snapshot completo com hashes. A comparação de conteúdo verificável usa os hashes pontuais do beta 1 (2026-10-13); novos caminhos de inventário podem refletir filtros diferentes. Histórico Git por data não identifica o momento em que um checkout local foi atualizado.', '',
      '## Atualizar e verificar', '', 'Na raiz do workspace:', '', '```powershell',
      'python 07_mapeamentos/mapeamento-beta-3.0.0/scripts/scan.py',
      '# Revisar scripts/profiles.py contra as fontes antes de gerar novos fatos.',
      'python 07_mapeamentos/mapeamento-beta-3.0.0/scripts/build.py',
      'python 07_mapeamentos/mapeamento-beta-3.0.0/scripts/verify.py', '```', '',
      'A verificação é estática e sequencial pelo mesmo codenavi-agent; não é revisão independente. APIs, compatibilidade de bibliotecas, CVE/EOL e eficácia dos modelos não foram validadas. Os mapas beta 1, beta 2 e NCM permanecem como histórico.']
    write('README.md', '\n'.join(readme))
    updates = ['# Atualizações verificadas — beta 3.0.0', '', f'Updated: {DATE}', 'Entry point: [README](README.md).', '',
       'O beta 2 tinha 16 diretórios; agora são 17. Suas notas internas divergiam em alguns estados; este pacote prevalece como snapshot local de 27/10. Sem baseline completo não se atribui toda mudança ao período de 20→27/10.', '']
    for r in repos:
        counts = collections_count(r['delta']['beta1_evidence_hash_comparison'])
        updates += [f"## {r['name']}", '', r['delta']['summary'], '',
                    f"Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {counts}.", '']
    updates += ['## Limites históricos', '', 'Os caminhos adicionados/ausentes estão em diferencas.json. Fora de escopo não significa removido. O beta 2 é preservado sem reescrever a história; suas alegações de pipelines funcionais e de runtime não são usadas como prova atual.', '',
                'Git sem HEAD resolvido em FreePDFReader é registrado como limitação de proveniência. O pacote dark-videos-mining-fix não recebe o HEAD do repositório pai. Nenhuma referência remota local é tratada como prova do estado remoto atual.']
    write('ATUALIZACOES.md', '\n'.join(updates))
    print(json.dumps({'repositories': len(repos), 'evidence': len(EVIDENCE), 'retired_locators': retired}, ensure_ascii=True))


def collections_count(rows):
    from collections import Counter
    return dict(Counter(r['state'] for r in rows))


if __name__ == '__main__':
    build()
