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

## Sprint 19 – Example submission pipeline (completed)
* Added `/submit_example` endpoint storing community prompts for review.

## Sprint 20 – Build progress events (completed)
* Worker updates job meta and `/progress/<job_id>` streams progress via SSE.

## Sprint 21 – Submission review CLI (completed)
* Added `lego-gpt-review` for listing and approving community examples.

## Sprint 22 – CLI progress streaming (completed)
* `lego-gpt-cli` now streams live progress from `/progress/<job_id>` via SSE.

## Sprint 23 – Automatic example tagging (completed)
* `lego-gpt-review` automatically generates keyword tags when approving submissions.

## Sprint 24 – Example search and filter (completed)
* Gallery UI can filter community examples by tag or free‑text search.

## Sprint 25 – Example rating system (completed)
* Users can rate community examples with 1–5 stars stored locally.
* Average rating is shown in the gallery.

## Sprint 26 – Favourite examples (completed)
* Gallery allows bookmarking favourites locally and toggling a favourites view.

## Sprint 27 – Submission moderation dashboard (completed)
* Web dashboard lists pending submissions with approve/reject actions.

## Sprint 28 – Collaboration chat messages (completed)
* WebSocket server broadcasts `/chat` messages.
* Demo page shows a simple chat panel.

## Sprint 29 – Build instructions export (completed)
* Worker outputs placeholder PDF instructions alongside the model files.
* CLI and PWA provide a download link for the PDF.

## Sprint 30 – Example comments (completed)
* Signed-in users can comment on community examples.
* Recent comments are displayed below each example.

## Sprint 31 – Social sharing links (completed)
* Share buttons allow posting examples or builds to social media.

## Sprint 32 – Advanced build instructions (completed)
* PDF export includes basic part lists instead of a placeholder.

## Sprint 33 – Mobile push opt-in prompt (completed)
* A one-time prompt explains push notifications and lets users enable them.

## Sprint 34 – Admin analytics dashboard (completed)
* Simple metrics dashboard shows request and submission counts.

## Sprint 35 – Comment notifications (completed)
* Email is sent to `COMMENT_NOTIFY_EMAIL` when a new comment is posted.

## Sprint 36 – Federated example search (completed)
* Added `/search_examples?q=` endpoint aggregating results from remote instances.

## Sprint 37 – Mobile UI polish (completed)
* Improved button padding and font sizes on small screens.

## Sprint 38 – Admin roles (completed)
* JWT tokens may include a `role` claim; admin-only endpoints now require it.

## Sprint 39 – Live metrics stream (completed)
* New `lego-gpt-metrics` WebSocket server streams metrics to connected clients.

## Sprint 40 – Build history export (completed)
* `/history` endpoint returns per-user JSON build history.

## Sprint 41 – Distributed moderation queue (completed)
* Submissions are stored in Redis so multiple instances share the queue.

## Sprint 42 – Account linking (completed)
* Users generate a one-time link code to sync tokens across devices.

## Sprint 43 – Notification preferences (completed)
* `/preferences` endpoint stores per-user email and push settings.

## Sprint 44 – Example import/export (completed)
* New `lego-gpt-examples` CLI can export and import `examples.json`.

## Sprint 45 – Resilience improvements (completed)
* Worker jobs retry automatically and `/health` checks Redis status.

## Sprint 46 – Submission reporting (completed)
* Users can flag inappropriate examples for admin review.

## Sprint 47 – Rate-limit metrics (completed)
* Metrics dashboard charts token usage and rate-limit hits.

## Sprint 48 – Improved CLI auth (completed)
* `lego-gpt-cli` reads tokens from `~/.lego-gpt` if `--token` is missing.

## Sprint 49 – Mobile performance audit (completed)
* Lighthouse-based CI job enforces PWA performance budgets.

## Sprint 50 – Comment moderation tools (completed)
* Admin dashboard can delete comments and ban users.

## Sprint 51 – Example report review UI (completed)
* Admin dashboard lists flagged examples and allows clearing reports.

## Sprint 52 – Token usage graphs (completed)
* Metrics dashboard visualises token usage and rate-limit trends.

## Sprint 53 – Offline CLI usage (completed)
* CLI queues requests offline and replays them when connected.

## Sprint 54 – Advanced performance budgets (completed)
* Lighthouse CI also checks accessibility and best-practices scores.

## Sprint 55 – Federated comment moderation (completed)
* Banned-user lists can be synced across instances via a new CLI.

## Sprint 56 – Persistent offline queue (completed)
* Front-end and CLI store pending requests across sessions.

## Sprint 57 – Analytics export CLI (completed)
* Admins can export metrics history to CSV for external analysis.

## Sprint 58 – Dark mode theme (completed)
* PWA offers a dark mode toggle and remembers the preference.

## Sprint 59 – YAML server config (completed)
* Server and workers can load settings from a YAML file.

## Sprint 60 – CLI plugin system (completed)
* Third-party plugins can extend the command-line client.

## Sprint 61 – Scheduled cleanup jobs (completed)
* Server runs periodic tasks to purge old assets automatically.

## Sprint 62 – Kubernetes templates (completed)
* Added sample manifests under `infra/k8s` for deploying the stack on Kubernetes.

## Sprint 63 – CLI shell completion (completed)
* `lego-gpt-cli completion` outputs bash or zsh scripts.

## Sprint 64 – In-app tutorial overlay (completed)
* First-time users see a short guided tour in the PWA.

## Sprint 65 – Prometheus metrics exporter (completed)
* `/metrics_prom` returns counters in Prometheus format.

## Sprint 66 – Example translation workflow (completed)
* `lego-gpt-translate` CLI translates example prompts via an external API.

## Sprint 67 – Helm chart skeleton (completed)
* Added `infra/helm` with a minimal Helm chart for Kubernetes.

## Sprint 68 – CLI config generator (completed)
* Added `lego-gpt-config` command that outputs a sample YAML config.

## Sprint 69 – Auto-scaling docs (completed)
* Documented horizontal scaling strategies for workers in `SCALABILITY_BENCHMARKING.md`.

## Sprint 70 – Remote example import UI (completed)
* New PWA page allows importing examples from another instance.

## Sprint 71 – Theme colour picker (completed)
* Settings page includes a colour input that updates the accent CSS variable.

## Sprint 72 – Container security hardening (completed)
* Production Dockerfiles now create a non-root user.

## Sprint 73 – Admin user management CLI (completed)
* Added `lego-gpt-users` tool for listing and deleting accounts.

Older sprint plans were combined into `SPRINT_PLAN_ARCHIVE.md` as part of the
documentation cleanup.
