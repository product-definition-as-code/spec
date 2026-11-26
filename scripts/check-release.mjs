import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const root = fileURLToPath(new URL('..', import.meta.url));
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const release = JSON.parse(read('release.json'));
const report = JSON.parse(read(release.evidence));
export function checkReport(report, release, cases) {
  assert.equal(report.schema, 'pdac-conformance/report/v1');
  assert.deepEqual(report.summary, {
    total: release.cases, passed: release.cases, failed: 0, skipped: 0, errored: 0,
  });
  assert.deepEqual(report.cases.map(c => c.name).sort(), cases.sort());
  assert.ok(report.cases.every(c => c.status === 'pass'));
  assert.equal(report.provenance.observed.spec.revision, release.specRevision);
  assert.equal(report.provenance.observed.spec.dirty, false);
  assert.equal(report.provenance.observed.runner.version, release.runner.version);
  assert.equal(report.provenance.claimed.implementation.version, release.implementation.version);
  assert.equal(report.provenance.claimed.implementation.artifactIdentity, `sha256:${release.implementation.sha256}`);
  assert.equal(report.provenance.claimed.spec.version, release.methodVersion);
  assert.equal(report.provenance.claimed.spec.serializationVersion, release.serializationVersion);
}
if (process.argv.includes('--self-test')) {
  const cases = report.cases.map(c => c.name);
  checkReport(report, release, cases);
  const skipped = structuredClone(report);
  skipped.summary.skipped = 1;
  assert.throws(() => checkReport(skipped, release, cases));
  assert.throws(() => checkReport(report, release, [...cases, 'unexecuted-case']));
  const wrongPair = structuredClone(release);
  wrongPair.serializationVersion = 'v1alpha1';
  assert.throws(() => checkReport(report, wrongPair, cases));
  console.log('Release guard rejects skips, missing cases and mismatched version pairs.');
} else {
  checkReport(report, release, readdirSync(resolve(root, 'conformance/cases')));
  for (const path of ['README.md', 'MATURITY.md', 'spec/index.md']) {
    const text = read(path);
    assert.ok(text.includes(release.methodVersion), `${path}: missing method version`);
    assert.ok(text.includes(release.serializationVersion), `${path}: missing serialization version`);
    assert.doesNotMatch(text, /v0\.3\.0 development candidate|latest released version remains v0\.2\.0/);
  }
  for (const path of ['conformance/cases', 'schemas/v1alpha1', 'schemas/v1alpha2']) {
    execFileSync('git', ['diff', '--exit-code', release.specRevision, '--', path], { cwd: root });
  }
  assert.ok(read('CHANGELOG.md').includes(`## [${release.methodVersion}]`));
  assert.ok(read('.github/workflows/conformance.yml').includes(`${release.runner.package}@${release.runner.version}`));
  if (process.argv.includes('--published')) {
    for (const pkg of [release.runner, release.implementation]) {
      const response = await fetch(`https://registry.npmjs.org/${pkg.package}/${pkg.version}`);
      assert.ok(response.ok, `${pkg.package}@${pkg.version}: registry HTTP ${response.status}`);
      assert.equal((await response.json()).version, pkg.version);
    }
    const response = await fetch(`https://api.github.com/repos/product-definition-as-code/spec/releases/tags/v${release.methodVersion}`);
    assert.ok(response.ok, `Official release: HTTP ${response.status}`);
    const published = await response.json();
    assert.equal(published.draft, false);
    assert.equal(published.prerelease, false);
    const live = await fetch('https://pdac.dev/release.json');
    assert.ok(live.ok, `Live release manifest: HTTP ${live.status}`);
    assert.deepEqual(await live.json(), release);
  }
  console.log(`${release.methodVersion}/${release.serializationVersion}: ${release.cases} passing cases; documentation and runner pin agree.`);
}
