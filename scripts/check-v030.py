"""Check schema closure and fixture integrity, not implementation conformance."""
from pathlib import Path
import hashlib
import json
import re
import sys
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n').replace(b'\r', b'\n')).hexdigest()

def frontmatter(path):
    raw = path.read_text(encoding='utf-8', errors='replace')
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', raw, re.S)
    return yaml.safe_load(match[1]) if match else None

def pointer(parts):
    return ''.join('/' + str(p).replace('~', '~0').replace('/', '~1') for p in parts)

def error_paths(error):
    if error.validator == 'required':
        return [pointer([*error.absolute_path, k]) for k in error.validator_value if k not in error.instance]
    if error.validator == 'additionalProperties':
        return [pointer([*error.absolute_path, k]) for k in error.instance if k not in error.schema.get('properties', {})]
    if error.validator == 'oneOf':
        # Discard branches with incompatible discriminating fields. Union shape errors
        # remain at the union instance when no one branch can be selected.
        compatible = []
        for i, branch in enumerate(error.schema['oneOf']):
            if '$ref' in branch:
                continue
            if all(not ('const' in rule and key in error.instance and error.instance[key] != rule['const']) for key, rule in branch.get('properties', {}).items()) and set(branch.get('required', [])) <= set(error.instance):
                compatible.append(i)
        if len(compatible) == 1:
            return [p for e in error.context if list(e.schema_path)[0] == compatible[0] for p in error_paths(e)]
    return [pointer(error.absolute_path)]

def main():
    failures = []
    schemas = {p.stem.removesuffix('.schema'): load(p) for p in (ROOT / 'schemas/v1alpha2').glob('*.json')}
    registry = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in schemas.values())
    ids = {s['$id'] for s in schemas.values()}
    for name, schema in schemas.items():
        Draft202012Validator.check_schema(schema)
        def visit(node):
            if isinstance(node, dict):
                if '$ref' in node:
                    ref = node['$ref']
                    if not ref.startswith('#') and ref.split('#')[0] not in ids:
                        failures.append(f'{name}: unclosed reference {ref}')
                    registry.resolver(schema['$id']).lookup(ref)
                for value in node.values(): visit(value)
            elif isinstance(node, list):
                for value in node: visit(value)
        visit(schema)
    validators = {n: Draft202012Validator(s, registry=registry) for n, s in schemas.items()}
    checked = pins = 0
    for case in sorted((ROOT / 'conformance/cases').iterdir()):
        if not (case / 'expected.json').exists(): continue
        expected = load(case / 'expected.json')
        ds = expected['diagnostics']
        # Older negative fixtures intentionally combine schema and semantic failures.
        # Their semantic precedence is tested by an implementation, not this audit.
        is_new = case.name.startswith(('lifecycle-', 'evidence-', 'impact-', 'forecast-', 'rule-use-case-'))
        if not is_new: continue
        checked += 1
        artifacts = {}
        for p in (case / 'repo/docs/product/model').glob('**/*.md'):
            data = frontmatter(p)
            if data: artifacts[data['id']] = p
        for p in (case / 'repo').rglob('*.md'):
            if '/changes/completed/' in p.as_posix(): continue
            data = frontmatter(p)
            if not data: continue
            if expected.get('history') and re.fullmatch(r'\{\{revision:\d+\}\}', str(data.get('base-revision', ''))):
                # The runner resolves this controlled fixture token before invocation.
                index = int(data['base-revision'][11:-2])
                if index >= len(expected['history']): failures.append(f'{case.name}: undeclared revision placeholder')
                data['base-revision'] = '1' * 40
            validator = validators.get(data.get('type'))
            if not validator: failures.append(f'{case.name}/{p.name}: missing schema'); continue
            found = {v for error in validator.iter_errors(data) for v in error_paths(error)}
            source = p.relative_to(case / 'repo').as_posix()
            wanted = {d['field'] for d in ds if d['code'] == 'PRODUCT002' and d['file'] == source}
            if found != wanted: failures.append(f'{case.name}/{source}: schema paths {sorted(found)} != {sorted(wanted)}')
            if data.get('type') == 'product-change':
                for n, entry in enumerate(data.get('unaffected', []), 1):
                    for key, idkey in [('digest', 'id'), ('cause-digest', 'cause')]:
                        if key not in entry: continue
                        id = entry[idkey]
                        target = artifacts.get(id)
                        if key == 'cause-digest' and id not in data['operations']['remove']:
                            target = next((f for f in p.parent.glob('proposed/**/*.md') if frontmatter(f).get('id') == id), None)
                        intentional = any(d['code'] in ['PRODUCT002', 'PRODUCT033'] and (d['field'] == f'unaffected[{n}]' or d['field'].startswith(f'/unaffected/{n-1}/')) for d in ds)
                        if target and digest(target) != entry[key] and not intentional: failures.append(f'{case.name}: incorrect {key} for {id}')
                        pins += 1
        for path in expected.get('evidence', []) + expected.get('currentEvidence', []):
            p = case / 'repo' / path
            try: document = load(p)
            except json.JSONDecodeError:
                if not any(d['code'] == 'PRODUCT080' for d in ds): failures.append(f'{case.name}: unaccounted invalid JSON')
                continue
            found = sorted({v for e in validators['verification-evidence'].iter_errors(document) for v in error_paths(e)})
            malformed = [d for d in ds if d['code'] == 'PRODUCT080']
            if malformed:
                if 'field' in malformed[0] and (not found or found[0] != malformed[0]['field']): failures.append(f'{case.name}: first evidence schema path {found}')
                continue
            if found: failures.append(f'{case.name}: unexpected evidence schema errors {found}'); continue
            for result in document['results']:
                for citation in result['citations']:
                    target = artifacts.get(citation['id'])
                    if target and citation['digest'] != digest(target) and not any(d['code'] in ['PRODUCT061', 'PRODUCT042'] and d.get('target') == citation['id'] for d in ds): failures.append(f'{case.name}: incorrect evidence pin')
                    pins += 1
        report = expected.get('reports', {}).get('affectedCitations')
        for p in (case / 'repo').rglob('*'):
            if not p.is_file() or '/changes/' in p.as_posix() or p.suffix not in ['.md', '.yml']: continue
            text = p.read_text(encoding='utf-8', errors='replace')
            citations = []
            if p.name.endswith('.citations.yml'):
                citations = yaml.safe_load(text).get('citations', [])
            elif p.suffix == '.md':
                citations = [dict(re.findall(r'([a-z-]+)="([^"]*)"', m[1])) for m in re.finditer(r'(?<!/)pdac:cite (id=[^\n]+)', text)]
            for citation in citations:
                target = artifacts.get(citation.get('id'))
                if target is None and expected.get('operation') in ['apply', 'apply-dry-run']:
                    target = next((f for f in (case / 'repo/docs/product/changes/active').glob('*/proposed/**/*.md') if frontmatter(f).get('id') == citation.get('id')), None)
                intentional = any(d['code'] in ['PRODUCT042', 'PRODUCT060', 'PRODUCT061', 'PRODUCT062'] and d.get('target') == citation.get('id') for d in ds)
                if (not target or citation.get('digest') != digest(target)) and not intentional:
                    failures.append(f'{case.name}: incorrect citation pin in {p.name}')
                pins += 1
        if report is not None:
            records = report['records']
            if report['count'] != len(records): failures.append(f'{case.name}: forecast count')
            def key(r): return (r['file'], 1 if 'line' in r else 2 if 'entry' in r else 0, r.get('line', r.get('entry', 0)), r['target'], r.get('anchor', ''), r['status'])
            if sorted(records, key=key) != records: failures.append(f'{case.name}: forecast order')
            for r in records:
                source = case / 'repo' / r['file']
                if not source.exists(): failures.append(f'{case.name}: missing report source {r["file"]}')
                if 'line' in r:
                    text = source.read_text(encoding='utf-8').splitlines()[r['line']-1]
                    if f'pdac:cite id="{r["target"]}"' not in text: failures.append(f'{case.name}: missing actual citation occurrence')
    if not checked or not pins: failures.append('audit exercised no cases or pins')
    for failure in failures: print(f'ERROR {failure}', file=sys.stderr)
    print(f'{len(schemas)} schemas closed; {checked} v0.3 cases checked; {pins} ledger/evidence pins inspected. Implementation semantics are not asserted by this audit.')
    return bool(failures)

if __name__ == '__main__':
    sys.exit(main())
