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

## Backend has two separate venvs

The API runtime and the migration tooling deliberately have **separate virtualenvs with separate
requirements files** — `backend/migrations/env.py` only imports `app.core.db` and `app.models`
(no FastAPI/Pydantic), so Alembic never needs the full API dependency set.

- `backend/app/.venv` + `backend/app/requirements.txt` — fastapi, uvicorn, sqlalchemy, pydantic,
  python-ulid, pytest, httpx. Used to run and test the API.
- `backend/migrations/.venv` + `backend/migrations/requirements.txt` — alembic, sqlalchemy,
  python-ulid only. Used to run migrations.

Both venvs are invoked from the `backend/` directory (not from inside `app/` or `migrations/`) so
the `app` package resolves as a top-level import and `alembic.ini` (at `backend/alembic.ini`) is
found.

## Running locally

Backend (verified working):

```
cd backend

# one-time setup
python -m venv app/.venv && app/.venv/Scripts/pip install -r app/requirements.txt
python -m venv migrations/.venv && migrations/.venv/Scripts/pip install -r migrations/requirements.txt

# run tests
app/.venv/Scripts/python -m pytest

# run migrations
migrations/.venv/Scripts/python -m alembic upgrade head

# run the API
app/.venv/Scripts/python -m uvicorn app.main:app --reload
```

Frontend (structure only — **not yet verified**; this machine has no Node.js/npm/Angular CLI
installed, so `npm ci` / `ng serve` have not been run against this skeleton):

```
cd frontend
npm ci
ng serve
```
