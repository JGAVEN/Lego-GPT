# Latest Sprint Plan

This plan outlines the next five logical sprints after completing the offline mode improvements.

## Sprint 1 – Enhanced CLI options (completed)
* Support batch generation via a file of prompts.
* Add progress indicators and richer error messages.

## Sprint 2 – CLI integration tests (completed)
* Cover new batch and progress features end-to-end.
* Maintain fast execution with mocked API responses.

## Sprint 3 – Deployment automation (completed)
* Build production Docker images for CPU and GPU targets.
* Publish versioned images to the registry.

## Sprint 4 – Scalability benchmarking (completed)
* Added `benchmark_scalability.py` script to measure throughput.
* Documented tuning guidelines in `docs/SCALABILITY_BENCHMARKING.md`.

## Sprint 5 – Advanced front-end features (completed)
* Improve offline UX with queued requests when offline.
* Add settings page to manage cached results.
