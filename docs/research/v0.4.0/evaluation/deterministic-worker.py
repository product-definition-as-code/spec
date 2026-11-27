#!/usr/bin/env python3
"""Runs only inside the scorer's empty-root, no-network sandbox."""
import json
import runpy
import sys

cases = json.load(sys.stdin)
try:
    decide = runpy.run_path('/submission/decision.py')['decide']
except BaseException as error:
    print(json.dumps({'startup_error': type(error).__name__}))
    raise SystemExit(0)
results = []
for case in cases:
    try:
        output = json.loads(json.dumps(decide(case['input']), allow_nan=False))
        results.append({'id': case['id'], 'output': output})
    except BaseException as error:
        results.append({'id': case['id'], 'error': type(error).__name__})
print(json.dumps({'results': results}, allow_nan=False))
