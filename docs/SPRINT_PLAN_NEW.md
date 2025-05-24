# Upcoming Sprint Plan

This plan outlines the next five logical sprints after completing the detector training workflow.

## Sprint 1 – Offline mode improvements (completed)
* Cache API responses in IndexedDB for repeat access.
* Added a service worker route for cached preview images.

## Sprint 2 – Enhanced CLI options (completed)
* Support batch generation via a file of prompts.
* Add progress indicators and richer error messages.

## Sprint 3 – CLI integration tests (completed)
* Cover new batch and progress features end-to-end.
* Maintain fast execution with mocked API responses.

## Sprint 4 – Deployment automation
* Build production Docker images for CPU and GPU targets.
* Publish versioned images to the registry.

## Sprint 5 – Scalability benchmarking
* Measure throughput with multiple workers and queue setups.
* Document tuning guidelines for self-hosted deployments.
