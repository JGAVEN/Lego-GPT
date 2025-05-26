#!/usr/bin/env node
import { spawnSync, spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const frontend = join(root, '..', 'frontend');
const lh = join(frontend, 'node_modules', '.bin', 'lighthouse');
if (!existsSync(lh)) {
  console.error('Lighthouse not installed; skipping performance audit.');
  process.exit(0);
}
spawnSync('pnpm', ['exec', 'vite', 'build'], { cwd: frontend, stdio: 'inherit' });
const preview = spawn('pnpm', ['exec', 'vite', 'preview', '--port', '4173'], {
  cwd: frontend,
  stdio: 'ignore'
});
await new Promise(r => setTimeout(r, 2000));
const res = spawnSync(lh, ['http://localhost:4173', '--quiet', '--only-categories=performance', `--budget-path=${join(frontend,'lighthouse-budget.json')}`], { stdio: 'inherit' });
preview.kill();
process.exit(res.status);
