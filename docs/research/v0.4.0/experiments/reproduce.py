#!/usr/bin/env python3
"""Reproduce current exploratory observations without an LLM. Output directory must be new."""
import argparse, json
from pathlib import Path
from run import HERE, run
from evolution import main as evolution
from check import validate
p=argparse.ArgumentParser();p.add_argument('tools',type=Path);p.add_argument('output',type=Path);a=p.parse_args();t=a.tools.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
z=str(t/'Z3Prover/z3-5.3.3-x64-glibc-2.39/bin/z3');c=str(t/'cvc5/cvc5-Linux-x86_64-static/bin/cvc5');d=str(t/'dafny-lang/dafny/dafny');backend=str(t/'dafny-lang/dafny/z3/bin/z3-4.12.1');alloy=str(t/'org.alloytools.alloy.dist.jar')
for name,cmd in [('z3-version',[z,'--version']),('cvc5-version',[c,'--version']),('alloy-version',['java','-Xmx1024m','-jar',alloy,'version']),('dafny-version',[d,'--version']),('dafny-backend-version',[backend,'--version']),('containment',['/bin/sh','-c','p=$(cut -d: -f3 /proc/self/cgroup); cat /proc/self/cgroup; cat /sys/fs/cgroup$p/memory.max /sys/fs/cgroup$p/memory.swap.max /sys/fs/cgroup$p/pids.max'])]:
    assert run(name,cmd,out).returncode==0
jobs=[('z3-feasibility',[z,'models/feasibility.smt2'],0),('cvc5-feasibility',[c,'--incremental','models/feasibility.smt2'],0),('alloy-feasibility',['java','-Xmx1024m','-jar',alloy,'exec','-q','-t','json','-o',str(out/'alloy-instance'),'models/relations.als'],0),('dafny-feasibility',[d,'verify','--cores','1','--solver-path',backend,'--verification-time-limit','20','models/feasibility.dfy'],4),('z3-booking-corrected',[z,'models/booking.smt2'],0),('cvc5-booking-corrected',[c,'--incremental','models/booking.smt2'],0),('z3-inconclusive',[z,'models/inconclusive.smt2'],0),('dafny-booking-pinned',[d,'verify','--cores','1','--solver-path',backend,'--verification-time-limit','20','--extract-counterexample','models/booking.dfy'],4)]
for name,cmd,expected in jobs:
    result=run(name,cmd,out);assert result.returncode==expected,(name,result.returncode)
evolution(z,out/'evolution');validate(out)
inputs={str(f.relative_to(HERE)):__import__('hashlib').sha256(f.read_bytes()).hexdigest() for group in ['models','intent'] for f in (HERE/group).glob('*') if f.is_file()}
(out/'input-manifest.json').write_text(json.dumps(inputs,indent=2)+'\n')
print('All declared observations reproduced; intentional negative and unknown outcomes preserved.')
