---
status: Draft
owner: "Oleksandr Lisnychenko"
updated_at: "2026-09-05"
depth: "medium"
---

# Idea brief — pawgress-tracker

## 1. Raw idea

Pawgress — це трекер виховання та дресирування цуценяти. Додаток дозволяє вести список команд та навичок за категоріями (Базові, Побутові, Соціалізація), змінювати їхні статуси (Заплановано -> У процесі -> Закріплено -> Вивчено) та фіксувати журнал тренувань (дата, кількість успішних спроб, коментар). Стек: FastAPI (SQLite) + Angular.

## 2. Problem

Right now the owner keeps no record at all of what they're training their puppy on or how it's going — training happens "from memory," so it's hard to tell what's already reinforced versus what's stalled. There is no existing tool being replaced (not a notebook, not a spreadsheet); the gap is the complete absence of any tracking today.

## 3. Users

A single puppy owner training their own dog solo — not a professional trainer managing multiple clients, and not a household of several people coordinating training for one pet. MVP explicitly tracks one puppy per owner, no multi-pet or multi-user support.

## 4. Why now

There is no external trigger (no incident, no deadline) — this is a "would be nice to have" personal tool the owner wants for their own puppy's training. The motivation is self-generated: consolidate scattered, currently-nonexistent tracking into one place before training habits solidify without it.

## 5. Out of scope

- **Training-plan ordering / prerequisites between commands** (e.g., "Сидіти" must precede "Поряд") — deferred to a future phase; MVP treats each command/skill as an independent item with its own properties, no dependency graph.
- **Multi-pet support** — MVP tracks exactly one puppy per owner; a profile switcher and per-pet data model are out of scope.
- **Custom/user-defined categories** — the three categories (Базові, Побутові, Соціалізація) are fixed for MVP; no CRUD UI for categories.
- **Starter templates / suggested command library** — the owner always adds commands and skills manually from a blank list; no seeded content or onboarding suggestions.
- **Multi-user / shared household tracking** — one owner per puppy, no role management or sync between family members.

## 6. Risks

- **Unstructured journal comments limit self-analysis.** The training log's free-text comments (e.g., "займалися на вулиці, відволікався") are meant to let the owner spot patterns themselves, but the app does nothing to surface those patterns beyond a chronological list — assumes the owner will do that analysis manually; false if the log grows long enough that manual review stops being practical.
- **Status regression changes the meaning of "Вивчено."** Statuses can move backward (e.g., a puppy that starts forgetting a "Закріплено" skill can be moved back to "У процесі"), which better reflects real training but means status history is not a simple funnel — any reporting built on top of statuses later must account for non-monotonic transitions.
- **Attempt counts without context were originally ambiguous** — a raw "successful attempts" number meant different things depending on the unknown total attempts. Resolved during the interview: each journal entry now records both successful and total attempts, but this makes the entry-writing step slightly heavier than a single number.
- **Success-rate trend was pulled into MVP scope**, which cuts against the "keep MVP thin" bias applied everywhere else in this brief — worth watching that this doesn't invite scope creep into further auto-analysis (e.g., recommendations, alerts) before the core tracking loop is validated.

## 7. Recommendation

Build the MVP as a single-owner, single-puppy tracker: a manually-curated, flat list of commands/skills across three fixed categories, each with a status that can move both forward and backward through Заплановано → У процесі → Закріплено → Вивчено, plus a per-skill training journal (date, successful/total attempts, free-text comment) and an auto-computed success-rate trend derived from that journal. Keep everything else — ordering/dependencies between commands, multi-pet support, custom categories, and starter templates — deliberately out, and treat command sequencing as the clearest candidate for a v2 "training plan" feature once the core tracking loop proves useful.

## 8. Open questions

- Should the success-rate trend be a simple aggregate (e.g., percentage over all logged attempts) or a rolling/time-windowed trend? — owner, before `specify`.
- What should happen to journal history and success-rate data when a skill's status regresses — kept as-is, annotated, or reset? — owner, before `specify`.
