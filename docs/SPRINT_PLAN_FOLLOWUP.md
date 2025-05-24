# Follow-up Sprint Plan

This document lists the next five sprints after completing the front-end TypeScript migration.

## Sprint 1 – Solver edge-case unit tests (completed)
* Add tests for ill-conditioned graphs and complex overhang scenarios.
* Keep CI green with OR-Tools HiGHS backend.

## Sprint 2 – Detector training workflow
* Provide Dockerfile and scripts to train YOLOv8 models.
* Document dataset format and expected output.

## Sprint 3 – Offline mode improvements
* Cache API responses in IndexedDB for repeat access.
* Add a service worker route for cached preview images.

## Sprint 4 – Enhanced CLI options
* Support batch generation via a file of prompts.
* Add progress indicators and richer error messages.

## Sprint 5 – CLI integration tests
* Cover new batch and progress features end-to-end.
* Maintain fast execution with mocked API responses.
