#!/usr/bin/env python3
"""Deterministic public change simulation; semantic dependencies are authored, not inferred."""
import hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path
import yaml
from run import HERE, run


def digest(data):
    return 'sha256:'+hashlib.sha256(data.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()


def frontmatter(data):
    return yaml.safe_load(data.decode().split('---',2)[1])


def main(z3, output):
    output.mkdir(parents=True, exist_ok=False)
    original={p.name:p.read_bytes() for p in (HERE/'intent').glob('*.md')}
    by_id={frontmatter(b)['id']:n for n,b in original.items()}
    # Deliberately external, manual mapping, not new canonical PDaC fields.
    dependencies={'confirm-capacity':['BR-A','TERM-A','LC-A'],
                  'authorization':['UC-A','TERM-IDENTITY']}
    reverse={i:set() for i in by_id}
    for name,data in original.items():
        fm=frontmatter(data); source=fm['id']
        targets=[]
        for key in ['subject','defined-in','primary-actor','uses-terms','governed-by','illustrates']:
            v=fm.get(key,[]);targets.extend(v if isinstance(v,list) else [v])
        if fm.get('covers-transition'):targets.append(fm['covers-transition']['lifecycle'])
        for t in fm.get('transitions',[]):
            for k in ['initiated-by','governed-by','realized-by']:targets.extend(t.get(k,[]))
        for target in targets:reverse[target].add(source)
    def closure(prop):
        # Dependency traversal is deterministic; map completeness is not proven.
        return {i:digest(original[by_id[i]]) for i in dependencies[prop]}
    pins={p:closure(p) for p in dependencies}
    uc_pin=digest(original['uc-a.md'])
    stages=[('rule', 'br-a.md', b'at most 60 days', b'at most 30 days', 'sat'),
            ('domain','term-a.md',b'one indivisible room slot',b'two indivisible room slots','sat'),
            ('external','term-identity.md',b'Only issuer A is trusted.',b'Issuers A and B are trusted.','sat'),
            ('unrelated','br-unrelated.md',b'7 days',b'14 days','unsat'),
            ('editorial','uc-a.md',b'## Goal',b'<!-- Editorial spelling note; no modeled predicate changed. -->\n\n## Goal','unsat')]
    rows=[];queries='(set-logic QF_LIA)\n(set-option :produce-models true)\n'
    with tempfile.TemporaryDirectory(prefix='pdac-exploration-') as temp:
        repo=Path(temp);model=repo/'docs/product/model';model.mkdir(parents=True)
        for n,b in original.items():(model/n).write_bytes(b)
        def git(*args):return subprocess.check_output(['git',*args],cwd=repo,env={**os.environ,'GIT_AUTHOR_NAME':'Research fixture','GIT_AUTHOR_EMAIL':'research@example.invalid','GIT_COMMITTER_NAME':'Research fixture','GIT_COMMITTER_EMAIL':'research@example.invalid','GIT_AUTHOR_DATE':'2026-11-27T00:00:00Z','GIT_COMMITTER_DATE':'2026-11-27T00:00:00Z'},stderr=subprocess.DEVNULL).decode().strip()
        git('init','-b','main');git('add','.');git('commit','-m','Draft research baseline; not accepted product intent')
        for idx,(label,name,old,new,expected) in enumerate(stages,1):
            base=git('rev-parse','HEAD');prior={p.name:p.read_bytes() for p in model.glob('*.md')}
            assert old in prior[name]
            (model/name).write_bytes(prior[name].replace(old,new))
            changed=frontmatter(prior[name])['id'];current={p.name:p.read_bytes() for p in model.glob('*.md')}
            changed_pins={p:[i for i,h in pins[p].items() if digest(current[by_id[i]])!=h] for p in dependencies}
            direct_current=digest(current['uc-a.md'])==uc_pin
            affected=sorted(reverse[changed])
            change_id='CHG-EXP-'+str(idx)
            proposal=output/change_id.lower();(proposal/'proposed').mkdir(parents=True)
            (proposal/'proposed'/name).write_bytes(current[name])
            fm={'id':change_id,'type':'product-change','title':'Draft '+label+' perturbation','status':'draft','base-revision':base,'operations':{'add':[],'modify':[changed],'remove':[]},'unaffected':[]}
            # Not approved/applicable: one-hop review/acceptance intentionally pending.
            text='---\n'+yaml.safe_dump(fm,sort_keys=False)+'---\n\n'
            for heading,body in [('Problem','Research-only '+label+' perturbation.'),('Intended Product Outcome','Explore changed applicability; no real product decision accepted.'),('Rationale','Test freshness separately from formal dependency and validity.'),('Affected Product Areas',', '.join(affected) or 'None in declared one-hop graph.'),('Open Questions','None.'),('Product Acceptance','Not accepted; these are experimental draft proposals.'),('Out of Scope','Production, approval/apply and normative contract changes.')]:text+=f'## {heading}\n\n{body}\n\n'
            (proposal/'change.md').write_text(text)
            # Each query isolates the new change, not accumulated prior changes.
            formulas={
              'rule':'(declare-const day Int)\n(assert (and (>= day 0) (<= day 60) (> day 30)))',
              'domain':'(declare-const capacity Int)\n(declare-const used Int)\n(assert (and (> capacity 0) (<= 0 used) (< used capacity) (> (+ used 2) capacity)))',
              'external':'(declare-const issuer Int)\n(assert (and (or (= issuer 0) (= issuer 1)) (not (= issuer 0))))',
              'unrelated':'(assert (not (= 60 60)))',
              'editorial':'(assert (not (= 60 60)))'}
            # push scopes do not scope declarations in every SMT engine, hence unique names.
            formula=formulas[label].replace('capacity',f'capacity{idx}').replace('used',f'used{idx}').replace('day',f'day{idx}').replace('issuer',f'issuer{idx}')
            queries+=f'(echo "{label}")\n(push 1)\n'+formula+'\n(check-sat)\n'
            if expected=='sat':
                terms={'rule':f'day{idx}','domain':f'capacity{idx} used{idx}','external':f'issuer{idx}'}[label];queries+=f'(get-value ({terms}))\n'
            queries+='(pop 1)\n'
            rows.append({'change':change_id,'kind':label,'base_revision':base,'changed_id':changed,'one_hop_dependents':affected,'direct_uc_citation_current':direct_current,'changed_baseline_formal_pins':changed_pins,'expected_delta_query':expected,'historical_result':'retained for original model/assumptions','applicability':'requires review; not inferred solely from hashes','proposal_sha256':digest(text.encode())})
            # Advancing this private snapshot is not PDaC approval/apply.
            git('add','.');git('commit','-m','Unaccepted exploratory snapshot '+label)
    (output/'delta-queries.smt2').write_text(queries)
    result=run('evolution-delta',[z3,str(output/'delta-queries.smt2')],output)
    observed=[s for s in result.stdout.decode().splitlines() if s in ['sat','unsat','unknown']]
    assert observed==[r['expected_delta_query'] for r in rows],observed
    for row,status in zip(rows,observed):row['observed_delta_query']=status
    report={'status':'public exploratory simulation; no approval/apply/conformance claim','baseline_formal_dependency_pins':pins,'dependency_completeness':'manual and unaudited beyond these seeded cases','stages':rows,'query_interpretation':'isolated delta per stage, historical pins compared cumulatively; unrelated/editorial preservation is under an explicit unchanged-encoding assumption, not NLP equivalence proof'}
    (output/'evolution.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Five change snapshots: expected formal deltas confirmed; graph/hashes are distinct from intent applicability.')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('z3');p.add_argument('output',type=Path);a=p.parse_args();main(str(Path(a.z3).resolve()),a.output.resolve())
