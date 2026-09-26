import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cpSync, mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
function check(edit) {
  const temp = mkdtempSync(join(tmpdir(), 'pdac-templates-'));
  try {
    for (const dir of ['schemas', 'templates', 'spec']) cpSync(join(root, dir), join(temp, dir), { recursive: true });
    mkdirSync(join(temp, 'scripts'));
    cpSync(join(root, 'scripts/check-templates.mjs'), join(temp, 'scripts/check-templates.mjs'));
    edit(temp);
    return spawnSync(process.execPath, [join(temp, 'scripts/check-templates.mjs')], { encoding: 'utf8' });
  } finally { rmSync(temp, { recursive: true, force: true }); }
}

test('templates validate from a CRLF checkout', () => {
  const result = check((temp) => {
    for (const dir of ['templates', 'spec']) for (const file of readdirSync(join(temp, dir))) {
      if (!file.endsWith('.md')) continue;
      const path = join(temp, dir, file);
      writeFileSync(path, readFileSync(path, 'utf8').replace(/\r\n?/g, '\n').replace(/\n/g, '\r\n'));
    }
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /12 templates valid/);
});

test('quoted boolean is rejected rather than silently treated as true', () => {
  const result = check((temp) => {
    const path = join(temp, 'templates/domain-lifecycle.md');
    writeFileSync(path, readFileSync(path, 'utf8').replace('initial: true', 'initial: "true"'));
  });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /expected a boolean/);
});

test('nested transition relationship sequences parse with continued keys', () => {
  const result = check((temp) => {
    const path = join(temp, 'templates/domain-lifecycle.md');
    writeFileSync(path, readFileSync(path, 'utf8').replace('initiated-by: [ACT-EXAMPLE-001]', 'initiated-by:\n      - ACT-EXAMPLE-001'));
  });
  assert.equal(result.status, 0, result.stderr);
});
