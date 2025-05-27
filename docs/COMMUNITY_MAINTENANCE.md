# Community Maintenance Guide

This project is now community‑maintained. The codebase remains English‑only and receives security fixes only.
See [LTS_POLICY.md](LTS_POLICY.md) for details on the support timeline.

## Forking
1. Use the GitHub **Fork** button to create your own copy.
2. Clone your fork locally and add this repository as `upstream`:
   ```bash
   git clone https://github.com/<yourname>/Lego-GPT.git
   cd Lego-GPT
   git remote add upstream https://github.com/JGAVEN/Lego-GPT.git
   ```
3. Create feature branches from `main` and keep your fork up to date:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

## Submitting Security Fixes
1. Install dependencies and run tests:
   ```bash
   python -m pip install --editable ./backend[test,env]
   ./scripts/setup_frontend.sh
   ./scripts/run_tests.sh
   ```
2. Commit your patch following the Conventional Commits style.
3. Open a pull request against `JGAVEN/Lego-GPT` and add the **security** label.
4. Provide a clear description of the vulnerability and how your fix resolves it.

See `CONTRIBUTING.md` for general workflow details.
