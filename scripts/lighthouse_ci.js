#!/usr/bin/env node
import { spawnSync, spawn } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
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
const report = join(frontend, 'lh-report.json');
const budget = JSON.parse(readFileSync(join(frontend, 'lighthouse-budget.json'), 'utf8'))[0];
const res = spawnSync(lh, [
  'http://localhost:4173',
  '--quiet',
  '--output=json',
  `--output-path=${report}`,
  '--only-categories=performance,accessibility,best-practices',
  `--budget-path=${join(frontend,'lighthouse-budget.json')}`
], { stdio: 'inherit' });
if (existsSync(report)) {
  const data = JSON.parse(readFileSync(report, 'utf8'));
  const scores = data.categories;
  const thresholds = budget.scores || { accessibility: 90, 'best-practices': 90 };
  if (
    scores.performance.score < 0.9 ||
    scores.accessibility.score * 100 < thresholds.accessibility ||
    scores['best-practices'].score * 100 < thresholds['best-practices']
  ) {
    console.error('Lighthouse scores below budget.');
    process.exit(1);
  }
}
preview.kill();
process.exit(res.status);
