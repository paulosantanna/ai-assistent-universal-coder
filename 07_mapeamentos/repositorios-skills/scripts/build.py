"""Generate an offline source-backed map without changing repositories."""
import collections
import csv
import hashlib
import html
import json
import re
import tomllib
from pathlib import Path
from profiles import PROFILES, GROUPS, TRANSVERSAL, CONDITIONAL
from inventory import ROOT, OUT

DATE = '2026-10-13'
DIMENSIONS = [('technology','Tecnologias e versões'),('architecture','Arquitetura'),
 ('purpose','Propósito'),('flow','Fluxo'),('data','Dados'),('deployment','Configuração/deploy'),
 ('operation','Operação/observabilidade'),('interfaces','Interfaces/dependências'),
 ('vulnerabilities','Vulnerabilidades'),('obsolescence','Obsolescência')]
STACKS = {
 'AIHealthResearch':'Python · FastAPI · SQLAlchemy · BM25/vetores · PEFT · AWS declarado',
 'dark-videos':'Python · FastAPI · Celery · PostgreSQL · Redis · Next.js/React',
 'dark-videos-mining-fix':'Python/FastAPI · SQLAlchemy · alterações TypeScript/React',
 'DiabeticsresearchJEV':'Python · FastAPI/GraphQL · MongoDB/Chroma · GraphRAG · QLoRA',
 'Engenharia-Reversa':'TypeScript/Node.js · MCP/CLI · bridges Python/Java/Swift/C++',
 'FreePDFReader':'Rust edição 2024 · egui/eframe · PDFium · ONNX Runtime',
 'ibunny':'Flutter/Dart · API Go 1.22 · PostgreSQL/runner em stub',
 'laya':'Python/FastAPI · SvelteKit/Svelte · Tauri/Rust · SQLite/FTS5/Chroma · n8n',
 'pdfcraft':'Rust edição 2024 · egui/eframe · engine PDF · CLI/MCP opt-in',
 'remove-onedrive':'PowerShell · operações Windows/OneDrive',
 'RemoveWindowsAI':'Windows PowerShell 5.1 · registro/Appx/TrustedInstaller',
}
evidence = {}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8', newline='\n')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_text(path):
    raw = path.read_bytes()
    encoding = 'utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig'
    try:
        text = raw.decode(encoding)
    except UnicodeDecodeError:
        encoding = 'cp1252'
        text = raw.decode(encoding)
    return raw, text, encoding


def cite(repo, rel, needle=None):
    path = ROOT / '02_repositorios' / repo / rel
    raw, text, encoding = read_text(path)
    lines = text.splitlines()
    line_no = next((i for i,line in enumerate(lines,1) if needle is None or needle in line), None)
    if line_no is None:
        raise ValueError(f'Evidence absent: {repo}/{rel} needle={needle!r}')
    key = f'{repo}/{rel}:{line_no}'
    snippet = lines[line_no-1].strip()
    if re.search(r'password|api[_-]?key|secret|cookie|\w+://[^\s/]*@|-----BEGIN.*PRIVATE', snippet, re.I):
        snippet = '[linha potencialmente sensível omitida; verificar fonte local]'
    evidence[key] = {'id': key, 'path': path.relative_to(ROOT).as_posix(), 'line': line_no,
                     'sha256': sha(raw), 'encoding': encoding, 'excerpt': snippet}
    return key


def versions(repo, inventory):
    result = []
    # All declared manifests in the inventoried tree; no inference of installed versions.
    for rel in inventory['manifests']:
        path = ROOT / '02_repositorios' / repo / rel
        raw, text, _ = read_text(path)
        name = path.name
        found = []
        if name == 'pyproject.toml':
            obj = tomllib.loads(text)
            proj = obj.get('project', {})
            found.extend((k,str(proj[k])) for k in ('name','version','requires-python') if k in proj)
            found.extend(('dependency',v) for v in proj.get('dependencies', []))
            for extra, deps in proj.get('optional-dependencies', {}).items():
                found.extend((f'extra:{extra}',v) for v in deps)
        elif name == 'package.json':
            obj = json.loads(text)
            found.extend((k,str(obj[k])) for k in ('name','version','packageManager') if k in obj)
            for field in ('engines','dependencies','devDependencies'):
                found.extend((k,str(v)) for k,v in obj.get(field, {}).items())
        elif name == 'Cargo.toml':
            obj = tomllib.loads(text)
            pkg = obj.get('workspace',{}).get('package', obj.get('package',{}))
            found.extend((k,str(pkg[k])) for k in ('name','version','edition','rust-version') if k in pkg and isinstance(pkg[k], (str,int)))
            deps = obj.get('workspace',{}).get('dependencies', obj.get('dependencies',{}))
            for k,v in deps.items():
                value = v if isinstance(v,str) else v.get('version')
                if value:
                    found.append((k,str(value)))
        elif name in {'go.mod','pubspec.yaml','requirements.txt','.nvmrc'}:
            found.extend(('declaration',line.strip()) for line in text.splitlines()
                         if (name=='go.mod' and line.startswith(('module ','go ')))
                         or (name=='pubspec.yaml' and re.match(r'^\s*(version|sdk|flutter|http|speech_to_text|audioplayers):',line))
                         or (name=='requirements.txt' and line and not line.startswith('#'))
                         or name=='.nvmrc')
        for label, value in found:
            literal = value if value in text else label
            ref = cite(repo,rel,literal)
            result.append({'label': label, 'value': value, 'provenance':'declared_manifest', 'evidence':ref})
    return result


def markdown_ref(ref, depth=0):
    e = evidence[ref]
    return f"[{e['path']}:{e['line']}]({'../'*(2+depth)}{e['path']})"


def build():
    inventory = json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
    cat_bytes = (ROOT/'00_skills/catalog.json').read_bytes()
    catalog = json.loads(cat_bytes)
    skills = catalog['skills']
    skills_by_id = {s['id']:s for s in skills}
    if len(skills_by_id) != len(skills):
        raise ValueError('Duplicate canonical skill')
    if {r['name'] for r in inventory} != set(PROFILES):
        raise ValueError('Intake changed: profiles must be reviewed')
    skill_evidence = []
    for s in skills:
        raw = (ROOT/s['path']).read_bytes()
        if sha(raw) != s['sha256']:
            raise ValueError('Catalog skill hash drift: '+s['id'])
        skill_evidence.append({'id':s['id'],'path':s['path'],'sha256':sha(raw),
                               'runtime_binding':s['runtime_binding'],'aliases':s.get('aliases',[])})
    repos, matrix = [], []
    for inv in inventory:
        name = inv['name']
        profile = PROFILES[name]
        dims = {}
        for key, title in DIMENSIONS:
            if key in {'technology','vulnerabilities','obsolescence'}:
                continue
            c = profile[key]
            dims[key] = {'title': title,'state':c['state'],'summary':c['summary'],
                         'evidence':[cite(name,*c['source'])]}
        ver = versions(name,inv)
        dims['technology'] = {'title':'Tecnologias e versões','state':'declarado',
            'summary':'Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior.',
            'evidence':sorted(set(v['evidence'] for v in ver))}
        for key,title in DIMENSIONS[-2:]:
            dims[key] = {'title':title,'state':'não verificado','evidence':[],
             'summary': 'Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs.' if key=='vulnerabilities' else 'Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual.'}
        ci_refs = [cite(name,p) for p in inv['ci']]
        quality = {'ci_files':inv['ci'],'test_candidate_files':inv['tests'],
                   'evidence':ci_refs, 'state':'presença estática; testes/CI não executados'}
        assignment = {}
        for group in profile['groups']:
            dimension, ids = GROUPS[group]
            refs = ci_refs if dimension=='quality' else dims[dimension]['evidence']
            for sid in ids:
                assignment[sid] = {'status':'direta','reason':f"Necessidade observada: {group}. Usar na tarefa correspondente, respeitando o contrato da skill.",'evidence':refs}
        for sid in profile.get('extra',[]):
            assignment[sid] = {'status':'direta','reason':'Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente.',
                              'evidence':dims['interfaces']['evidence']+dims['flow']['evidence']}
        for sid, reason in profile.get('conditional_extra',{}).items():
            assignment[sid] = {'status':'condicionada','reason':reason,'evidence':dims['purpose']['evidence']}
        for sid in TRANSVERSAL:
            assignment.setdefault(sid, {'status':'transversal','reason':'Apoio a recon, documentação, continuidade, qualidade ou mudança futura; não é especialista desta stack.', 'evidence':dims['purpose']['evidence']})
        for sid, reason in CONDITIONAL.items():
            assignment.setdefault(sid, {'status':'condicionada','reason':reason,'evidence':[]})
        if 'training' in profile['groups']:
            assignment['ai-continuous-training-maintainer'] = {'status':'condicionada','reason':'Contrato fixa E:/GitHub/aidiabetic-research/src/, diferente deste alvo. Confirmar escopo e pipeline antes de reutilizar.', 'evidence':dims['purpose']['evidence']}
        if name=='dark-videos':
            assignment['typesafe-ai']['evidence'] = [cite(name,'backend/app/modules/learning/jev/client.py','class TypeSafeJevClient')]
        missing = set(assignment)-set(skills_by_id)
        if missing:
            raise ValueError('Unknown canonical skills: '+str(missing))
        direct = sorted(sid for sid,a in assignment.items() if a['status']=='direta')
        counts = collections.Counter(a['status'] for a in assignment.values())
        counts['sem necessidade identificada'] = len(skills)-len(assignment)
        for s in skills:
            decision = assignment.get(s['id'], {'status':'sem necessidade identificada','reason':'Nenhuma necessidade específica identificada nesta amostra estática. Não significa incompatibilidade universal; reavaliar se a tarefa mudar.', 'evidence':[]})
            matrix.append({'repository':name,'skill':s['id'],'category':s['category'],'skill_path':s['path'],
                           'runtime_binding':s['runtime_binding'],**decision})
        repos.append({'name':name,'stack':STACKS[name],'kind':'Git próprio' if inv['own_git'] else 'pacote sem Git próprio',
                      'files_in_scope':len(inv['files']),'excluded_entries':len(inv['excluded']),
                      'inventory_errors':inv['errors'], 'dimensions':dims,'versions':ver,'quality':quality,
                      'direct_skills':direct,'decision_counts':dict(counts),'gaps':profile['gaps']})
    relations = [
        {'from':'dark-videos-mining-fix','to':'dark-videos','type':'pacote de correção','state':'documentado; não chamada runtime',
         'evidence':[cite('dark-videos-mining-fix','README.md','Aplicado em D:/Git/dark-videos')]},
        {'from':'dark-videos','to':'serviço externo LAYA','type':'cliente HTTP','state':'endpoint observado; disponibilidade não verificada',
         'evidence':[cite('dark-videos','backend/app/modules/learning/laya_jev_client.py','https://api.laya.ai/v1/decisions')]},
    ]
    data = {'schema_version':1,'updated':DATE,'owner':'codenavi-agent',
        'scope':'11 diretórios; análise estática seletiva de fontes próprias; sem executar projetos',
        'catalog_sha256':sha(cat_bytes),'catalog_skills':len(skills),
        'repositories':repos,'skills':skill_evidence,'matrix':matrix,'evidence':list(evidence.values()),
        'relations':relations,'non_edges':[
            'AIHealthResearch e DiabeticsresearchJEV compartilham domínio, mas integração entre eles não foi comprovada.',
            'FreePDFReader e pdfcraft compartilham domínio PDF/Rust, sem relação de consumo comprovada.',
            'Serviço LAYA do cliente dark-videos não foi identificado como o aplicativo local laya.'],
        'limits':['Fontes próprias amostradas; nenhum percentual de auditoria integral de código é alegado.',
            'Árvores excluídas não foram enumeradas internamente; contagem é de entradas/árvores, não arquivos nelas.',
            'Binários, datasets, credenciais, cookies, backups, caches e código de terceiros não foram analisados.',
            'CVE/EOL, runtime/MCP, contas externas e testes dos projetos não verificados.',
            'Skills não foram instaladas/copied/executadas nos projetos. Associações não autorizam operações futuras.',
            'Nenhum download, treino, publicação, commit/push ou utilitário de remoção foi executado.']}
    save(OUT/'mapa.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    for repo in repos:
        lines=[f"# {repo['name']} — mapa estático de skills",f"\nUpdated: {DATE}",
               '\nEntry point: ../README.md',f"\nTipo: {repo['kind']}. Arquivos no inventário delimitado: {repo['files_in_scope']}; entradas excluídas: {repo['excluded_entries']}.",
               '\n[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)', '\n## Dez dimensões\n',
               '| Dimensão | Estado | Observação | Evidência |','| --- | --- | --- | --- |']
        for key,title in DIMENSIONS:
            d=repo['dimensions'][key]
            refs='; '.join(markdown_ref(r,1) for r in d['evidence'][:3]) or 'Sem verificação nesta missão'
            if len(d['evidence'])>3:
                refs+='; demais fontes em mapa.json/declarações abaixo'
            lines.append(f"| {title} | {d['state']} | {d['summary']} | {refs} |")
        lines+=['\n## Declarações dos manifests\n','Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.\n',
                '| Declaração | Valor | Fonte |','| --- | --- | --- |']
        for v in repo['versions']:
            lines.append(f"| {v['label']} | {v['value'].replace('|','&#124;')} | {markdown_ref(v['evidence'],1)} |")
        lines+=['\n## Skills diretamente relacionadas\n','| Skill | Aplicação | Fonte |','| --- | --- | --- |']
        for row in matrix:
            if row['repository']==repo['name'] and row['status']=='direta':
                skill_link=f"[{row['skill']}](../../../{row['skill_path']})"
                lines.append(f"| {skill_link} | {row['reason']} | {'; '.join(markdown_ref(r,1) for r in row['evidence'])} |")
        lines+=['\n## Uso condicionado\n']
        lines+=['- **'+r['skill']+'**: '+r['reason'] for r in matrix if r['repository']==repo['name'] and r['status']=='condicionada']
        lines+=['\n## Testes/CI\n',f"{len(repo['quality']['test_candidate_files'])} arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. {len(repo['quality']['ci_files'])} workflows encontrados. Suites não executadas.\n"]
        lines += ['- '+markdown_ref(r,1) for r in repo['quality']['evidence']]
        lines+=['\n## Lacunas\n']+['- '+g for g in repo['gaps']]
        save(OUT/'repositorios'/f"{repo['name']}.md",'\n'.join(lines)+'\n')
    with (OUT/'matriz.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['repositorio','skill','categoria','aplicabilidade','motivo','skill_path','evidencias'])
        for r in matrix:
            writer.writerow([r['repository'],r['skill'],r['category'],r['status'],r['reason'],r['skill_path'],'; '.join(r['evidence'])])
    unused = [s['id'] for s in skills if not any(r['skill']==s['id'] and r['status'] in {'direta','transversal','condicionada'} for r in matrix)]
    counts=dict(collections.Counter(r['status'] for r in matrix))
    summary=[ '# Mapeamento dos repositórios com as skills do workspace',f'\nUpdated: {DATE}',
      '\nEntry point: [relatório HTML offline](relatorio.html). Fontes: [mapa estruturado](mapa.json), [matriz CSV](matriz.csv), [inventário delimitado](inventory.json), [verificação](verificacao.json).',
      f'\n**{len(repos)} projetos/diretórios · {len(skills)} skills canônicas · {len(matrix)} decisões de aplicabilidade.** Dez têm Git próprio; dark-videos-mining-fix é pacote de trabalho. Aliases e pointers .agents/.codex não foram contados como novas skills.',
      '\nGovernança: herda [AGENTS.md](../../AGENTS.md) e o ciclo BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF. Scope/inputs/outputs/riscos/gates: [SPEC](../../.specs/repository-skill-map/SPEC.md).',
      '\n## Como usar\n',
      '- Direta: stack, domínio ou interface fornecem motivo concreto para usar a skill em tarefa correspondente.',
      '- Transversal: apoio de documentação, continuidade, qualidade ou mudança futura; não especialista de linguagem.',
      '- Condicionada: falta alvo concreto, requisito, acesso ou autorização para tarefa futura.',
      '- Sem necessidade identificada: não selecionada nesta amostra; reavaliar quando houver novo objetivo.',
      '\nAssociações são recomendações locais de instruções. Não comprovam MCP/runtime instalado, segurança, produção ou testes aprovados. Nenhuma skill foi executada automaticamente nos projetos.',
      '\n## Mapa por projeto\n','| Projeto | Stack declarada/observada | Propósito | Skills diretas | Lacunas principais |','| --- | --- | --- | --- | --- |']
    for r in repos:
        summary.append(f"| [{r['name']}](repositorios/{r['name']}.md) | {r['stack']} | {r['dimensions']['purpose']['summary']} | {', '.join(r['direct_skills'])} | {' '.join(r['gaps'])} |")
    summary += ['\n## Relações\n']
    summary += [f"- {r['from']} → {r['to']}: {r['type']} ({r['state']}); {'; '.join(markdown_ref(e) for e in r['evidence'])}." for r in relations]
    summary += ['- '+n for n in data['non_edges']]
    summary += ['\n## Cobertura e lacunas do catálogo\n',f"Distribuição das {len(matrix)} decisões: {counts}.",
       '\nEspecialistas ausentes: Go, Flutter/Dart, PowerShell/Windows, Svelte/SvelteKit, n8n, C++/Swift. Skills genéricas ajudam análise e documentação, mas não estabelecem cobertura especialista destas APIs.',
       '\nNenhuma evidência obriga ativação de WordPress, KingHost, Angular, Rails, Shopify, outreach/GTM ou mídia de reuniões nesta missão.',
       f'\n{len(unused)} skills sem necessidade identificada em todos os projetos: '+', '.join(unused)+'.',
       '\n## Limites\n']+['- '+n for n in data['limits']]
    summary+=['\n## Atualização e verificação\n',
       'Após mudança das fontes/catálogo, revisar profiles.py, regenerar inventário e mapa e verificar. O build falha se o conjunto de projetos, skill/hash ou needle de evidência mudar.\n',
       '```powershell\npython -X utf8 07_mapeamentos/repositorios-skills/scripts/inventory.py\npython -X utf8 07_mapeamentos/repositorios-skills/scripts/build.py\npython -X utf8 07_mapeamentos/repositorios-skills/scripts/verify.py\npython -X utf8 07_mapeamentos/repositorios-skills/scripts/browser_check.py\n```',
       '\nO navegador requer Playwright e Chromium/Edge já instalados; nenhuma instalação é automática. A data identifica o snapshot desta missão; nova missão deve atualizar DATE após revisar evidências.',
       '\nMétodo: [fleet-mapping](../../00_skills/(mapping)/fleet-mapping/SKILL.md), [repo-scanner](../../00_skills/(mapping)/repo-scanner/SKILL.md) e [report-design](../../00_skills/(design)/report-design/SKILL.md). Sem fontes oficiais atuais de CVE/EOL, ambas dimensões permanecem não verificadas.']
    save(OUT/'README.md','\n'.join(summary)+'\n')
    template=(OUT/'scripts/report.template.html').read_text(encoding='utf-8')
    safe=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    save(OUT/'relatorio.html',template.replace('__MAP_DATA__',safe))
    save(OUT/'evidencias.json',json.dumps({'catalog_sha256':sha(cat_bytes),'sources':list(evidence.values()),'skills':skill_evidence},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'repositories':len(repos),'skills':len(skills),'decisions':len(matrix),'source_pointers':len(evidence),'status_counts':counts},ensure_ascii=False))


if __name__ == '__main__':
    build()
