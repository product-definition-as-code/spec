"""Explicit baseline migration; prints a plan unless --write is supplied."""
from pathlib import Path
import argparse
import re
import yaml


def migrate_documents(documents):
    parsed = {}
    identities = {}
    for path, text in documents.items():
        match = re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        if not match: continue
        data = yaml.safe_load(match[1])
        if not isinstance(data, dict) or 'id' not in data: continue
        if data['id'] in identities: raise ValueError(f'duplicate identity: {data["id"]}')
        identities[data['id']] = path
        parsed[path] = (data, match.end())
    additions = {}
    updates = {}
    for path, (data, _) in parsed.items():
        if data.get('type') != 'business-rule': continue
        targets = data.get('applies-to', [])
        removed = [id for id in targets if id.startswith('UC-')]
        if not removed: continue
        for id in removed:
            target = identities.get(id)
            if target is None or parsed[target][0].get('type') != 'use-case':
                raise ValueError(f'{data["id"]}: unresolved or wrong-type Use Case {id}')
            additions.setdefault(target, set()).add(data['id'])
        data = {**data}
        retained = [id for id in targets if id not in removed]
        if retained: data['applies-to'] = retained
        else: del data['applies-to']
        updates[path] = data
    for path, rules in additions.items():
        data = {**parsed[path][0]}
        existing = list(dict.fromkeys(data.get('governed-by', [])))
        data['governed-by'] = existing + sorted(rules - set(existing))
        updates[path] = data
    return {path: '---\n' + yaml.safe_dump(data, sort_keys=False, width=1000) + '---\n' + documents[path][parsed[path][1]:] for path, data in updates.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path, help='explicit baseline model directory')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    model = args.model.resolve(strict=True)
    if not model.is_dir(): parser.error('model must be a directory')
    documents = {}
    for path in sorted(model.rglob('*.md')):
        if path.is_symlink() or not path.resolve().is_relative_to(model): parser.error('model contains a path outside its root')
        documents[path] = path.read_text(encoding='utf-8')
    try: changes = migrate_documents(documents)
    except (ValueError, yaml.YAMLError) as error: parser.error(str(error))
    for path in changes: print(path.relative_to(model).as_posix())
    if args.write:
        written = []
        try:
            for path, text in changes.items():
                written.append(path)
                path.write_text(text, encoding='utf-8', newline='\n')
        except OSError:
            for path in written: path.write_text(documents[path], encoding='utf-8', newline='\n')
            raise
    print(f'{len(changes)} file(s) {"migrated" if args.write else "planned"}. Review live overlays and configuration separately; archives and consumer pins are not rewritten.')


if __name__ == '__main__': main()
