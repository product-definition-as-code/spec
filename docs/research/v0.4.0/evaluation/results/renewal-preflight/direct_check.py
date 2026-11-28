import sys
from pathlib import Path
sys.path.insert(0,'/tmp/pdac-v040-renewal/spec/docs/research/v0.4.0/experiments')
from run import run
root=Path('/tmp/pdac-v040-renewal');work=root/'public-work'
cmd=['env','TMPDIR=/tmp','codex','sandbox','-c','sandbox_mode="workspace-write"','--','python3','-c','from pathlib import Path; assert Path("input.txt").read_text()=="PUBLIC_CANARY"; Path("direct-output.txt").write_text("PUBLIC_WRITE"); print("TOOL_TRANSPORT_OK")']
r=run('direct-native-transport',cmd,root/'check-3-direct-native',cwd=work)
print(r.stdout.decode(),r.stderr.decode()[-1000:])
