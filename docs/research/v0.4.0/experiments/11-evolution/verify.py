#!/usr/bin/env python3
"""Audit saved receipts and accepted Git history, independently of a running agent."""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
from formal import EXPECTED


def verify(root):
    manifest=json.loads((root/'run-manifest.json').read_text());rows=manifest['stages']
    assert [r['stage'] for r in rows]==['baseline','rule','identity','lifecycle','domain','unrelated','editorial']
    assert manifest['llm_calls_by_runner']==0 and manifest['automatic_retries']==0
    assert manifest['negative_proposal']['formal_consistency']=='unsat' and not manifest['negative_proposal']['applied']
    executed_queries=0
    for p in (root/'logs').glob('*.json'):
        data=json.loads(p.read_text())
        for suffix in ['stdout','stderr']:
            assert hashlib.sha256(p.with_suffix('.'+suffix).read_bytes()).hexdigest()==data[suffix+'_sha256']
        for path,value in data.get('input_sha256',{}).items():
            if '/formal/' in path:
                actual=root/'formal'/path.split('/formal/',1)[1]
                assert actual.resolve().is_relative_to((root/'formal').resolve())
                assert hashlib.sha256(actual.read_bytes()).hexdigest()==value
                executed_queries+=sum(1 for line in actual.read_text().splitlines() if line=='(check-sat)')
        assert 'MemoryMax=2147483648' in data['containment_command']
        assert 'RuntimeMaxSec=30' in data['containment_command']
        assert 'KillMode=control-group' in data['containment_command']
    for row in rows:
        for engine in ['z3','cvc5']:assert row['formal'][engine]['statuses']==EXPECTED
        for doc in row.get('new_evidence',row.get('evidence'))['documents']:
            assert doc['runRevision']==row.get('post_apply_full_recheck',row['formal'])['run_revision']
            assert all(x['outcome']=='passed' and x['citationStatuses']==['current'] for x in doc['evidenceResults'])
    stages={r['stage']:r for r in rows}
    for name in ['identity','lifecycle']:
        assert stages[name]['model_changed'] and not stages[name]['direct_uc_changed'] and not stages[name]['forecast']
        assert all(x['citationStatuses']==['current'] for x in stages[name]['evidence_before_new_run']['documents'][0]['evidenceResults'])
    for name in ['domain','editorial']:
        assert any(c['id']=='SB-A' and c['form']=='verification-evidence' and c['prospectiveStatus']=='stale' for c in stages[name]['forecast'])
        old=stages[name]['evidence_before_new_run']['documents'][0]['evidenceResults'][0]
        assert old['outcome']=='passed' and old['citationStatuses']==['stale']
    for name in ['unrelated','editorial']:
        assert not stages[name]['model_changed']
        for engine in ['z3','cvc5']:assert stages[name]['formal'][engine]['cache_hit']
    probe=manifest['retired_contract_and_unmapped_intent_probes']['unmapped-intent']
    assert probe['unchanged_formula_still_verifies'] and probe['formal_dependency_pin_changed']
    assert not probe['applied'] and not probe['published_new_evidence']
    for engine in ['z3','cvc5']:assert probe['corrected_encoding'][engine]['statuses'][5]=='unsat'
    # The bundle retains the exact executable Product Change history and run commits.
    with tempfile.TemporaryDirectory(prefix='pdac-history-audit-') as temp:
        subprocess.run(['git','clone','--quiet','--no-checkout',str(root/'history.bundle'),temp],check=True)
        def git(*a):return subprocess.check_output(['git',*a],cwd=temp)
        for row in rows:
            git('cat-file','-e',row['revision']+'^{commit}')
            for doc in row.get('new_evidence',row.get('evidence'))['documents']:git('cat-file','-e',doc['runRevision']+'^{commit}')
            # Accepted change containers are immutable through all later stages.
            paths=git('ls-tree','-r','--name-only',row['revision'],'docs/product/changes/completed').decode().splitlines()
            for path in paths:assert git('show',row['revision']+':'+path)==git('show','HEAD:'+path)
        assert len(git('ls-tree','--name-only','HEAD:docs/product/changes/completed').splitlines())==7
    records=[json.loads(p.read_text()) for p in (root/'logs').glob('*.json')]
    summary={'tool_jobs':len(records),'recorded_tool_wall_seconds':round(sum(r['wall_seconds'] for r in records),3),'executed_solver_queries':executed_queries,'recorded_input_queries':sum(sum(1 for line in p.read_text().splitlines() if line=='(check-sat)') for p in (root/'formal').rglob('*.smt2')),'stages':7,'applied_changes_including_initial':7,'automatic_retries':0,'llm_calls_by_runner':0,'audit':'receipts, explicit findings and immutable accepted history verified'}
    print(json.dumps(summary,indent=2));return summary

if __name__=='__main__':verify(Path(sys.argv[1]).resolve())
