"""Deterministic full tool-transport canary; no model call, benchmark or private input."""
import argparse,json,sys,tempfile
from pathlib import Path
from isolation import namespace
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'experiments'))
from run import run


def preflight(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='pdac-transport-canary-') as folder:
        work=Path(folder);(work/'home').mkdir();(work/'input.txt').write_text('PUBLIC_CANARY')
        code='from pathlib import Path; import os; assert os.environ["TMPDIR"]=="/tmp"; assert not Path("/home/juan").exists(); assert Path("input.txt").read_text()=="PUBLIC_CANARY"; Path("output.txt").write_text("PUBLIC_WRITE"); print("TOOL_TRANSPORT_OK")'
        command=['codex','sandbox','-c','sandbox_mode="workspace-write"','--','python3','-c',code]
        result=run('full-tool-transport',namespace(work,command,network=False),output,cwd=work)
        record={'returncode':result.returncode,'passed':result.returncode==0 and result.stdout.strip()==b'TOOL_TRANSPORT_OK' and (work/'output.txt').exists(),'model_calls':0,'benchmark_cases':0,'automatic_retries':0,'fallback_or_security_relaxation':False,'purpose':'same nested tool sandbox, public read/write only; failed transport blocks preparation'}
        (output/'preflight.json').write_text(json.dumps(record,indent=2)+'\n')
        return record

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args();raise SystemExit(0 if preflight(a.output)['passed'] else 1)
