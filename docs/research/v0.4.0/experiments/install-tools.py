#!/usr/bin/env python3
"""Fetch pinned public distributions into an explicit local directory; no global installs."""
import argparse, hashlib, json, urllib.request, zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ALLOY_OBSERVED_SHA256='6b8c1cb5bc93bedfc7c61435c4e1ab6e688a242dc702a394628d9a9801edb78d'
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();root=a.directory.resolve();root.mkdir(parents=True,exist_ok=True)
for tool in json.loads((HERE/'../calibration/tool-candidates.json').read_text())['tools']:
    asset=tool['assets'][0];path=root/asset['name']
    if not path.exists():
        # Network timeout, one download attempt; interruptions are visible failures.
        with urllib.request.urlopen(asset['url'],timeout=60) as src,path.open('xb') as dst:
            while data:=src.read(1024*1024):dst.write(data)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    expected=asset['digest'].removeprefix('sha256:') if asset['digest'] else ALLOY_OBSERVED_SHA256
    if actual!=expected:raise SystemExit('Digest mismatch: '+asset['name'])
    if path.suffix=='.zip':
        target=root/tool['repository'].split('/')[0];target.mkdir(exist_ok=True)
        with zipfile.ZipFile(path) as archive:
            for entry in archive.infolist():
                dest=(target/entry.filename).resolve()
                if not dest.is_relative_to(target):raise SystemExit('Unsafe archive path')
                archive.extract(entry,target)
                if (entry.external_attr>>16)&0o111:dest.chmod(dest.stat().st_mode|0o111)
    print(asset['name'],actual)
