---
status: Accepted
owner: "Oleksandr Lisnychenko"
reviewers: []
updated_at: "2026-09-05"
feature_size: ""
ticket: ""
---

# 0001 — Use Python/FastAPI for the backend and Angular for the frontend

- **Status:** Accepted
- **Date:** 2026-09-05
- **Deciders:** Oleksandr Lisnychenko (owner), during the `survey` greenfield foundation session

## Context

Pawgress is a solo puppy-training tracker (see `docs/idea-brief.md`) with no code yet. The stack
had to be fixed before anything could be scaffolded. The owner's idea brief already named
FastAPI + SQLite for the backend and Angular for the frontend — this ADR records that as a
deliberate, irreversible foundation choice rather than leaving it implicit.

## Decision drivers

- The owner named this stack directly in the raw idea (`docs/idea-brief.md` §1) — a pre-existing preference, not derived from an NFR.
- Solo MVP, moving fast: the stack needed to be something the owner is already comfortable with, not the "best" stack in the abstract.
- HTTP API + separate web frontend fits the product shape (a browser app talking to a REST backend).

## Considered options

1. **Python + FastAPI (backend) + Angular (frontend)** — the owner's stated choice; async-friendly, typed, mainstream framework combo.
2. **Node.js (Express/NestJS) full-stack with a single language** — would unify the language across front/back, but abandons the owner's explicit FastAPI/Angular preference for no stated benefit.
3. **Django (backend) + Angular** — a batteries-included alternative to FastAPI, but heavier than a small MVP needs and not what the owner asked for.

## Decision outcome

**Chosen:** Option 1 — Python + FastAPI + Angular. This matches what the owner already specified
in the idea brief; no driver surfaced during the interview or this session argued for deviating
from it.

## Consequences

**Positive**
- Matches the owner's existing intent — no re-litigation needed.
- FastAPI + Pydantic gives request/response validation and OpenAPI docs for free, useful once `/sdd:api` runs.
- Angular's structure (standalone components, CLI-driven) gives a clear, opinionated frontend layout for a solo dev.

**Negative**
- Two separate toolchains (Python + Node/TypeScript) to maintain in one repo — more setup than a single-language stack.
- SQLite (chosen alongside this stack) will eventually need a migration path to a server DB if the app ever needs concurrent multi-user access — not a concern for the current single-owner scope.

**Neutral**
- Switching either half of the stack later is possible but would be a substantial rewrite of that layer.

## Links

- Spec: [[../idea-brief.md]]
- SAD: none yet — no feature has been designed
- Related ADR: [[0002-use-layered-backend-architecture]], [[0003-use-sqlite-alembic-ulid-persistence]]
