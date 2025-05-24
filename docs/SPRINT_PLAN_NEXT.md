# Next Sprint Plan

This plan outlines the following sprints after completing the initial roadmap.

## Sprint 1 – Front-end TypeScript migration (completed)
* Converted all React components to TypeScript.
* Added a `typecheck` script so the project builds and type-checks via `pnpm typecheck`.

## Sprint 2 – Solver edge-case unit tests (completed)
* Add tests for ill-conditioned graphs and complex overhang scenarios.
* Keep CI green with OR-Tools HiGHS backend.

## Sprint 3 – Detector training workflow
* Provide Dockerfile and scripts to train YOLOv8 models.
* Document dataset format and expected output.

## Sprint 4 – Offline mode improvements
* Cache API responses in IndexedDB for repeat access.
* Add a service worker route for cached preview images.

## Sprint 5 – Enhanced CLI options
* Support batch generation via a file of prompts.
* Add progress indicators and richer error messages.
