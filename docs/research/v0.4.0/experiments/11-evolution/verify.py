#!/usr/bin/env python3
"""Audit raw execution evidence and source bindings; not a proof-authenticity oracle."""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
import yaml
from formal import EXPECTED, encode, fingerprint, statuses

IDS={'rule':'chg-lead','identity':'chg-issuers','lifecycle':'chg-expiry',
     'domain':'chg-footprint','unrelated':'chg-retention','editorial':'chg-editorial'}
ENGINES=['z3','cvc5']


def expected_jobs():
    names={'version','node-version','z3-version','cvc5-version','init','chg-initial-create',
           'initial-draft-blocked','chg-initial-overlay','chg-initial-acknowledged','initial-dry',
           'initial-apply','baseline-validation','baseline-z3','baseline-cvc5','baseline-new-evidence',
           'baseline-citations','cite-proof-contract-uc-a','cite-proof-contract-sb-a',
           'cite-proof-contract-sb-auth','cite-rule-contract-br-a','chg-contradiction-create',
           'contradiction-structural-validation','contradiction-formal','contradiction-archive',
           'old-lead-contract','old-issuer-contract','old-footprint-contract','chg-unmapped-create',
           'unmapped-structural-validation','unmapped-archive'}
    for stage,id in IDS.items():
        names.update(id+s for s in ['-create','-overlay','-acknowledged'])
        names.update(stage+s for s in ['-draft-overlay','-forecast','-apply','-validation',
                                      '-old-evidence','-citations','-new-evidence'])
        names.update(stage+'-'+phase+'-'+engine for phase in ['overlay','accepted'] for engine in ENGINES)
    names.update(stage+'-unaccounted-blocked' for stage in ['rule','identity','lifecycle','domain'])
    names.update(phase+'-'+engine for phase in ['unmapped-old-encoding','unmapped-corrected-encoding'] for engine in ENGINES)
    return names


def normalized_digest(data):
    return 'sha256:'+hashlib.sha256(data.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()


def verify(root):
    manifest=json.loads((root/'run-manifest.json').read_text());rows=manifest['stages']
    assert [r['stage'] for r in rows]==['baseline',*IDS]
    assert manifest['llm_calls_by_runner']==0 and manifest['automatic_retries']==0
    assert manifest['negative_proposal']=={'productshape_errors':0,'formal_consistency':'unsat','applied':False}
    actual={p.stem for p in (root/'logs').glob('*.json')}
    assert actual==expected_jobs(),('Missing/unexpected receipts',expected_jobs()-actual,actual-expected_jobs())
    blocked={'initial-draft-blocked',*(s+'-unaccounted-blocked' for s in ['rule','identity','lifecycle','domain'])}
    receipts={};executed_queries=0
    for name in sorted(actual):
        p=root/'logs'/(name+'.json');data=json.loads(p.read_text());receipts[name]=data
        for suffix in ['stdout','stderr']:assert hashlib.sha256(p.with_suffix('.'+suffix).read_bytes()).hexdigest()==data[suffix+'_sha256']
        assert data['returncode']==(1 if name in blocked else 0) and data.get('failure_class') is None,(name,data['returncode'])
        for path,value in data.get('input_sha256',{}).items():
            if '/formal/' in path:
                source=root/'formal'/path.split('/formal/',1)[1]
                assert source.resolve().is_relative_to((root/'formal').resolve())
                assert hashlib.sha256(source.read_bytes()).hexdigest()==value
                executed_queries+=sum(line=='(check-sat)' for line in source.read_text().splitlines())
        for flag in ['MemoryMax=2147483648','RuntimeMaxSec=30','KillMode=control-group']:assert flag in data['containment_command']
    def raw(name):return json.loads((root/'logs'/(name+'.stdout')).read_text())
    def solver(label,engine,claimed,expected):
        name=label+'-'+engine;data=receipts[name]
        observed=statuses((root/'logs'/(name+'.stdout')).read_bytes())
        assert observed==expected==claimed['statuses'],(name,observed)
        model=(root/'formal'/label/'model.smt2').read_text()
        assert any('/formal/'+label+'/model.smt2' in p for p in data['input_sha256'])
        assert claimed['fingerprint']==fingerprint(model,claimed['solver_sha256'])
        assert Path(data['command'][0]).name==engine
        if claimed['cache_hit']:
            prior=claimed['cache_source'];assert prior and prior!=label
            assert (root/'formal'/prior/'model.smt2').read_text()==model
            assert statuses((root/'logs'/(prior+'-'+engine+'.stdout')).read_bytes())==observed
    for row in rows:
        label='baseline' if row['stage']=='baseline' else row['stage']+'-overlay'
        for engine in ENGINES:solver(label,engine,row['formal'][engine],EXPECTED)
        if row['stage']!='baseline':
            for engine in ENGINES:
                solver(row['stage']+'-accepted',engine,row['post_apply_full_recheck'][engine],EXPECTED)
                assert row['formal'][engine]['fingerprint']==row['post_apply_full_recheck'][engine]['fingerprint']
            forecast=raw(row['stage']+'-forecast');applied=raw(row['stage']+'-apply')
            assert forecast['dryRun'] and not applied['dryRun']
            assert row['forecast']==forecast['affectedCitations']==applied['affectedCitations']
            assert raw(row['stage']+'-old-evidence')==row['evidence_before_new_run']
        assert raw(row['stage']+'-new-evidence')==row.get('new_evidence',row.get('evidence'))
    probe=manifest['retired_contract_and_unmapped_intent_probes']['unmapped-intent']
    assert probe['unchanged_formula_still_verifies'] and probe['formal_dependency_pin_changed']
    assert not probe['applied'] and not probe['published_new_evidence']
    negative=list(EXPECTED);negative[5]='unsat'
    for engine in ENGINES:solver('unmapped-corrected-encoding',engine,probe['corrected_encoding'][engine],negative)
    for engine in ENGINES:assert statuses((root/'logs'/('unmapped-old-encoding-'+engine+'.stdout')).read_bytes())==EXPECTED
    for name in ['old-lead-contract','old-issuer-contract','old-footprint-contract']:assert statuses((root/'logs'/(name+'.stdout')).read_bytes())==['sat']
    assert statuses((root/'logs/contradiction-formal.stdout').read_bytes())==['unsat']
    for name in blocked:assert raw(name)['applied'] is False
    for name in blocked-{'initial-draft-blocked'}:assert any(d['code']=='PRODUCT034' for d in raw(name)['diagnostics'])
    stages={r['stage']:r for r in rows}
    for name in ['identity','lifecycle']:
        assert stages[name]['model_changed'] and not stages[name]['direct_uc_changed'] and not stages[name]['forecast']
        assert all(x['citationStatuses']==['current'] for x in stages[name]['evidence_before_new_run']['documents'][0]['evidenceResults'])
    assert set(stages['domain']['changed'])=={'TERM-A','SB-A','UC-A','LC-A'}
    for name in ['domain','editorial']:
        assert any(c['id']=='SB-A' and c['form']=='verification-evidence' and c['prospectiveStatus']=='stale' for c in stages[name]['forecast'])
        old=stages[name]['evidence_before_new_run']['documents'][0]['evidenceResults'][0]
        assert old['outcome']=='passed' and old['citationStatuses']==['stale']
    for name in ['unrelated','editorial']:
        assert not stages[name]['model_changed'] and all(stages[name]['formal'][e]['cache_hit'] for e in ENGINES)
    # Reconstruct recorded inputs from the bundled history, including actual proposed overlays.
    with tempfile.TemporaryDirectory(prefix='pdac-history-audit-') as temp:
        subprocess.run(['git','clone','--quiet','--no-checkout',str(root/'history.bundle'),temp],check=True)
        def git(*a):return subprocess.check_output(['git',*a],cwd=temp)
        def artifacts(rev,prefix='docs/product/model'):
            mapping={}
            for path in git('ls-tree','-r','--name-only',rev,prefix).decode().splitlines():
                if not path.endswith('.md') or Path(path).name=='README.md':continue
                data=git('show',rev+':'+path)
                if not data.startswith(b'---'):continue
                front=yaml.safe_load(data.decode().split('---',2)[1]);id=front['id'];assert id not in mapping;mapping[id]=data
            return mapping
        def bind(label,source,expected_revision):
            meta=json.loads((root/'formal'/label/'semantic-inputs.json').read_text())
            assert meta['actual_run_revision']==expected_revision,label
            git('cat-file','-e',expected_revision+'^{commit}')
            assert {id:normalized_digest(data) for id,data in source.items()}==meta['source_pins'],label
            folder=Path(temp)/'materialized'/label;folder.mkdir(parents=True)
            paths={}
            for id,data in source.items():paths[id]=folder/(id+'.md');paths[id].write_bytes(data)
            assert encode(paths,meta['values'])==(root/'formal'/label/'model.smt2').read_text(),label
        for row in rows:
            stage=row['stage'];revision=row['revision'];git('cat-file','-e',revision+'^{commit}')
            # Accepted containers must remain byte-identical throughout later history.
            for path in git('ls-tree','-r','--name-only',revision,'docs/product/changes/completed').decode().splitlines():assert git('show',revision+':'+path)==git('show','HEAD:'+path)
            if stage=='baseline':bind('baseline',artifacts(row['formal']['run_revision']),row['formal']['run_revision'])
            else:
                original=artifacts(row['formal']['run_revision'])
                original.update(artifacts(row['post_apply_full_recheck']['run_revision'],'docs/product/changes/completed/'+IDS[stage]+'/proposed'))
                bind(stage+'-overlay',original,row['formal']['run_revision'])
                bind(stage+'-accepted',artifacts(row['post_apply_full_recheck']['run_revision']),row['post_apply_full_recheck']['run_revision'])
            evidence=row.get('new_evidence',row.get('evidence'))
            for doc in evidence['documents']:
                assert doc['runRevision']==row.get('post_apply_full_recheck',row['formal'])['run_revision']
                assert all(x['outcome']=='passed' and x['citationStatuses']==['current'] for x in doc['evidenceResults'])
                record=json.loads(git('show',revision+':evidence/history/'+stage+'.json'))
                assert record['revision']==doc['runRevision']
                source=artifacts(record['revision'])
                for result in record['results']:
                    for citation in result['citations']:assert citation['digest']==normalized_digest(source[citation['id']])
        all_paths=git('ls-tree','-r','--name-only','HEAD').decode().splitlines()
        proposals=[p for p in all_paths if '/chg-unmapped/proposed/' in p]
        assert len(proposals)==1
        drift=artifacts(probe['corrected_encoding']['run_revision']);drift.update(artifacts('HEAD',str(Path(proposals[0]).parent)))
        bind('unmapped-old-encoding',drift,probe['corrected_encoding']['run_revision']);bind('unmapped-corrected-encoding',drift,probe['corrected_encoding']['run_revision'])
        assert len(git('ls-tree','--name-only','HEAD:docs/product/changes/completed').splitlines())==7
    assert executed_queries==334
    summary={'tool_jobs':len(receipts),'recorded_tool_wall_seconds':round(sum(r['wall_seconds'] for r in receipts.values()),3),'executed_solver_queries':executed_queries,'stages':7,'applied_changes_including_initial':7,'automatic_retries':0,'llm_calls_by_runner':0,'audit':'required receipts/raw statuses, source bindings, revisions, full/cache consistency and immutable accepted history verified'}
    print(json.dumps(summary,indent=2));return summary

if __name__=='__main__':verify(Path(sys.argv[1]).resolve())
