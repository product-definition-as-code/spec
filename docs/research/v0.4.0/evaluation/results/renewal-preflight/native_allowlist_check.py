import json,sys
from pathlib import Path
sys.path.insert(0,'/tmp/pdac-v040-renewal/spec/docs/research/v0.4.0/experiments');from run import run
root=Path('/tmp/pdac-v040-renewal');work=root/'public-work';secret=root/'outside-public-sentinel';secret.write_text('PUBLIC_SENTINEL_DO_NOT_EXPOSE')
(work/'escape').symlink_to(secret)
profile=['-c','default_permissions="pdac"','-c','permissions.pdac.filesystem={":minimal"="read",'+json.dumps(str(work))+'="write"}','-c','permissions.pdac.network.enabled=false']
code='''from pathlib import Path
import socket,os,json
assert Path('input.txt').read_text()=='PUBLIC_CANARY'
Path('allowlist-output.txt').write_text('PUBLIC_WRITE')
blocked=[]
for p in %r:
 try: Path(p).read_bytes()
 except (PermissionError,FileNotFoundError,OSError): blocked.append(p)
 else: raise AssertionError('unexpected readable path: '+p)
for family,addr in [(socket.AF_INET,('1.1.1.1',443)),(socket.AF_INET,('127.0.0.1',22))]:
 try:
  s=socket.socket(family);s.settimeout(.2);s.connect(addr)
 except OSError:pass
 else:raise AssertionError('network unexpectedly allowed')
print(json.dumps({'passed':True,'blocked_count':len(blocked),'public_write':True,'network_denied':True}))
''' % [str(secret),str(work/'escape'),'/home/juan/.codex/auth.json','/home/juan/.local/share/pdac-v040-evaluation/g1-custody/cases.json','/srv/repos/product-definition-as-code/spec/README.md']
r=run('native-allowlist-transport',['env','TMPDIR=/tmp','codex','sandbox',*profile,'--','python3','-c',code],root/'check-4-native-allowlist',cwd=work)
print(r.stdout.decode(),r.stderr.decode()[-1300:])
