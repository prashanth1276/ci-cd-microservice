# CI/CD Pipeline Setup for a Microservice

> **End-to-end CI/CD pipeline with quality gates, artifact management, real deployment and rollback — built to reflect real industry practices.**

---

## Project Overview

This project demonstrates a **production-grade CI/CD pipeline** for a Python-based microservice using **GitHub Actions**, **Docker**, **Docker Compose**, **SonarQube**, and **GitHub Container Registry (GHCR)**.

The goal was to eliminate manual builds and deployments by implementing:

* Automated testing and linting
* Code quality & coverage gates
* Containerized builds
* Versioned artifact publishing
* **Real continuous deployment to a running environment**
* Manual rollback by redeploying the latest production image

This setup closely mirrors how modern engineering teams ship and maintain microservices in real-world environments.

---

## Tech Stack

| Category                | Tools                                       |
| ----------------------- | ------------------------------------------- |
| Language                | Python 3.11                                 |
| Framework               | Flask                                       |
| CI/CD                   | GitHub Actions                              |
| Code Quality            | Flake8, Pytest, Pytest-Cov                  |
| Security & Quality Gate | SonarCloud                                  |
| Containerization        | Docker                                      |
| Deployment              | Docker Compose (VM-based)                   |
| Artifact Registry       | GitHub Container Registry (GHCR)            |
| Deployment Runner       | Self-hosted GitHub Actions Runner (Windows) |

---

## Microservice Details

### Application Features

* `/` → Health endpoint (returns status + environment)
* `/hello` → Sample API endpoint
* Environment-aware configuration using `APP_ENV`

### Environment Handling

* **Dev**: Local build using Docker Compose
* **Prod**: Pre-built image pulled from GHCR

---

## Docker & Compose Setup

### Dockerfile

* Uses `python:3.11-slim`
* Layer-optimized build
* Production-ready image

### Docker Compose

**Development** (`docker-compose.dev.yml`)

* Builds image locally
* Used for local testing

**Production** (`docker-compose.prod.yml`)

* Pulls image from GHCR
* Injects `APP_ENV=prod`
* Uses restart policies

---

## CI/CD Architecture

```
Developer Push / PR
        ↓
GitHub Actions (CI)
        ↓
Lint → Test → Coverage → SonarQube Quality Gate
        ↓
Docker Image Build
        ↓
Tag (SHA / SemVer / latest)
        ↓
Push to GHCR
        ↓
Self-hosted Runner (CD)
        ↓
Docker Compose Deployment
```

---

## Continuous Integration (CI)

The CI pipeline runs automatically on:

* Pull Requests
* Merges to `main`

### CI Steps

1. Checkout source code
2. Install dependencies
3. Lint with **Flake8**
4. Run unit tests
5. Enforce **80% coverage threshold**
6. Generate coverage report (XML)
7. Run **SonarCloud analysis**
8. Enforce **Sonar Quality Gate**
9. Build Docker image
10. Tag image with:

* Git SHA
* Semantic version
* `latest`

11. Push image to **GHCR**

**Quality gates ensure that bad code never reaches production.**

---

## Artifact Management

Each successful pipeline run publishes **three Docker image tags**:

* `:latest`
* `:<semantic-version>` (example: `0.1.0`)
* `:<git-sha>`

This enables:

* Traceability
* Reproducible deployments
* Safe rollbacks

---

## Continuous Deployment (CD)

### Deployment Strategy

* Uses a **self-hosted GitHub Actions runner**
* Runs on merge to `main`
* Deploys via **Docker Compose**

### CD Steps

1. Authenticate to GHCR
2. Pull latest production image
3. Stop existing containers
4. Start updated containers
5. Verify running containers

**Containers remain running after the workflow finishes**

---

## Rollback Mechanism

A dedicated rollback workflow allows manually redeploying the production service using Docker Compose.

### Rollback Features

* Manual trigger via GitHub UI (`workflow_dispatch`)
* Re-deploys the service using Docker Compose
* Does not require rebuilding artifacts

---

## Code Quality & Security

### SonarCloud Integration

* Static code analysis
* Code smells & maintainability checks
* Coverage enforcement
* Quality Gate blocking deployments

This ensures:

* Clean, maintainable code
* Early detection of issues

---

## Security Considerations

* Uses **GitHub-provided `GITHUB_TOKEN`** (no hardcoded secrets)
* Scoped permissions (`contents`, `packages`)
* No credentials committed to the repository
* Self-hosted runner used only for deployment

Note: Self-hosted runners in public repos require trust. This setup reflects a controlled environment similar to internal company repos.

---

## How to Run Locally

```bash
# Development
Docker Compose -f docker-compose.dev.yml up --build

# Production-style
Docker Compose -f docker-compose.prod.yml up -d
```
