"""Small allow-list mount namespace for fresh author sessions; no repository/held-out mounts."""
import os
from pathlib import Path

def namespace(work, command, auth=None, tools=None, network=True):
    work=Path(work).resolve()
    args=['bwrap','--die-with-parent','--unshare-pid','--unshare-ipc','--unshare-uts','--new-session']
    if not network:args+=['--unshare-net']
    for path in ['/usr','/bin','/lib','/lib64']:
        if Path(path).exists():args+=['--ro-bind',path,path]
    args+=['--dir','/etc','--dir','/etc/ssl']
    for path in ['/etc/ssl/certs','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf','/etc/passwd','/etc/group']:
        if Path(path).exists():args+=['--ro-bind',path,path]
    args+=['--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/home','--dir','/srv','--dir','/run','--bind',str(work),'/work','--chdir','/work']
    if auth:args+=['--bind',str(Path(auth).resolve()),'/codex','--setenv','CODEX_HOME','/codex']
    if tools:
        for name,path in tools.items():args+=['--ro-bind',str(Path(path).resolve()),'/tools/'+name]
    args+=['--setenv','HOME','/work/home','--setenv','PATH','/work/bin:/usr/local/bin:/usr/bin:/bin','--',*command]
    return args

def environment():
    # Never inherit API keys, connector credentials, host CODEX_HOME or user configuration.
    return {'PATH':'/usr/local/bin:/usr/bin:/bin','HOME':str(Path.home()),'LANG':'C.UTF-8','XDG_RUNTIME_DIR':os.environ.get('XDG_RUNTIME_DIR',f'/run/user/{os.getuid()}')}
