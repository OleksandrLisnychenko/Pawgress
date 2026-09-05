# Pawgress

Puppy skill/command tracking app. Backend: Python 3.12 + FastAPI + SQLAlchemy + Alembic + SQLite.
Frontend: Angular (standalone components, no NgModules).

## Backend conventions

- **Layering:** `api/` (FastAPI routers, HTTP boundary) → `services/` (business logic, no
  SQLAlchemy imports) → `repositories/` (SQLAlchemy queries only, no business logic) →
  `models/` (SQLAlchemy ORM). `schemas/` holds Pydantic request/response shapes, used by `api/`.
  `core/` holds cross-cutting concerns (config, DB session, error envelope, ID generation) and is
  importable repo-wide.
- **Wiring:** routers are included in `backend/app/main.py`.
- **IDs:** app-generated ULID strings as primary keys (`app/core/ids.py::new_id`) — set before
  insert, never DB auto-increment.
- **Errors:** unified JSON envelope `{"error": {"code", "message", "details"}}`, raised as
  `AppError` and handled centrally in `app/core/errors.py`.
- **Persistence:** SQLite as dumb storage (no triggers/stored logic); repositories own the
  SQLAlchemy session, services never import SQLAlchemy directly.
- **Migrations:** Alembic, versioned scripts under `backend/migrations/versions/`. Every schema
  change ships a paired forward + rollback migration.

## Frontend conventions

- Angular standalone components only, lazy-loaded per feature via `frontend/src/app/app.routes.ts`.
- `frontend/src/app/core/` — HTTP client setup and app-wide singletons.
- `frontend/src/app/shared/` — reusable components/pipes with no feature-specific logic.
- `frontend/src/app/features/<feature>/` — one folder per feature.
- Component-scoped SCSS per component; no third-party UI kit for MVP.
- State/data-fetching: Angular `HttpClient` directly from feature services — no state library yet.

## Testing

- Backend ships only a structural smoke test for now: `backend/tests/test_smoke.py` (app boots via
  `TestClient`, responds on `/health`). No broader unit/integration test convention is fixed yet —
  `plan-tests` should establish one before feature-level TDD begins.
- No CI workflow yet — builds/tests/lint run locally only.
- No UI design system yet — run `/sdd:design-system` once there's more than one feature's worth
  of UI.

## Running locally

Backend (verified working):

```
cd backend
python -m venv .venv && .venv/Scripts/activate  # or source .venv/bin/activate on macOS/Linux
pip install -e ".[dev]"
pytest
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend (structure only — **not yet verified**; this machine has no Node.js/npm/Angular CLI
installed, so `npm ci` / `ng serve` have not been run against this skeleton):

```
cd frontend
npm ci
ng serve
```
