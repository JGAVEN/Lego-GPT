# Contributing & AI‑Agent Workflow

This project is developed by a **human owner (Jeff) plus ChatGPT‑4o “dev agents”.**

## Ground rules for *all* dev agents

1. **One atomic step at a time.**  
   End each message with **“➡️ Reply \`done\` when finished, or \`help\` if stuck.”**
2. **macOS + zsh** is assumed. Use full paths (`~/Documents/Lego-GPT`).
3. **Ask before destructive actions.**  
   If a command could delete or overwrite, request explicit approval.
4. **Show expected console output** so Jeff can verify each step.
5. **Commit etiquette**  
   * Conventional Commits (`feat:`, `fix:`, `docs:` …).  
   * One logical change per PR.  
   * `git push --set-upstream origin <branch>`; open PR and add `@OpenAI-JeffArchitect` as reviewer.
6. **Docs are living.**  
   After a ticket merges, update `CHANGELOG.md` and, if scope changes, `PROJECT_BACKLOG.md`.

## Local setup (for humans)

```bash
brew install git gh docker --cask docker docker-compose node@20 pnpm
git clone git@github.com:JGAVEN/Lego-GPT.git
cd Lego-GPT && git submodule update --init
./scripts/setup_frontend.sh \
  # run automatically in the dev container's setup script
  # installs React and linting packages used by scripts/lint_frontend.js
python -m pip install --editable ./backend[test]  # backend + worker deps (incl. fakeredis for tests)
  # also installed automatically in the dev container
```

Run `ruff check backend detector` before pushing to ensure code style.

See **docs/ARCHITECTURE.md** for more details.
