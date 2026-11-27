#!/usr/bin/env python3
"""Actual ProductShape apply/forecast + external formal checks; no inference calls."""
import argparse, copy, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
import yaml

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from run import run as bounded
from formal import encode, statuses, fingerprint, EXPECTED, DEPENDENCIES, fm


def digest(path):
    return 'sha256:'+hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()


def write_fm(path,data,body):
    path.write_text('---\n'+yaml.safe_dump(data,sort_keys=False)+'---'+body)


def amend(path,transform):
    _,front,body=path.read_text().split('---',2);data=yaml.safe_load(front)
    data,body=transform(data,body);write_fm(path,data,body)


class Experiment:
    def __init__(self,output,package,tools):
        self.out=output;output.mkdir(parents=True,exist_ok=False)
        self.repo=output/'workspace';self.repo.mkdir()
        self.logs=output/'logs';self.cli=str(package/'node_modules/@prodshape/cli/dist/bin.js')
        p=json.loads((package/'node_modules/@prodshape/cli/package.json').read_text());assert p['version']=='0.26.1'
        self.package=package;self.tools=tools;self.cache={};self.rows=[];self.current=False
        self.ps('version','--version',json_output=False)
        self.git('init','-q','-b','main')
        self.ps('init','init','--sdd','none',json_output=False)
        config=self.repo/'.product/config.yaml';data=yaml.safe_load(config.read_text());data['extensions']['prodshape']['citations']['consumer-roots']=['consumers'];config.write_text(yaml.safe_dump(data,sort_keys=False))
        (self.repo/'.gitignore').write_text('.product/generated/\n.product/cache/\n')
        self.semantics={'footprint':1,'lead_days':60,'trusted_issuers':[0], 'expire_requested':False,'example':{'capacity':1,'next_used':1}}

    def git(self,*args):
        env={**os.environ,'GIT_AUTHOR_NAME':'Synthetic research fixture','GIT_AUTHOR_EMAIL':'research@example.invalid','GIT_COMMITTER_NAME':'Synthetic research fixture','GIT_COMMITTER_EMAIL':'research@example.invalid','GIT_AUTHOR_DATE':'2026-11-27T00:00:00Z','GIT_COMMITTER_DATE':'2026-11-27T00:00:00Z'}
        return subprocess.check_output(['git',*args],cwd=self.repo,env=env,stderr=subprocess.PIPE).decode().strip()

    def ps(self,name,*args,expected=0,json_output=True):
        command=['node',self.cli,'--serialization-version','v1alpha2']
        if self.current:command+=['--current-evidence',str(self.repo/'current-evidence.json')]
        command+=list(args)
        if json_output:command+=['--format','json']
        result=bounded(name,command,self.logs,cwd=self.repo)
        if expected is not None:assert result.returncode==expected,(name,result.returncode,result.stderr.decode(),result.stdout.decode())
        return json.loads(result.stdout) if json_output else result

    def artifacts(self):
        return {fm(p)['id']:p for p in (self.repo/'docs/product/model').rglob('*.md') if p.name!='README.md'}

    def new_change(self,id,proposed):
        self.ps(id.lower()+'-create','change','create',id)
        d=self.repo/'docs/product/changes/active'/id.lower();p=d/'change.md'
        for artifact,content in proposed.items():
            existing=self.artifacts().get(artifact);name=existing.name if existing else artifact.lower()+'.md'
            (d/'proposed'/name).write_bytes(content)
        def transform(data,body):
            data['operations']={'add':[i for i in proposed if i not in self.artifacts()], 'modify':[i for i in proposed if i in self.artifacts()],'remove':[]};data['unaffected']=[]
            body=body.replace('What is wrong or missing in the current Product Definition? State the problem, not the solution.','Public synthetic research fixture: '+id+'. Not human-accepted product policy.').replace('What the Product Definition says once this change is accepted. Describe the destination, not the steps.','Exercise explicit draft intent and formal interpretation in an isolated test repository.').replace('How a human recognises that the accepted definition expresses the intended outcome.','Synthetic approval state for execution testing only; no claim of human review or real-product acceptance.')
            return data,body
        amend(p,transform);return d

    def snapshot(self):
        return {str(p.relative_to(self.repo)):digest(p) for p in (self.repo/'docs/product').rglob('*') if p.is_file()}

    def approve_fixture(self,d,reason):
        """Synthetic gate input, not an invented human decision; all reasons are public test data."""
        report=self.ps(d.name+'-overlay','change','validate',fm(d/'change.md')['id'])
        assert not report['summary']['errors']
        art=self.artifacts();proposed={fm(p)['id']:p for p in (d/'proposed').glob('*.md')}
        causes=[x for x in report['diagnostics'] if x['code']=='PRODUCT029']
        ledger=[{'id':x['artifact'],'cause':x['target'],'relationship':x['field'],'digest':digest(art[x['artifact']]),'cause-digest':digest(proposed[x['target']]),'reason':reason} for x in causes]
        amend(d/'change.md',lambda data,body:({**data,'status':'approved','unaffected':ledger},body))
        verified=self.ps(d.name+'-acknowledged','change','validate',fm(d/'change.md')['id'])
        assert not verified['summary']['errors'] and not any(x['code']=='PRODUCT029' for x in verified['diagnostics'])
        return causes

    def formal(self,label,artifacts,semantics):
        run_revision=self.git('rev-parse','HEAD') if (self.repo/'.git/HEAD').exists() else None
        model=encode(artifacts,semantics);directory=self.out/'formal'/label;directory.mkdir(parents=True)
        path=directory/'model.smt2';path.write_text(model)
        (directory/'semantic-inputs.json').write_text(json.dumps({'role':'handwritten experimental interpretation, not canonical PDaC fields','values':semantics,'source_pins':{i:digest(p) for i,p in artifacts.items()},'formal_dependencies':DEPENDENCIES,'actual_run_revision':run_revision,'dirty_workspace':bool(self.git('status','--porcelain'))}},indent=2)+'\n')
        data={}
        for solver,path_bin,flags in [('z3',self.tools/'Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3',[]),('cvc5',self.tools/'cvc5/cvc5-Linux-x86_64-static/bin/cvc5',['--incremental'])]:
            key=fingerprint(model,hashlib.sha256(path_bin.read_bytes()).hexdigest())
            prior=self.cache.get((solver,key));full=bounded(label+'-'+solver,[str(path_bin),*flags,str(path)],self.logs,cwd=self.repo)
            observed=statuses(full.stdout);assert full.returncode==0 and observed==EXPECTED,(label,solver,observed)
            if prior:assert prior['statuses']==observed
            data[solver]={'statuses':observed,'cache_hit':bool(prior),'cache_source':prior['label'] if prior else None,'fingerprint':key,'full_recheck_seconds':json.loads((self.logs/f'{label}-{solver}.json').read_text())['wall_seconds']}
            self.cache[(solver,key)]={'label':label,'statuses':observed}
        assert data['z3']['statuses']==data['cvc5']['statuses']
        data['run_revision']=run_revision
        return data

    def evidence(self,label):
        art=self.artifacts();revision=self.git('rev-parse','HEAD')
        record={'format':'pdac-verification-evidence/v1alpha1','provider':'pdac-v040-external-smt-exploration','run-id':label,'revision':revision,'results':[{'test-id':'booking/conditional-invariant','level':'domain','outcome':'passed','citations':[{'id':'SB-A','digest':digest(art['SB-A'])}]},{'test-id':'authorization/encoded-policy','level':'domain','outcome':'passed','citations':[{'id':'SB-AUTH','digest':digest(art['SB-AUTH'])}]}]}
        history=self.repo/'evidence/history';history.mkdir(parents=True,exist_ok=True)
        (history/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        # A new run document is emitted after full recheck; old documents/pins are never edited.
        shutil.copyfile(history/(label+'.json'),self.repo/'current-evidence.json');self.current=True
        return self.ps(label+'-new-evidence','evidence','verify','current-evidence.json')

    def initialize(self):
        proposed={fm(p)['id']:p.read_bytes() for p in (HERE/'fixture').glob('*.md')}
        d=self.new_change('CHG-INITIAL',proposed)
        before=self.snapshot()
        rejected=self.ps('initial-draft-blocked','change','apply','CHG-INITIAL',expected=None)
        assert rejected.get('applied') is False and self.snapshot()==before
        self.approve_fixture(d,'Synthetic initialization: no existing neighbors; fixtures only.')
        before=self.snapshot();self.ps('initial-dry','change','apply','CHG-INITIAL','--dry-run');assert self.snapshot()==before
        self.ps('initial-apply','change','apply','CHG-INITIAL')
        self.ps('baseline-validation','validate')
        consumers=self.repo/'consumers';consumers.mkdir()
        art=self.artifacts()
        for name,ids in [('proof-contract',['UC-A','SB-A','SB-AUTH']),('rule-contract',['BR-A'])]:
            content='# Experimental consumer\n\n'
            for id in ids:
                result=self.ps('cite-'+name+'-'+id.lower(),'cite','--id',id,'--file',str(art[id]),json_output=False)
                content+='<!-- '+result.stdout.decode().strip()+' -->\n'
            (consumers/(name+'.md')).write_text(content)
        self.git('add','.');self.git('commit','-qm','Synthetic baseline accepted only inside experiment')
        checks=self.formal('baseline',self.artifacts(),self.semantics)
        ev=self.evidence('baseline');citations=self.ps('baseline-citations','citations','verify','consumers')
        self.git('add','.');self.git('commit','-qm','Record actual baseline formal run and citations')
        self.rows.append({'stage':'baseline','revision':self.git('rev-parse','HEAD'),'formal':checks,'evidence':ev,'citations':citations})

    def stage(self,label,id,proposed,semantics,reason):
        old_art=self.artifacts();old_pins={i:digest(p) for i,p in old_art.items()};old_model=encode(old_art,self.semantics)
        d=self.new_change(id,proposed);overlay={**old_art,**{fm(p)['id']:p for p in (d/'proposed').glob('*.md')}}
        validation=self.ps(label+'-draft-overlay','change','validate',id)
        assert not validation['summary']['errors']
        causes=[x for x in validation['diagnostics'] if x['code']=='PRODUCT029']
        if causes:
            amend(d/'change.md',lambda data,body:({**data,'status':'approved'},body))
            before=self.snapshot();blocked=self.ps(label+'-unaccounted-blocked','change','apply',id,expected=None)
            assert blocked.get('applied') is False and any(x['code']=='PRODUCT034' for x in blocked['diagnostics']) and self.snapshot()==before
        # Checks run on actual proposed artifacts before applying them.
        checks=self.formal(label+'-overlay',overlay,semantics)
        computed_causes=self.approve_fixture(d,reason)
        before=self.snapshot();forecast=self.ps(label+'-forecast','change','apply',id,'--dry-run');assert before==self.snapshot()
        applied=self.ps(label+'-apply','change','apply',id)
        assert forecast['affectedCitations']==applied['affectedCitations']
        self.ps(label+'-validation','validate')
        old_evidence=self.ps(label+'-old-evidence','evidence','verify','current-evidence.json',expected=None)
        citation_status=self.ps(label+'-citations','citations','verify','consumers',expected=None)
        art=self.artifacts();changed=[i for i,p in art.items() if old_pins.get(i)!=digest(p)]
        self.git('add','.');self.git('commit','-qm','Apply synthetic '+id+' through ProductShape')
        accepted_checks=self.formal(label+'-accepted',art,semantics)
        assert all(checks[s]['fingerprint']==accepted_checks[s]['fingerprint'] and checks[s]['statuses']==accepted_checks[s]['statuses'] for s in ['z3','cvc5'])
        # Core apply must not rewrite old provider outcomes or pins.
        prior=json.loads((self.repo/'current-evidence.json').read_text());assert all(r['outcome']=='passed' for r in prior['results'])
        new_evidence=self.evidence(label)
        self.git('add','.');self.git('commit','-qm','Record new full formal recheck '+label)
        self.rows.append({'stage':label,'change':id,'revision':self.git('rev-parse','HEAD'),'changed':changed,'one_hop_causes':computed_causes,'direct_uc_changed':old_pins['UC-A']!=digest(art['UC-A']),'model_changed':old_model!=encode(art,semantics),'formal':checks,'post_apply_full_recheck':accepted_checks,'changed_declared_formal_dependencies':{prop:[i for i in ids if i in changed] for prop,ids in DEPENDENCIES.items()},'forecast':forecast['affectedCitations'],'evidence_before_new_run':old_evidence,'citations_before_new_run':citation_status,'new_evidence':new_evidence,'synthetic_review_reason':reason})
        self.semantics=semantics

    def applicability_probes(self):
        # Retired contracts are checked against newly declared policy, not silently reused.
        snippets={
          'old-lead-contract':'(declare-const day Int)\n(assert (and (> day 30) (<= day 60)))\n(check-sat)\n(get-value (day))',
          'old-issuer-contract':'(declare-const issuer Int)\n(assert (and (or (= issuer 0) (= issuer 1)) (not (= issuer 0))))\n(check-sat)\n(get-value (issuer))',
          'old-footprint-contract':'(declare-const cap Int)\n(declare-const used Int)\n(assert (and (> cap 0) (>= used 0) (<= (+ used 1) cap) (> (+ used 2) cap)))\n(check-sat)\n(get-value (cap used))'}
        rows={}
        for name,body in snippets.items():
            path=self.out/'formal'/(name+'.smt2');path.write_text('(set-logic QF_LIA)\n(set-option :produce-models true)\n'+body+'\n')
            result=bounded(name,[str(self.tools/'Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3'),str(path)],self.logs,cwd=self.repo)
            assert result.returncode==0 and statuses(result.stdout)==['sat']
            rows[name]={'status':'sat','raw_output':str((self.logs/(name+'.stdout')).relative_to(self.out))}
        # Negative control: a new semantic edit with no reviewed encoding/binding revision.
        artifacts=self.artifacts();candidate=artifacts['TERM-A'].read_text().replace('two indivisible room slots','three indivisible room slots')
        assert candidate!=artifacts['TERM-A'].read_text()
        d=self.new_change('CHG-UNMAPPED',{'TERM-A':candidate.encode()})
        report=self.ps('unmapped-structural-validation','change','validate','CHG-UNMAPPED');assert not report['summary']['errors']
        overlay={**artifacts,'TERM-A':d/'proposed'/artifacts['TERM-A'].name}
        old_bytes=encode(artifacts,self.semantics);unchanged_encoding=encode(overlay,self.semantics)
        assert old_bytes==unchanged_encoding and digest(artifacts['TERM-A'])!=digest(overlay['TERM-A'])
        check=self.formal('unmapped-old-encoding',overlay,self.semantics)
        assert all(check[s]['cache_hit'] for s in ['z3','cvc5'])
        rows['unmapped-intent']={'productshape_errors':report['summary']['errors'],'unchanged_formula_still_verifies':True,'formal_dependency_pin_changed':True,'current_intent_applicability':'not established; explicit semantic review/binding update required','published_new_evidence':False,'applied':False}
        amend(d/'change.md',lambda data,body:({**data,'status':'rejected'},body))
        self.ps('unmapped-archive','change','archive','CHG-UNMAPPED')
        self.git('add','.');self.git('commit','-qm','Retain unapproved unmodeled semantic edit as a negative control')
        return rows

    def negative_proposal(self):
        art=self.artifacts();text=art['BR-A'].read_text()+'\nResearch negative control: the same lead time must also be at least 61 days.\n'
        d=self.new_change('CHG-CONTRADICTION',{'BR-A':text.encode()})
        result=self.ps('contradiction-structural-validation','change','validate','CHG-CONTRADICTION');assert not result['summary']['errors']
        file=self.out/'formal/contradiction.smt2';file.write_text('(set-logic QF_LIA)\n(declare-const days Int)\n(assert (<= days 60))\n(assert (>= days 61))\n(check-sat)\n')
        r=bounded('contradiction-formal',[str(self.tools/'Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3'),str(file)],self.logs,cwd=self.repo);assert statuses(r.stdout)==['unsat']
        amend(d/'change.md',lambda data,body:({**data,'status':'rejected'},body))
        self.ps('contradiction-archive','change','archive','CHG-CONTRADICTION')
        self.git('add','.');self.git('commit','-qm','Retain rejected contradictory proposal and structural/formal distinction')
        return {'productshape_errors':result['summary']['errors'],'formal_consistency':'unsat','applied':False}


def main(package,tools,output):
    e=Experiment(output,package,tools);e.initialize();negative=e.negative_proposal()
    def current(id):return e.artifacts()[id].read_text()
    sem=copy.deepcopy(e.semantics);sem['lead_days']=30
    e.stage('rule','CHG-LEAD',{'BR-A':current('BR-A').replace('at most 60 days','at most 30 days').encode()},sem,'Synthetic review: generic Use Case/Lifecycle refer to the rule; SB day 30 remains the inclusive boundary.')
    sem=copy.deepcopy(e.semantics);sem['trusted_issuers']=[0,1]
    e.stage('identity','CHG-ISSUERS',{'TERM-IDENTITY':current('TERM-IDENTITY').replace('Only issuer A is trusted.','Issuers A and B are trusted.').encode()},sem,'Synthetic review: existing rule/Use Case use the declared trusted-issuer set; issuer-A example remains valid but does not enumerate that set.')
    sem=copy.deepcopy(e.semantics);sem['expire_requested']=True
    a=e.artifacts()['LC-A'];_,front,body=a.read_text().split('---',2);data=yaml.safe_load(front)
    next(t for t in data['transitions'] if t['id']=='EXPIRE')['from']=['REQUESTED','CONFIRMED']
    body=body.replace('CANCEL and EXPIRE each require CONFIRMED and release that footprint.','CANCEL requires CONFIRMED and releases that footprint. EXPIRE also accepts REQUESTED without releasing capacity; CONFIRMED expiry releases the footprint.')
    e.stage('lifecycle','CHG-EXPIRY',{'LC-A':('---\n'+yaml.safe_dump(data,sort_keys=False)+'---'+body).encode()},sem,'Synthetic review: existing confirmation example is unchanged; the additional REQUESTED expiry path is checked separately by the external model.')
    sem=copy.deepcopy(e.semantics);sem['footprint']=2;sem['example']={'capacity':2,'next_used':2}
    term=current('TERM-A').replace('one indivisible room slot','two indivisible room slots')
    sb=current('SB-A').replace('Capacity is 1','Capacity is 2').replace('used slots are 1','used slots are 2')
    e.stage('domain','CHG-FOOTPRINT',{'TERM-A':term.encode(),'SB-A':sb.encode()},sem,'Synthetic review: generic footprint references remain applicable; the concrete SB is explicitly changed to capacity/usage 2. External formal interpretation is revised, not inferred from prose.')
    e.stage('unrelated','CHG-RETENTION',{'BR-UNRELATED':current('BR-UNRELATED').replace('7 days','14 days').encode()},copy.deepcopy(e.semantics),'Synthetic review: report retention is outside all declared booking/identity formal dependencies.')
    e.stage('editorial','CHG-EDITORIAL',{'SB-A':(current('SB-A')+'\n<!-- Editorial wording note; scenario values are unchanged. -->\n').encode()},copy.deepcopy(e.semantics),'Synthetic review: no structured scenario value or external formula changes; whole-artifact citation freshness still changes.')
    assert all(row['formal'][s]['cache_hit'] for row in e.rows if row['stage'] in ['unrelated','editorial'] for s in ['z3','cvc5'])
    applicability=e.applicability_probes()
    e.git('bundle','create',str(output/'history.bundle'),'--all')
    manifest={'status':'public non-scored exploratory integration; synthetic approval fixtures, not human product acceptance','pdac_method':'0.3.0','serialization':'v1alpha2','productshape':'0.26.1','source_main':'39b5e05547cf8f9f12a1f962d25b854837f4f779','stages':e.rows,'negative_proposal':negative,'retired_contract_and_unmapped_intent_probes':applicability,'llm_calls_by_runner':0,'automatic_retries':0,'limitations':['Handwritten semantic inputs; no generic prose translator or completeness guarantee.','Synthetic fixture approvals/acknowledgments exercise CLI gates; not human review.','Whole-model cache checked against full reruns; not an optimized incremental prover.','No four-cohort scoring, independent session comparison, H0 effect or normative extension.']}
    (output/'run-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Actual ProductShape changes and formal rechecks complete.',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--productshape',type=Path,required=True);p.add_argument('--tools',type=Path,required=True);p.add_argument('output',type=Path);a=p.parse_args();main(a.productshape.resolve(),a.tools.resolve(),a.output.resolve())
