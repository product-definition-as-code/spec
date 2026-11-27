#!/usr/bin/env python3
"""Fresh documentary assessments after frozen deterministic scoring; no expert/proof certification."""
import argparse, json, shutil, subprocess, time, uuid
from pathlib import Path
from pilot import HERE, load, dump, sha
from isolation import namespace,environment

PROMPT='''Read approved-intent.md, protocol.md, machine-summary.json and trajectory files. You are an independent documentary reviewer, not their author, a human expert or a mathematical verifier. Do not execute submitted programs or alter evidence. Assess explicitly structural impact, citation freshness, declared formal dependencies, mathematical validity versus current-intent applicability, unsupported assumptions and unresolved decisions. Cite concrete path/line or receipt for every finding; severity P0..P3, no speculative scope expansion. Evidence source pins are whole-file; no automatic renewal. State exposure/unblinding, unknown completeness and provider limitations. Write assessment.json with status, findings(list), hypothesis_assessments(mapping), limitations(list), recommendation(proceed/narrow/revise/pause/stop). An agent review is not proof, general correctness or human intent acceptance.'''

def session(work,target,prompt,model):
    auth=target/'auth';auth.mkdir(mode=0o700);shutil.copyfile(Path.home()/'.codex/auth.json',auth/'auth.json');(auth/'auth.json').chmod(0o600)
    cmd=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--model',model,'-c','model_reasoning_effort="medium"','--sandbox','workspace-write','--json',prompt]
    unit='pdac-review-'+uuid.uuid4().hex
    wrapped=['systemd-run','--user','--quiet','--wait','--pipe','--collect','--unit='+unit,'-p','MemoryMax=4294967296','-p','MemorySwapMax=0','-p','RuntimeMaxSec=480','-p','TasksMax=128','-p','KillMode=control-group','--',*namespace(work,cmd,auth=auth)]
    start=time.monotonic()
    pins={str(p.relative_to(work)):sha(p) for p in work.rglob('*') if p.is_file()}
    try:
        try:r=subprocess.run(wrapped,env=environment(),capture_output=True,timeout=495)
        except subprocess.TimeoutExpired as e:
            subprocess.run(['systemctl','--user','kill','--kill-whom=all',unit],capture_output=True);r=subprocess.CompletedProcess(cmd,124,e.stdout or b'',e.stderr or b'')
        except OSError as e:r=subprocess.CompletedProcess(cmd,127,b'',str(e).encode())
    finally:(auth/'auth.json').unlink(missing_ok=True)
    (target/'events.jsonl').write_bytes(r.stdout);(target/'stderr').write_bytes(r.stderr)
    intact=all((work/p).is_file() and not (work/p).is_symlink() and sha(work/p)==pin for p,pin in pins.items())
    result={'returncode':r.returncode,'wall_seconds':time.monotonic()-start,'inputs_unchanged':intact,'input_pins':pins,'events_sha256':sha(target/'events.jsonl'),'model_requested':model,'resolved_weights':'not exposed','role':'fresh independent agent assessment, not human expert validation','automatic_retries':0}
    dump(target/'receipt.json',result);return result

def evaluate(pilot,scored,out):
    frozen=load(pilot/'frozen-inputs.json');approval=load(pilot/'approval.json');submissions=load(pilot/'submissions.json')
    assert approval['frozen_manifest_sha256']==sha(pilot/'frozen-inputs.json')
    assert len(submissions['submissions'])==64 and all((pilot/'attempts'/j['id']/'receipt.json').is_file() for j in frozen['plan'])
    assert load(scored/'inputs.json')['manifest_sha256']==sha(pilot/'submissions.json')
    out.mkdir(parents=True,exist_ok=False);assessments=[]
    for seed in ['17','29']:
        for cohort in [1,2,3,4]:
            label='trajectory-'+str(len(assessments)+1);target=out/label;work=target/'work';work.mkdir(parents=True)
            shutil.copyfile(HERE/'product-intent.md',work/'approved-intent.md');shutil.copyfile(HERE/'frozen-protocol.md',work/'protocol.md')
            current=[x for x in load(scored/'summary.json')['counts'] if str(x['seed'])==seed and x['cohort']==str(cohort)]
            dump(work/'machine-summary.json',[{k:v for k,v in x.items() if k not in ['cohort','seed']} for x in current])
            for row in submissions['submissions']:
                if str(row['seed'])!=seed or row['cohort']!=cohort:continue
                source=Path(row['path']);destination=work/row['episode']
                if source.exists():shutil.copytree(source,destination,symlinks=True,ignore=shutil.ignore_patterns('.git','home','bin','__pycache__'))
                if destination.exists():
                    for path in destination.rglob('*'):
                        if path.is_symlink():path.unlink()
            (work/'AGENTS.md').write_text('Read only supplied evidence; no external lookup, private cases, authored program execution, paid services or retired agent-toolkit. Write assessment.json only. Representation may reveal treatment.\n')
            receipt=session(work,target,PROMPT,frozen['model_requested'])
            assessments.append({'label':label,'seed':seed,'cohort':cohort,'receipt':receipt,'assessment_sha256':sha(work/'assessment.json') if (work/'assessment.json').is_file() and not (work/'assessment.json').is_symlink() else None})
    synthesis=out/'synthesis';work=synthesis/'work';work.mkdir(parents=True)
    shutil.copyfile(HERE/'product-intent.md',work/'approved-intent.md');shutil.copyfile(HERE/'frozen-protocol.md',work/'protocol.md');shutil.copyfile(scored/'summary.json',work/'machine-summary.json')
    for item in assessments:
        src=out/item['label']/'work/assessment.json'
        if item['assessment_sha256']:shutil.copyfile(src,work/(item['label']+'.json'))
    dump(work/'assessment-map.json',assessments)
    receipt=session(work,synthesis,PROMPT+' Synthesize all eight trajectories and deterministic paired comparisons. Missing/failed reviews are inconclusive, never replace or retry them. Recommend G2 action with exact unsupported endpoints. Do not authorize phase3 or normative changes.',frozen['model_requested'])
    dump(out/'G2-inputs.json',{'status':'evidence prepared, owner G2 decision required','frozen_manifest_sha256':sha(pilot/'frozen-inputs.json'),'approval':approval,'score_inputs':load(scored/'inputs.json'),'assessments':assessments,'synthesis_receipt':receipt,'phase3_authorized':False})
    print('G2 evidence assembled; no phase3 execution authorized.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pilot',type=Path,required=True);p.add_argument('--score',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();evaluate(a.pilot.resolve(),a.score.resolve(),a.output.resolve())
