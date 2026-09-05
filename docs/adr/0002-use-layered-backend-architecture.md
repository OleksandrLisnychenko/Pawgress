---
status: Accepted
owner: "Oleksandr Lisnychenko"
reviewers: []
updated_at: "2026-09-05"
feature_size: ""
ticket: ""
---

# 0002 — Use a simple layered backend architecture (api → services → repositories → models)

- **Status:** Accepted
- **Date:** 2026-09-05
- **Deciders:** Oleksandr Lisnychenko (owner), during the `survey` greenfield foundation session

## Context

The backend needs a module/layer structure fixed before scaffolding. Pawgress is a solo-owner
MVP with a small, well-understood domain (commands/skills, statuses, a training journal) — the
structure should be cheap to work in, not a framework for hypothetical future complexity.

## Decision drivers

- Explicit "MVP на скору руку" (quick, no-frills MVP) direction from the owner during this session — favors the simplest structure that still separates concerns.
- Solo developer, single backend service — no need for module boundaries that anticipate a team or a future split into services.
- Still wants a clean seam between HTTP concerns and business logic, and between business logic and persistence, so the training-journal aggregation logic (success-rate trend) isn't tangled into route handlers or SQL.

## Considered options

1. **Flat layered architecture** — `api/` (FastAPI routers) → `services/` (business logic) → `repositories/` (SQLAlchemy access) → `models/` (ORM) + `schemas/` (Pydantic), all within one `backend/app/` package.
2. **Hexagonal / ports-and-adapters** — domain/app/infra/ports with explicit interface boundaries — more rigorous but adds ceremony (interfaces, dependency inversion wiring) that a solo MVP doesn't need yet.
3. **Everything in route handlers** — fastest to write, but mixes HTTP, business logic, and SQL in one place, making the training-journal and success-rate logic hard to test or change later.

## Decision outcome

**Chosen:** Option 1 — flat layered architecture. It gives the minimum separation needed (routes
don't know SQL, services don't know HTTP) without the interface/wiring overhead of hexagonal
architecture, matching the "MVP на скору руку" driver.

## Consequences

**Positive**
- Easy to navigate for a single developer — one obvious place for each kind of code.
- Business logic (status transitions, success-rate calculation) stays testable independent of FastAPI or SQLAlchemy specifics.
- Low ceremony — no interfaces/ports to define before writing the first feature.

**Negative**
- No enforced dependency-inversion boundary — a service could technically import SQLAlchemy directly if discipline slips; this is a convention, not a compiler-enforced rule.
- If the project ever needs to split into multiple deployable services, this structure will need real rework (acceptable — not a current concern).

**Neutral**
- Migrating to hexagonal later is possible without a full rewrite, since services already sit behind a a clear boundary from routers.

## Links

- Spec: [[../idea-brief.md]]
- SAD: none yet — no feature has been designed
- Related ADR: [[0001-choose-python-fastapi-angular-stack]], [[0003-use-sqlite-alembic-ulid-persistence]]
