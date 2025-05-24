# Future Sprint Plan

This document lists the next five sprints after completing the solver edge-case tests.

## Sprint 1 – Detector training workflow (completed)
* Provided `detector/Dockerfile.train` and `scripts/train_detector.sh`.
* Documented dataset layout in `docs/DETECTOR_DATASET.md`.

## Sprint 2 – Offline mode improvements (completed)
* Cache API responses in IndexedDB for repeat access.
* Added a service worker route for cached preview images.

## Sprint 3 – Enhanced CLI options
* Support batch generation via a file of prompts.
* Add progress indicators and richer error messages.

## Sprint 4 – CLI integration tests
* Cover new batch and progress features end-to-end.
* Maintain fast execution with mocked API responses.

## Sprint 5 – Deployment automation
* Build production Docker images for CPU and GPU targets.
* Publish versioned images to the registry.
