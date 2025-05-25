# Latest Sprint Plan

This plan outlines the next five logical sprints after completing the advanced front-end features.

## Sprint 1 – Cloud infrastructure templates (completed)
* Added `infra/aws` sample using Terraform and App Runner.
* Secrets are supplied via `TF_VAR_*` environment variables.

## Sprint 2 – Mobile PWA polish (completed)
* Fine‑tune touch controls in the 3‑D viewer.
* Add install prompts and home-screen icons.

## Sprint 3 – Documentation cleanup (completed)
* Consolidate older sprint plans.
* Expand deployment instructions with best practices.

## Sprint 4 – Continuous benchmarking (completed)
* Automate the scalability benchmark in CI for regressions.
* Added a stub server benchmark step in CI.

## Sprint 5 – Community example library (completed)
* Added a gallery of example builds and shareable prompts in the PWA.

## Sprint 6 – Automated UI regression tests (completed)
* Added Cypress setup and a basic end-to-end test for the PWA.

## Sprint 7 – Multi-language support (completed)
* Introduced a language switcher and Spanish translations in the PWA.

## Sprint 8 – Real-time collaboration (completed)
* Added a simple WebSocket server and CLI (`lego-gpt-collab`).

## Sprint 9 – Model quality improvements (completed)
* Backend can load custom checkpoints via the `LEGOGPT_MODEL` env var.

## Sprint 10 – Accessibility polish (completed)
* Added ARIA labels and improved keyboard navigation in the PWA.

Older sprint plans were combined into `SPRINT_PLAN_ARCHIVE.md` as part of the
documentation cleanup.
