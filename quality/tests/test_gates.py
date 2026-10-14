import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import canonical, package_hash, safe_path, sha, write_json
from protocol import environment, probe
from publish import allowed
from upstream import import_skill, missing_skills, update, verify_controls
from validate import capabilities, distribution, executable_resources, reviews, schema_valid, security_and_syntax, tools_valid, workflows


TOOL={'name':'demo.status','description':'Return fixture status','inputSchema':{'type':'object','properties':{},'additionalProperties':False}}


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def skill(self):
        description='Use when "request one", "request two", "request three". Do NOT use for unrelated work.'
        path=self.root/'00_skills/(development)/example/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('skill content',encoding='utf-8')
        native=self.root/'.agents/skills/example/SKILL.md'
        native.parent.mkdir(parents=True)
        native.write_text('pointer',encoding='utf-8')
        (self.root/'00_skills/skills.registry.yaml').write_text('skills:\n- id: example\n  path: 00_skills/(development)/example/SKILL.md\n  mission: '+json.dumps(description)+'\n',encoding='utf-8')
        return {'skills':[{'id':'example','aliases':[],'category':'development','path':'00_skills/(development)/example/SKILL.md',
                           'description':description}]}

    def test_text_hash_is_cross_platform(self):
        self.assertEqual(sha(b'one\r\ntwo\r\n'),sha(b'one\ntwo\n'))

    def test_binary_hash_is_byte_exact(self):
        self.assertNotEqual(sha(b'\0\r\n'),sha(b'\0\n'))

    def test_source_executable_modes_are_preserved(self):
        package=self.root/'00_skills/(development)/example'
        path=package/'references/tlc/scripts/helper'; path.parent.mkdir(parents=True)
        path.write_text('#!/bin/sh\nexit 0\n')
        write_json(self.root/'00_skills/upstream.manifest.json',{'skills':[{'installed_path':'00_skills/(development)/example',
                   'files':[{'installed':'references/tlc/scripts/helper','executable':True}]}]})
        subprocess.run(['git','init',str(self.root)],check=True,capture_output=True)
        subprocess.run(['git','add','.'],cwd=self.root,check=True,capture_output=True)
        path.chmod(0o644)
        self.assertEqual(executable_resources(self.root)[0]['code'],'source-helper-not-executable')
        path.chmod(0o755)
        subprocess.run(['git','update-index','--chmod=+x','--',path.relative_to(self.root).as_posix()],cwd=self.root,check=True,capture_output=True)
        self.assertEqual(executable_resources(self.root),[])

    def test_resource_escape_rejected(self):
        for path in ['../secret','/etc/passwd','C:/secret','a\\b','a/../../b']:
            with self.subTest(path=path),self.assertRaises(ValueError):
                safe_path(self.root,path)

    def test_valid_distribution(self):
        self.assertEqual(distribution(self.root,self.skill()),[])

    def test_new_unregistered_skill_rejected(self):
        catalog=self.skill()
        path=self.root/'00_skills/(development)/orphan/SKILL.md'
        path.parent.mkdir(); path.write_text('unknown')
        self.assertIn('unregistered-or-missing-skill',{e['code'] for e in distribution(self.root,catalog)})

    def test_missing_native_entry_rejected(self):
        catalog=self.skill()
        (self.root/'.agents/skills/example/SKILL.md').unlink()
        self.assertIn('native-discovery-drift',{e['code'] for e in distribution(self.root,catalog)})

    def test_category_drift_rejected(self):
        catalog=self.skill(); catalog['skills'][0]['category']='cloud'
        self.assertIn('category-drift',{e['code'] for e in distribution(self.root,catalog)})

    def test_duplicate_alias_rejected(self):
        catalog=self.skill(); catalog['skills'][0]['aliases']=['example']
        self.assertIn('duplicate-discovery-name',{e['code'] for e in distribution(self.root,catalog)})

    def test_stale_registry_rejected(self):
        catalog=self.skill(); (self.root/'00_skills/skills.registry.yaml').write_text('skills:\n- id: other\n')
        self.assertIn('registry-distribution-drift',{e['code'] for e in distribution(self.root,catalog)})

    def test_module_change_requires_review(self):
        catalog=self.skill(); package=self.root/'00_skills/(development)/example'
        write_json(self.root/'quality/skills-baseline.json',{'skills':{'example':package_hash(package)}})
        self.assertEqual(reviews(self.root,catalog)[0],[])
        (package/'reference.md').write_text('new behavior')
        self.assertEqual(reviews(self.root,catalog)[0][0]['code'],'new-or-changed-skill-needs-review')

    def test_valid_static_review(self):
        catalog=self.skill(); package=self.root/'00_skills/(development)/example'
        write_json(self.root/'quality/skills-baseline.json',{'skills':{}})
        write_json(self.root/'quality/reviews/example.json',{'package_hash':package_hash(package),
                   'positive_triggers':['request one','request two','request three'],'negative_scope':['outside scope','missing auth','missing evidence'],
                   'verification':{'kind':'structural-and-syntax','runtime_evaluated':False}})
        self.assertEqual(reviews(self.root,catalog),([],1))

    def test_stale_review_rejected(self):
        catalog=self.skill()
        write_json(self.root/'quality/skills-baseline.json',{'skills':{}})
        write_json(self.root/'quality/reviews/example.json',{'package_hash':'stale','positive_triggers':['a','b','c'],'negative_scope':['d','e','f'],'verification':{'kind':'behavioral'}})
        self.assertEqual(reviews(self.root,catalog)[0][0]['code'],'invalid-skill-review')

    def test_valid_mcp_tools(self):
        self.assertTrue(tools_valid([TOOL]))

    def test_duplicate_mcp_tools_rejected(self):
        self.assertFalse(tools_valid([TOOL,TOOL]))

    def test_invalid_input_schema_rejected(self):
        for schema in [None,{}, {'type':'array'}, {'type':'object','required':['missing']}, {'type':'object','properties':{'p':{'type':'banana'}}}]:
            with self.subTest(schema=schema):
                self.assertFalse(schema_valid(schema))

    def test_unknown_mcp_directory_rejected(self):
        (self.root/'unknown-mcp').mkdir()
        self.assertEqual(capabilities(self.root,{'mcps':[],'lsps':[]})[0][0]['code'],'mcp-inventory-drift')

    def test_unknown_lsp_directory_rejected(self):
        (self.root/'unknown-lsp').mkdir()
        self.assertEqual(capabilities(self.root,{'mcps':[],'lsps':[]})[0][0]['code'],'lsp-inventory-drift')

    def test_unregistered_server_configuration_rejected(self):
        (self.root/'lsp.json').write_text('{}')
        self.assertEqual(capabilities(self.root,{'mcps':[],'lsps':[]})[0][0]['code'],'unregistered-server-config')

    def test_embedded_editor_language_server_configuration_rejected(self):
        path=self.root/'.vscode/settings.json'; path.parent.mkdir()
        path.write_text('{"languageServer":{"command":"unknown"}}')
        self.assertEqual(capabilities(self.root,{'mcps':[],'lsps':[]})[0][0]['code'],'unregistered-server-config')

    def test_new_quarantine_cannot_hide_invalid_server(self):
        (self.root/'unknown-mcp').mkdir()
        entry={'id':'unknown','path':'unknown-mcp','state':'quarantined','owner':'codenavi-agent','reason':'skip','secret_policy':'runtime-references-only','baseline_hash':package_hash(self.root/'unknown-mcp')}
        self.assertEqual(capabilities(self.root,{'mcps':[entry],'lsps':[]})[0][0]['code'],'mcp-contract-failed')

    def test_legacy_source_change_invalidates_quarantine(self):
        p=self.root/'dark-videos-pipeline-mcp'; p.mkdir(); (p/'server.py').write_text('# baseline')
        entry={'id':p.name,'path':p.name,'state':'quarantined','owner':'codenavi-agent','reason':'legacy framing','secret_policy':'runtime-references-only','baseline_hash':package_hash(p)}
        self.assertEqual(capabilities(self.root,{'mcps':[entry],'lsps':[]})[0],[])
        (p/'server.py').write_text('# changed')
        self.assertEqual(capabilities(self.root,{'mcps':[entry],'lsps':[]})[0][0]['code'],'mcp-contract-failed')

    def test_known_upstream_controls(self):
        self.assertIsNone(verify_controls({'controls':{'guide':sha(b'known')}},lambda p:b'known'))

    def test_unrecognized_upstream_rule_blocks_update(self):
        with self.assertRaisesRegex(ValueError,'Unsupported TLC rule change'):
            verify_controls({'controls':{'guide':sha(b'known')}},lambda p:b'new mandatory rule')

    def test_alias_prevents_duplicate_import(self):
        catalog={'skills':[{'id':'web-accessibility','aliases':['accessibility']}]}
        self.assertEqual(missing_skills(catalog,{'skills':[{'name':'accessibility'}]}),[])

    def test_upstream_path_escape_blocks_import(self):
        with self.assertRaises(ValueError):
            missing_skills({'skills':[]},{'skills':[{'name':'new-skill','path':'../../secret','category':'development'}]})

    def test_auto_publication_cannot_change_guards(self):
        additions=[{'name':'new-skill','category':'development'}]
        for path in ['.github/workflows/ci.yml','quality/validate.py','quality/capabilities.json','AGENTS.md','00_skills/(development)/existing/SKILL.md']:
            with self.subTest(path=path): self.assertFalse(allowed(path,additions))
        self.assertTrue(allowed('00_skills/(development)/new-skill/SKILL.md',additions))

    def test_bad_registry_hash_cannot_write_a_package(self):
        entry={'name':'new-skill','path':'(development)/new-skill','category':'development','files':['SKILL.md'],'contentHash':'0'*64}
        with self.assertRaisesRegex(ValueError,'content hash mismatch'):
            import_skill(self.root,entry,lambda path:b'untrusted content','a'*40)
        self.assertFalse((self.root/'00_skills').exists())

    def test_failed_candidate_is_transactional(self):
        original=self.root/'important.txt'; original.write_text('original')
        def prepare(candidate,*args):
            (candidate/'important.txt').write_text('candidate mutation')
            (candidate/'extra.txt').write_text('new')
            return {'status':'PASS'}
        with patch('upstream._update',side_effect=prepare),patch('validate.validate',return_value={'status':'FAIL','errors':[{'code':'injected-failure'}]}):
            with self.assertRaisesRegex(ValueError,'Candidate gates failed'):
                update(self.root,lambda p:b'', 'a'*40,True)
        self.assertEqual(original.read_text(),'original')
        self.assertFalse((self.root/'extra.txt').exists())

    def test_noop_candidate_is_idempotent(self):
        original=self.root/'important.txt'; original.write_text('original')
        with patch('upstream._update',return_value={'status':'PASS'}),patch('validate.validate',return_value={'status':'PASS','counts':{}}):
            first=update(self.root,lambda p:b'', 'a'*40,True)
            second=update(self.root,lambda p:b'', 'a'*40,True)
        self.assertEqual(first['changed_files'],0); self.assertEqual(second['changed_files'],0)
        self.assertEqual(original.read_text(),'original')

    def test_workflow_rejects_floating_action(self):
        path=self.root/'.github/workflows/check.yml'; path.parent.mkdir(parents=True)
        path.write_text('name: Check\non:\n  push:\npermissions:\n  contents: read\njobs:\n  checks:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v7\n')
        self.assertEqual(workflows(self.root)[0]['code'],'workflow-contract')

    def test_workflow_rejects_failure_suppression(self):
        path=self.root/'.github/workflows/check.yml'; path.parent.mkdir(parents=True)
        path.write_text('name: Check\non:\n  push:\npermissions:\n  contents: read\njobs:\n  checks:\n    runs-on: ubuntu-latest\n    steps:\n      - run: validate\n        continue-on-error: true\n')
        self.assertEqual(workflows(self.root)[0]['code'],'workflow-contract')

    def test_automatic_publication_roundtrip_on_isolated_git_remote(self):
        import candidate
        import publish
        from common import artifact_sha
        producer=self.root/'producer'; consumer=self.root/'consumer'; remote=self.root/'remote.git'; artifact=self.root/'artifact'
        producer.mkdir()
        def git(cwd,*args):
            return subprocess.run(['git',*args],cwd=cwd,capture_output=True,check=True).stdout.decode().strip()
        git(self.root,'init','--bare',str(remote))
        git(producer,'init','-b','master')
        for directory in [producer]:
            git(directory,'config','user.name','Fixture'); git(directory,'config','user.email','fixture@example.invalid')
        write_json(producer/'quality/tlc-upstream.json',{'commit':'a'*40})
        git(producer,'add','.'); git(producer,'commit','-m','fixture baseline')
        git(producer,'remote','add','origin',str(remote)); git(producer,'push','origin','HEAD:master')
        git(self.root,'clone','--branch','master',str(remote),str(consumer))
        git(consumer,'config','user.name','Fixture'); git(consumer,'config','user.email','fixture@example.invalid')
        write_json(producer/'quality/tlc-upstream.json',{'commit':'b'*40})
        git(producer,'add','quality/tlc-upstream.json')
        patch_data=subprocess.run(['git','diff','--cached','--binary','--full-index'],cwd=producer,capture_output=True,check=True).stdout
        artifact.mkdir(); (artifact/'update.patch').write_bytes(patch_data)
        write_json(artifact/'manifest.json',{'base_sha':git(producer,'rev-parse','HEAD'),'source_commit':'b'*40,'additions':[],'patch_sha256':artifact_sha(patch_data),'validation':'PASS'})
        with patch.object(publish,'ROOT',consumer),patch.object(sys,'argv',['publish',str(artifact)]):
            self.assertEqual(publish.main(),0)
        self.assertEqual(json.loads((consumer/'quality/tlc-upstream.json').read_text())['commit'],'b'*40)
        self.assertEqual(git(consumer,'rev-parse','HEAD'),git(self.root,'--git-dir',str(remote),'rev-parse','master'))
        with patch.object(publish,'ROOT',consumer),patch.object(sys,'argv',['publish',str(artifact)]):
            with self.assertRaisesRegex(ValueError,'Master advanced'):
                publish.main()

    def test_secret_not_returned_in_findings(self):
        secret='ghp_'+'z'*40
        (self.root/'bad.txt').write_text(secret)
        errors,_=security_and_syntax(self.root)
        self.assertEqual(errors,[{'code':'possible-secret','path':'bad.txt'}])
        self.assertNotIn(secret,json.dumps(errors))

    def test_protocol_environment_has_no_credentials(self):
        with patch.dict(os.environ,{'GH_TOKEN':'fixture','DARKVIDEOS_SESSION_COOKIE':'fixture'}):
            self.assertNotIn('GH_TOKEN',environment())
            self.assertNotIn('DARKVIDEOS_SESSION_COOKIE',environment())

    def server(self,kind,broken=False):
        script=self.root/'server.py'
        script.write_text('''import json,sys
kind=sys.argv[1]
broken=sys.argv[2]=='broken'
while True:
    if kind=='mcp':
        line=sys.stdin.buffer.readline()
        if not line: break
        req=json.loads(line)
    else:
        header=sys.stdin.buffer.readline()
        if not header: break
        n=int(header.split(b':')[1]); sys.stdin.buffer.readline()
        req=json.loads(sys.stdin.buffer.read(n))
    if 'id' not in req:
        if req['method']=='exit': break
        continue
    if req['method']=='initialize':
        result={'capabilities':{'tools':{}},'serverInfo':{'name':'fixture','version':'1'},'protocolVersion':'2025-11-25' if not broken else 'wrong'}
    elif req['method']=='tools/list':
        result={'tools':[{'name':'demo.status','description':'Return fixture status','inputSchema':{'type':'object','properties':{},'additionalProperties':False}}]}
    elif req['method']=='shutdown': result=None
    else: result={}
    data=json.dumps({'jsonrpc':'2.0','id':req['id'],'result':result}).encode()
    if kind=='mcp': data+=b'\\n'
    else: data=f'Content-Length: {len(data)}\\r\\n\\r\\n'.encode()+data
    sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
''',encoding='utf-8')
        return [sys.executable,str(script),kind,'broken' if broken else 'valid']

    def test_real_mcp_stdio_roundtrip(self):
        result=probe(self.server('mcp'),self.root,'mcp')
        self.assertTrue(result['passed']); self.assertEqual(result['tools'],[TOOL])

    def test_invalid_mcp_negotiation_rejected(self):
        self.assertFalse(probe(self.server('mcp',True),self.root,'mcp')['passed'])

    def test_real_lsp_framed_roundtrip(self):
        self.assertTrue(probe(self.server('lsp'),self.root,'lsp')['passed'])

    def active_server(self,kind):
        self.server(kind)
        name='fixture-'+kind
        path=self.root/name; path.mkdir()
        (self.root/'server.py').rename(path/'server.py')
        entry={'id':name,'path':name,'state':'active','owner':'codenavi-agent','secret_policy':'runtime-references-only',
               'entrypoint':'server.py','command':[sys.executable,'server.py',kind,'valid'],
               'protocol':'jsonrpc-stdio' if kind=='mcp' else 'lsp-content-length'}
        if kind=='mcp': entry['tools']=[TOOL]
        else: entry.update(languages=['fixture'],file_extensions=['.fixture'])
        return entry

    def test_active_mcp_contract_and_runtime_pass(self):
        entry=self.active_server('mcp')
        errors,states=capabilities(self.root,{'mcps':[entry],'lsps':[]},True)
        self.assertEqual(errors,[]); self.assertEqual(states[0]['state'],'PROTOCOL_PASS')

    def test_active_lsp_contract_and_runtime_pass(self):
        entry=self.active_server('lsp')
        errors,states=capabilities(self.root,{'mcps':[],'lsps':[entry]},True)
        self.assertEqual(errors,[]); self.assertEqual(states[0]['state'],'PROTOCOL_PASS')

    def test_active_lsp_with_invalid_languages_rejected(self):
        entry=self.active_server('lsp'); entry['languages']='not-an-array'
        self.assertEqual(capabilities(self.root,{'mcps':[],'lsps':[entry]})[0][0]['code'],'lsp-contract-failed')

    def test_schema_with_invalid_required_elements_rejected(self):
        self.assertFalse(schema_valid({'type':'object','required':[{}]}))


if __name__=='__main__':
    unittest.main()
