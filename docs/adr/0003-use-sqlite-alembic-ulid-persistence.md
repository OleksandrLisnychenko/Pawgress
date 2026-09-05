---
status: Accepted
owner: "Oleksandr Lisnychenko"
reviewers: []
updated_at: "2026-09-05"
feature_size: ""
ticket: ""
---

# 0003 — Use SQLite + Alembic migrations + app-generated ULID primary keys

- **Status:** Accepted
- **Date:** 2026-09-05
- **Deciders:** Oleksandr Lisnychenko (owner), during the `survey` greenfield foundation session

## Context

The backend needs a persistence approach — datastore, migration tool, and ID strategy — fixed
before scaffolding, since changing any of these later means a real data migration.

## Decision drivers

- The owner named SQLite directly in the idea brief (`docs/idea-brief.md` §1) — a single-owner, single-puppy MVP has no concurrent-write load that would need a server database.
- Solo MVP direction ("MVP на скору руку") favors the lowest-ceremony persistence setup: no DB server to run, no connection pooling to configure.
- The data model will need to support status history that can move backward (see idea-brief §6 Risks) — nothing about SQLite/Alembic/ULID blocks that; it's a schema-design concern for `data-model`, not this ADR.

## Considered options

1. **SQLite + Alembic migrations + app-generated ULID string primary keys** — file-based DB, no server process; Alembic is SQLAlchemy's standard migration tool; ULIDs are time-sortable and generated in the application layer rather than relying on DB auto-increment.
2. **SQLite + Alembic + DB auto-increment integer PKs** — simpler ID story, but couples ID generation to the DB and makes IDs non-sortable-by-creation-time without a separate timestamp column, and complicates any future move to a server DB (auto-increment sequences don't merge cleanly).
3. **PostgreSQL + Alembic + ULID** — more headroom for concurrent access and a production-grade DB, but adds a DB server dependency the single-owner MVP doesn't need yet.

## Decision outcome

**Chosen:** Option 1 — SQLite + Alembic + app-generated ULID primary keys. Matches the owner's
stated choice of SQLite, keeps the migration story standard (Alembic is SQLAlchemy's own tool),
and ULIDs keep IDs meaningful (time-sortable, DB-independent) if the project ever needs to move
off SQLite without an ID redesign.

## Consequences

**Positive**
- Zero-ops persistence for local/solo development — no DB server to install or run.
- Alembic gives reversible, versioned schema changes from day one.
- ULIDs are generated before insert, so IDs are known application-side (useful for the journal/skill relationships) and stay time-sortable.

**Negative**
- SQLite has real concurrency limits (single-writer) — acceptable for one owner, but would need revisiting if Pawgress ever grows beyond a single-user tool.
- ULID string PKs are slightly larger and less human-memorable than small integers, and every model/repository must generate one explicitly rather than relying on the DB.

**Neutral**
- Moving to a server database later (PostgreSQL, etc.) is a standard SQLAlchemy-engine swap plus a data export/import — Alembic migrations would need re-targeting but the schema itself doesn't need to change because of this choice.

## Links

- Spec: [[../idea-brief.md]]
- SAD: none yet — no feature has been designed
- Related ADR: [[0001-choose-python-fastapi-angular-stack]], [[0002-use-layered-backend-architecture]]
