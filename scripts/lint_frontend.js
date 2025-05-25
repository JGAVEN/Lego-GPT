#!/usr/bin/env node
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const frontendDir = join(root, '..', 'frontend');
process.chdir(frontendDir);

const eslintBin = join('node_modules', '.bin', 'eslint');
if (!existsSync(eslintBin)) {
  console.error('Front-end dependencies missing. Run scripts/setup_frontend.sh with network access.');
  process.exit(0);
}

try {
  execSync('pnpm exec eslint .', { stdio: 'inherit' });
} catch (err) {
  process.exit(err.status || 1);
}
