import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execute = promisify(execFile);
const script = fileURLToPath(new URL('../scripts/deploy_site.sh', import.meta.url));

async function deployment(t, overrides) {
  const directory = await mkdtemp(join(tmpdir(), 'final8-deploy-test-'));
  t.after(() => rm(directory, { recursive: true, force: true }));
  const bin = join(directory, 'bin');
  const log = join(directory, 'git.log');
  await mkdir(bin);
  await writeFile(log, '');
  await writeFile(join(bin, 'npm'), '#!/bin/sh\nexit "${DEPLOY_TEST_NPM_EXIT:-0}"\n', { mode: 0o755 });
  await writeFile(join(bin, 'git'), `#!/bin/sh
printf '%s\\n' "$*" >> "$DEPLOY_TEST_LOG"
if [ "$1" = "ls-remote" ] && [ -n "$DEPLOY_TEST_TIP" ]; then
  printf '%s\\trefs/heads/gh-pages\\n' "$DEPLOY_TEST_TIP"
fi
if [ "$1" = "push" ] && [ "$DEPLOY_TEST_CONFLICT" = "1" ]; then
  exit 1
fi
`, { mode: 0o755 });
  return {
    run: () => execute('bash', [script], {
      env: {
        ...process.env,
        PATH: `${bin}:${process.env.PATH}`,
        DEPLOY_TEST_LOG: log,
        DEPLOY_TEST_TIP: 'a'.repeat(40),
        ...overrides,
      },
    }),
    commands: () => readFile(log, 'utf8'),
  };
}

test('a failed quality gate stops before any remote operation', async t => {
  const deploy = await deployment(t, { DEPLOY_TEST_NPM_EXIT: '1' });
  await assert.rejects(deploy.run(), { code: 1 });
  assert.equal(await deploy.commands(), '');
});

test('a rejected lease fails deployment instead of reporting success', async t => {
  const deploy = await deployment(t, { DEPLOY_TEST_CONFLICT: '1' });
  await assert.rejects(deploy.run(), { code: 1 });
  assert.match(await deploy.commands(), new RegExp(
    `push --force-with-lease=refs/heads/gh-pages:${'a'.repeat(40)} origin HEAD:refs/heads/gh-pages`
  ));
});

test('first deployment requires the remote branch to remain absent', async t => {
  const deploy = await deployment(t, { DEPLOY_TEST_TIP: '' });
  await deploy.run();
  assert.match(await deploy.commands(), /push --force-with-lease=refs\/heads\/gh-pages: origin HEAD:refs\/heads\/gh-pages/);
});
