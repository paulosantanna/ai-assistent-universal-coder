"""Verify delivered contracts, source freshness, coverage and regeneration."""
import collections
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from inventory import ROOT, OUT, inventory


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def links(text):
    for match in re.finditer(r'\[[^\]]*\]\(', text):
        start=match.end()
        level,end=1,start
        while end<len(text) and level:
            if text[end]=='(':
                level+=1
            elif text[end]==')':
                level-=1
            end+=1
        yield text[start:end-1]


def verify():
    errors, checks = [], []
    def check(value, label):
        checks.append({'check':label,'passed':bool(value)})
        if not value:
            errors.append(label)
    data=json.loads((OUT/'mapa.json').read_text(encoding='utf-8'))
    catalog=json.loads((ROOT/'00_skills/catalog.json').read_text(encoding='utf-8'))
    initial=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
    current=inventory()
    check(initial==current,'Inventário delimitado: mesmos arquivos/metadados e exclusões após geração')
    names={r['name'] for r in current}
    skill_ids={s['id'] for s in catalog['skills']}
    expected={(r,s) for r in names for s in skill_ids}
    actual=[(r['repository'],r['skill']) for r in data['matrix']]
    check(set(actual)==expected and len(actual)==len(expected),'Matriz cobre cada par projeto/skill exatamente uma vez')
    check(len(data['repositories'])==len(names)==11,'Todos os 11 diretórios têm mapa individual')
    check(data['catalog_skills']==len(skill_ids)==302,'302 skills canônicas; aliases não duplicados')
    check(sum(r['own_git'] for r in current)==10,'10 Git próprios e um pacote')
    check(data['catalog_sha256']==digest(ROOT/'00_skills/catalog.json'),'Hash do catálogo preservado')
    evidence={e['id']:e for e in data['evidence']}
    source_files={e['path']:e['sha256'] for e in data['evidence']}
    check(all(digest(ROOT/p)==h for p,h in source_files.items()),'Todos os arquivos citados preservados por SHA-256')
    check(all(digest(ROOT/s['path'])==s['sha256'] for s in data['skills']),'Todas as 302 skills preservadas por SHA-256')
    for e in evidence.values():
        raw=(ROOT/e['path']).read_bytes()
        lines=raw.decode(e['encoding']).splitlines()
        check(1<=e['line']<=len(lines),'Linha válida: '+e['id'])
        if not e['excerpt'].startswith('[linha potencialmente'):
            check(lines[e['line']-1].strip()==e['excerpt'],'Valor citado confere: '+e['id'])
    required={'technology','architecture','purpose','flow','data','deployment','operation','interfaces','vulnerabilities','obsolescence'}
    for repo in data['repositories']:
        check(set(repo['dimensions'])==required,'Dez dimensões: '+repo['name'])
        check((OUT/'repositorios'/f"{repo['name']}.md").is_file(),'Mapa individual: '+repo['name'])
        for dim in repo['dimensions'].values():
            check(all(ref in evidence for ref in dim['evidence']),'Referências válidas: '+repo['name']+'/'+dim['title'])
            if dim['state'] not in {'não verificado'}:
                check(bool(dim['evidence']) or dim['title']=='Tecnologias e versões','Claims observados exigem evidência: '+repo['name']+'/'+dim['title'])
    check(all(e in evidence for r in data['matrix'] for e in r['evidence']),'Associações só usam evidências existentes')
    check(all(r['evidence'] for r in data['matrix'] if r['status']=='direta'),'Associações diretas têm evidências')
    with (OUT/'matriz.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.reader(f))
    check(len(rows)==len(expected)+1 and all(len(row)==7 for row in rows),'CSV completo tem 3.322 decisões e sete colunas válidas')
    local_links=[]
    for md in [OUT/'README.md',*(OUT/'repositorios').glob('*.md')]:
        for target in links(md.read_text(encoding='utf-8')):
            if not target.startswith(('http:','https:','#')):
                resolved=md.parent/target.split('#')[0]
                if resolved.name=='verificacao.json':
                    continue
                local_links.append(resolved.exists())
    check(all(local_links),'Todos os links Markdown entregues resolvem localmente')
    html=(OUT/'relatorio.html').read_text(encoding='utf-8')
    check('src="http' not in html and 'href="https://fonts' not in html,'HTML sem assets remotos')
    check('sem necessidade identificada' in html and 'Exportar linhas filtradas (CSV)' in html,'HTML tem matriz completa e CSV explícito')
    # Regenerate twice from the same inputs; fixes must be made in the generator.
    artifact_paths=[OUT/'README.md',OUT/'mapa.json',OUT/'matriz.csv',OUT/'evidencias.json',OUT/'relatorio.html',*(OUT/'repositorios').glob('*.md')]
    before={p.name:digest(p) for p in artifact_paths}
    for n in range(2):
        run=subprocess.run([sys.executable,'-X','utf8',str(OUT/'scripts/build.py')],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        check(run.returncode==0,'Regeneração '+str(n+1)+' concluída')
        if run.returncode:
            errors.append(run.stderr)
        check({p.name:digest(p) for p in artifact_paths}==before,'Regeneração '+str(n+1)+' byte-idêntica')
    result={'schema_version':1,'updated':data['updated'],'status':'PASS' if not errors else 'FAIL',
            'repositories':len(names),'skills':len(skill_ids),'matrix_rows':len(actual),
            'source_pointers':len(evidence),'source_files_hashed':len(source_files),
            'inventory_files':sum(len(r['files']) for r in initial),
            'excluded_entries':sum(len(r['excluded']) for r in initial),
            'inventory_errors':sum(len(r['errors']) for r in initial),
            'status_counts':dict(collections.Counter(r['status'] for r in data['matrix'])),
            'checks':checks,'errors':errors,'artifact_sha256':before,
            'limits':['Preservação refere-se aos arquivos do inventário delimitado e hashes das fontes examinadas; árvores excluídas não auditadas.',
                      'Checks de projetos não executados; cobertura de skills é associação estática, não capacidade runtime.',
                      'CVEs, suporte/EOL e segurança de binários permanecem não verificados.']}
    (OUT/'verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in {'checks','artifact_sha256'}},ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__=='__main__':
    verify()
