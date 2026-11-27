"""Reproduce the failed trial's accounting from public evidence, without an LLM or solver call."""
import argparse,collections,hashlib,importlib.util,json,subprocess,tarfile,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())

def audit(result_folder):
    stats=load(result_folder/'result.json');archive=result_folder/'public-evidence.tar.gz'
    assert sha(archive)==stats['public_archive_sha256']
    with tempfile.TemporaryDirectory(prefix='pdac-result-audit-') as folder:
        root=Path(folder)
        with tarfile.open(archive) as tar:
            assert all(m.isfile() or m.isdir() for m in tar.getmembers())
            tar.extractall(root,filter='data')
        index=load(root/'manifest.json');assert sha(root/'manifest.json')==stats['public_file_manifest_sha256']
        assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}==set(index)|{'manifest.json'}
        for name,pin in index.items():assert sha(root/name)==pin,name
        frozen=load(root/'frozen-inputs.json');approval=load(root/'approval.json')
        assert sha(root/'frozen-inputs.json')==stats['frozen_manifest_sha256']==approval['frozen_manifest_sha256']
        assert frozen['source_revision']==approval['source_revision']==stats['source_commit']
        receipts=[load(p) for p in (root/'authors').glob('*/receipt.json')]
        launched=[x for x in receipts if 'wall_seconds' in x]
        assert len(receipts)==64 and len(launched)==8
        assert sum(x['status']=='blocked by failed predecessor' for x in receipts)==56
        histories=0
        for receipt in launched:
            attempt=root/'authors'/receipt['job']['id'];assert sha(attempt/'events.jsonl')==receipt['events_sha256']
            assert receipt['inputs_unchanged'] and receipt['outputs']=={} and receipt['readiness_defects']
            for name,pin in receipt['input_pins'].items():assert sha(attempt/'work'/name)==pin
            history=root/('history-'+str(histories))
            subprocess.run(['git','clone','--quiet','--no-checkout',str(attempt/'history.bundle'),str(history)],check=True,timeout=15)
            subprocess.run(['git','cat-file','-e',receipt['revision']+'^{commit}'],cwd=history,check=True,timeout=15)
            for name,pin in receipt['input_pins'].items():
                data=subprocess.check_output(['git','show',receipt['revision']+':'+name],cwd=history,timeout=15)
                assert hashlib.sha256(data).hexdigest()==pin
            histories+=1
        assert not list((root/'authors').glob('*/solver-receipts/query-*.json'))
        assert not list((root/'score').glob('*/decision.json'))
        original=load(root/'score/custody-file-index.json')
        assert original['cases.json']==frozen['custody_commitment']['private_commitments']['cases.json']
        assert not any(Path(name).name in ['decision.json','z3-run.json','cvc5-run.json'] for name in original)
        assert sha(HERE/'score.py')==frozen['public_inputs']['score.py'],'use frozen scorer to reproduce accounting'
        spec=importlib.util.spec_from_file_location('frozen_scorer',HERE/'score.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        rows=load(root/'score/public-rows.json');stored=load(root/'score/public-summary.json');recomputed=module.summarize(rows)
        assert len(rows)==4656 and all(x['outcome']=='unknown' for x in rows)
        for key in ['counts','comparisons','primary_screen_both_schedules']:assert recomputed[key]==stored[key],key
        sort=lambda xs:sorted(xs,key=lambda x:(x['seed'],x['episode'],x['id']))
        assert sort(recomputed['paired_4_vs_3'])==sort(stored['paired_4_vs_3'])
        assert recomputed['primary_screen_both_schedules'] is False
        review_receipts=list((root/'reviews').glob('*/receipt.json'));assert len(review_receipts)==9
        assert not list((root/'reviews').glob('*/assessment.json'))
        canary=load(root/'diagnostics/guarded-preflight/preflight.json');assert not canary['passed'] and canary['model_calls']==0
        derived={'planned_author_slots':len(receipts),'launched_author_sessions':len(launched),'blocked_by_predecessor':len(receipts)-len(launched),'unknown_observations':len(rows),'documentary_sessions_launched':len(review_receipts),'documentary_assessments_produced':0,'actual_author_solver_processes':0,'actual_scoring_solver_processes':0,'actual_scoring_python_workers':0,'actual_product_changes_applied':0}
        for key,value in derived.items():assert stats[key]==value,key
        author_usage=collections.Counter()
        for receipt in launched:author_usage.update(receipt.get('usage') or {})
        assert dict(author_usage)==stats['author_usage']
        assert stats['summed_author_wall_seconds']==round(sum(x['wall_seconds'] for x in launched),3)
        result={'audit':'passed','author_slots':64,'launched_authors':8,'blocked_successors':56,'unknown_observations':len(rows),'preserved_histories':histories,'actual_solver_processes':0,'review_attempts':9,'review_assessments':0,'primary_interpretation':'not estimable; invalid trial, not a negative PDaC finding','LLM_calls_by_audit':0,'solver_calls_by_audit':0}
        print(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('result_folder',type=Path);a=p.parse_args();audit(a.result_folder)
