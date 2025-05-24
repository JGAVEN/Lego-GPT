# Future Sprint Plan

This document lists the next five sprints after completing the solver edge-case tests.

## Sprint 1 – Detector training workflow
* Provide Dockerfile and scripts to train YOLOv8 models.
* Document dataset format and expected output.

## Sprint 2 – Offline mode improvements
* Cache API responses in IndexedDB for repeat access.
* Add a service worker route for cached preview images.

## Sprint 3 – Enhanced CLI options
* Support batch generation via a file of prompts.
* Add progress indicators and richer error messages.

## Sprint 4 – CLI integration tests
* Cover new batch and progress features end-to-end.
* Maintain fast execution with mocked API responses.

## Sprint 5 – Deployment automation
* Build production Docker images for CPU and GPU targets.
* Publish versioned images to the registry.
