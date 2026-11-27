#!/usr/bin/env python3
"""Validate draft schemas, expected solver verdicts and concrete arithmetic witnesses."""
import hashlib, json, re
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from run import HERE

ROOT=HERE.parents[3]

def validate(output):
    schemas=[json.loads(p.read_text()) for p in (ROOT/'schemas/v1alpha2').glob('*.json')]
    registry=Registry().with_resources((s['$id'],Resource.from_contents(s)) for s in schemas)
    validators={s['$id'].split(':')[-2]:Draft202012Validator(s,registry=registry) for s in schemas}
    count=0
    for p in list((HERE/'intent').glob('*.md'))+list((output/'evolution').rglob('*.md')):
        data=yaml.safe_load(p.read_text().split('---',2)[1]);validators[data['type']].validate(data);count+=1
    cases=json.loads((HERE/'expectations.json').read_text())
    expected=[c['expected'] for c in cases]
    checks={
      'weak-contract-counterexample':lambda v:v['used']<v['capacity']<v['nextUsed'],
      'structured-behaviour-baseline':lambda v:(v['used'],v['capacity'],v['days'],v['nextUsed'],v['nextState'])==(0,1,30,1,1),
      'structured-behaviour-survives-guard-mutant':lambda v:(v['used'],v['capacity'],v['days'],v['nextUsed'],v['nextState'])==(0,1,30,1,1),
      'guard-mutant-overbooks':lambda v:0<=v['used']<=v['capacity'] and v['nextUsed']==v['used']+1>v['capacity'] and v['nextState']==1,
      'missing-frame-changes-owner':lambda v:v['nextOwner']!=v['owner'] and v['nextState']==1,
      'double-release-mutant':lambda v:v['nextUsed']==v['used']-2<0 and v['nextState']==3,
      'lead-rule-change-breaks-old-contract':lambda v:30<v['days']<=60,
      'hours-conversion-counterexample':lambda v:60<v['days']<=1440}
    verified=0
    for solver in ['z3','cvc5']:
        text=(output/f'{solver}-booking-v3.stdout').read_text()
        statuses=[l for l in text.splitlines() if l in ['sat','unsat','unknown']];assert statuses==expected
        for i,c in enumerate(cases):
            if c['id'] not in checks:continue
            start=text.index(c['id'])+len(c['id']);end=text.index(cases[i+1]['id'],start) if i+1<len(cases) else len(text)
            values={k:int(n) if n else -int(neg) for k,n,neg in re.findall(r'\((\w+)\s+(?:(-?\d+)|\(-\s+(\d+)\))\)',text[start:end])}
            assert checks[c['id']](values),(solver,c['id'],values);verified+=1
    assert 'unknown' in (output/'z3-inconclusive.stdout').read_text()
    assert '2 verified, 1 error' in (output/'dafny-booking-pinned.stdout').read_text()
    assert '1 verified, 1 error' in (output/'dafny-feasibility.stdout').read_text()
    for s in ['z3','cvc5']:
        txt=(output/f'{s}-feasibility.stdout').read_text();assert [l for l in txt.splitlines() if l in ['sat','unsat']]==['sat','unsat']
    receipt=json.loads((output/'alloy-instance/receipt.json').read_text());assert receipt['commands']['Acyclic']['solution']
    # Check the returned finite relation really contains a cycle, without invoking an LLM.
    solution=json.loads((output/'alloy-instance/Acyclic-solution-0.json').read_text())
    values=receipt['commands']['Acyclic']['solution'][0]['instances'][0]['values']
    edges={k:[a[0] for a in v.get('next',[])] for k,v in values.items() if k.startswith('Node$')}
    def reaches(start,node,seen):
        return any(n==start or (n not in seen and reaches(start,n,seen|{n})) for n in edges[node])
    assert any(reaches(n,n,{n}) for n in edges)
    print(f'{count} draft artifact/proposal frontmatters schema-valid; 34 matched SMT verdicts; {verified} concrete arithmetic witnesses and Alloy cycle checked. No full Product Change conformance/apply claim.')

if __name__=='__main__':
    import sys
    validate(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE/'results')
