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

## Sprint 7 – UI text cleanup (completed)
* Removed the language switcher; the interface is now English only.

## Sprint 8 – Real-time collaboration (completed)
* Added a simple WebSocket server and CLI (`lego-gpt-collab`).

## Sprint 9 – Model quality improvements (completed)
* Backend can load custom checkpoints via the `LEGOGPT_MODEL` env var.

## Sprint 10 – Accessibility polish (completed)
* Added ARIA labels and improved keyboard navigation in the PWA.

## Sprint 11 – Offline mode enhancements (completed)
* Queued collaboration edits offline and synced them when reconnected.

## Sprint 12 – Push notifications (completed)
* Service worker displays notifications when collaborators edit a build.

## Sprint 13 – Interface polish (completed)
* The PWA remains English only and includes a collaboration demo page.

## Sprint 14 – Collaborative undo/redo (completed)
* WebSocket server keeps per-room history and handles `/undo` and `/redo`.
* Demo page shows Undo and Redo buttons.

## Sprint 15 – Push subscription management (completed)
* Settings page can enable or disable Web Push notifications.

## Sprint 16 – Expanded example library (completed)
* Added more sample prompts and images in `examples.json`.

## Sprint 17 – Automated front-end setup (completed)
* Dev container calls `scripts/setup_frontend.sh` to install packages.

## Sprint 18 – Presence indicator (completed)
* Collaboration server broadcasts the number of peers in each room.
* Demo page displays connected collaborator count.

Older sprint plans were combined into `SPRINT_PLAN_ARCHIVE.md` as part of the
documentation cleanup.
