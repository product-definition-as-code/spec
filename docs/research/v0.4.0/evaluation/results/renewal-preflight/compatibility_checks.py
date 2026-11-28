import sys,subprocess,json,datetime
from pathlib import Path
sys.path.insert(0,'/tmp/pdac-v040-renewal/spec/docs/research/v0.4.0/experiments')
from run import run
root=Path('/tmp/pdac-v040-renewal');work=root/'public-work';work.mkdir();(work/'home').mkdir();(work/'input.txt').write_text('PUBLIC_CANARY')
# Existing local image only; read-only public binaries. No auth, network, private data or Docker socket inside.
image='eclipse-temurin:21-jdk-noble'
meta=json.loads(subprocess.check_output(['docker','image','inspect',image]))[0]
(root/'docker-image.json').write_text(json.dumps({k:meta[k] for k in ('Id','RepoDigests')},indent=2)+'\n')
command=['docker','run','--rm','--pull=never','--name','pdac-v040-public-canary','--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges:true','--pids-limit=64','--memory=2g','--memory-swap=2g','--user=1000:1000','--tmpfs=/tmp:rw,nosuid,nodev,size=64m','--workdir=/work','-v',str(work)+':/work:rw','-v','/usr:/usr:ro','-v','/lib:/lib:ro','-v','/lib64:/lib64:ro','--env','TMPDIR=/tmp','--env','HOME=/work/home',image,'codex','sandbox','-c','sandbox_mode="workspace-write"','--','python3','-c','from pathlib import Path; assert Path("input.txt").read_text()=="PUBLIC_CANARY"; Path("output.txt").write_text("PUBLIC_WRITE"); print("TOOL_TRANSPORT_OK")']
r=run('default-docker-transport',command,root/'check-2-docker',cwd=work)
subprocess.run(['docker','rm','-f','pdac-v040-public-canary'],capture_output=True)
print(r.stderr.decode()[-1600:])
