---
status: Draft
owner: "Oleksandr Lisnychenko"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-09-05"
feature_size: "S"
---

# Spec — skill-catalog

> **Glossary:** [CONTEXT](../../../CONTEXT.md)
> **Reference module / docs / channels used:** None — only the interview + CONTEXT + `docs/idea-brief.md` + `docs/architecture-map.md` + `docs/roadmap.md`.

## 1. Context

Right now the puppy owner keeps no record at all of what commands or skills they want to teach their puppy — nothing exists today (`docs/idea-brief.md` §2 Problem). This is the first buildable slice of Pawgress: it lets the Owner add a named skill under one of three fixed categories and see it listed, giving them one durable place for the list that currently lives nowhere.

This is the anchor step of the MVP roadmap (`docs/roadmap.md` step 2 "Skill/command catalog"): the status-tracking and training-journal features that come next both attach to skills that must already exist in this catalog, so nothing else in the roadmap can be built before this slice.

The committed approach: the Owner manually adds a skill by giving it a name and one of the three fixed categories (Basic, Household, Socialization); the category is fixed at creation and never changes. The skill's name must be unique within its own category (exact match, after trimming leading/trailing whitespace) — a duplicate is rejected rather than silently created. Every new skill is stored with an explicit status attribute drawn from the four-stage training funnel — Planned, In Progress, Consolidating, Mastered — and starts at the initial value Planned; moving it through the other three values belongs to the separate status-tracking feature (roadmap step 3), not this slice. The catalog view groups skills under their category in the order they were added. Editing and deleting a skill are explicitly out of this slice.

**Decision override:** a failure-mode analysis during ideation found that allowing duplicate names with no way to delete them would make identical entries permanently indistinguishable once the status-tracking and training-journal features start attaching data to them (an accidental double-tap or typo becomes unremovable garbage forever). Rather than adding delete/edit to this slice to compensate, per-category name uniqueness at creation is enforced instead — see AC-03.

**Decision override:** the critic flagged that this uniqueness guard (AC-03) does not itself guarantee atomicity against two near-simultaneous identical submissions (e.g. a double-tap) both passing the check before either is recorded. Given this is a single local Owner with no concurrent multi-client access in this slice, that race is accepted as a known, low-probability risk rather than specified against — revisit if the app ever gains concurrent access.

**Decision override (clarify, 2026-09-05):** AC-04 reads as if it guards against more than one Owner/catalog, which would contradict §3's exclusion of multi-owner scoping. Resolved as a no-op for this slice: this MVP has exactly one dog, one Owner, and no authentication, so exactly one catalog exists and can ever exist — no other catalog is addressable, so no access-control mechanism is required to satisfy US-05. Revisit if the app ever gains multiple owners or dogs.

## 2. Goals

- Every command/skill the Owner wants to teach lives in one durable, categorized list instead of nowhere.
- The catalog gives each skill a stable, unambiguous identity within its category, so the status-tracking and training-journal features can attach to it reliably.

## 3. Non-goals

- Editing or deleting a skill after creation — deferred to a later feature; keeps this slice small and makes the per-category uniqueness guard (AC-03) actually matter.
- Custom/user-defined categories — the three categories are fixed (`docs/idea-brief.md` §5 Out of scope).
- Command/skill ordering or prerequisites (a training-plan sequence) — `docs/idea-brief.md` §5 Out of scope; every catalog item is independent.
- Multi-pet or multi-owner scoping — `docs/idea-brief.md` §5 Out of scope; the catalog belongs to exactly one implicit Owner.
- Moving a skill's status after creation — deferred to the status-tracking feature (roadmap step 3); this slice only ever sets a new skill's status to its initial value, Planned.

## 4. User stories

### US-01: Add a skill

**As a** Owner
**I want** to add a skill with a name and one of the three fixed categories
**So that** it becomes part of my puppy's training catalog

### US-02: View catalog grouped by category

**As a** Owner
**I want** to see my skills grouped under their fixed category, in the order I added them
**So that** I can find and review what I'm teaching without hunting through an unsorted list

### US-03: Avoid confusing duplicates

**As a** Owner
**I want** to be stopped from creating a skill whose name is an exact duplicate of one I already have in the same category
**So that** my catalog never ends up with entries I can't tell apart

### US-04: Get clear feedback on invalid input

**As a** Owner
**I want** to understand why an attempt to add a skill failed
**So that** I can fix my input and move on without guessing

### US-05: Trust catalog is exclusively mine

**As a** Owner
**I want** the catalog to only ever show and accept changes to my own puppy's skills
**So that** I never see or accidentally affect data that isn't mine

### US-06: New skill is ready for status-tracking

**As a** Owner
**I want** every skill I add to start in a state the future status-tracking feature already recognizes
**So that** I can immediately begin moving it through training stages once that feature exists

## 5. Acceptance criteria

### AC-01 (US-01) — happy path

**Given** the Owner is adding a skill
**When** the Owner submits a non-empty name and one of the three fixed categories
**Then** the system records the skill in the catalog with initial status Planned, confirms it to the Owner, and the skill appears under its category heading in the catalog view

### AC-02 (US-04) — error

**Given** the Owner is adding a skill
**When** the Owner submits a name that, after trimming leading and trailing whitespace, is empty
**Then** the system blocks the creation and tells the Owner the name cannot be empty

### AC-03 (US-03) — domain invariant

**Given** the catalog already contains a skill with a given name (exact match after trimming leading/trailing whitespace — internal spacing and letter case are not normalized) in a given category
**When** the Owner attempts to add another skill with that same name in that same category
**Then** the system blocks the creation and tells the Owner that name already exists in that category

### AC-04 (US-05) — authorization

**Given** this slice supports exactly one Owner and exactly one catalog, with no way to create or address another
**When** the Owner views or adds to the catalog
**Then** there is no other catalog for the system to expose or accept changes to — cross-owner exposure cannot occur in this slice, and no additional access-control step is required

### AC-05 (US-06) — cross-context

**Given** every skill's status is drawn from the four-stage training funnel (Planned, In Progress, Consolidating, Mastered) that the separate status-tracking feature will let the Owner move it through
**When** the Owner adds a new skill
**Then** the system assigns that skill the status Planned — the funnel's fixed starting value — so it is immediately valid input for the status-tracking feature once it exists

### AC-06 (US-02) — happy path

**Given** the catalog contains skills in zero or more of the three fixed categories
**When** the Owner opens the catalog view
**Then** the system displays all three category headings, always, each populated with its skills in the order they were added (or empty if it has none), and returns every skill in the catalog with no paging

### AC-07 (US-04) — error

**Given** the Owner is adding a skill
**When** the Owner submits a category that is missing or is not one of the three fixed categories
**Then** the system blocks the creation and tells the Owner the category must be one of the three fixed categories

## 6. Non-functional requirements

<!-- N/A: MVP speed is the explicit priority for this slice (see `docs/architecture-map.md` Constraints) — this is a single-local-user tool with no production load yet; numeric performance targets are deferred until real usage exists rather than invented now. -->

## 6.1 Security / privacy

<!-- N/A: internal single-user tool — no PII beyond names the Owner types themselves, no new authz boundary (single implicit Owner, no login in this MVP), no external exposure. See `docs/architecture-map.md` Constraints for the deferred CI/test-suite context this rides on. -->

## 7. Metrics / KPIs

<!-- N/A: MVP speed is the explicit priority for this slice — usage metrics are not being instrumented before the feature has real usage to measure. -->

## 8. Open questions

<!-- none — the two candidate open questions from drafting (name-normalization for the uniqueness check; a catalog-size warning threshold) were resolved by taking the stated defaults directly into scope rather than deferring: no size limit or warning is imposed on the catalog in this slice, and no maximum length is imposed on a skill name beyond the non-empty check (AC-02). AC-03's comparison was refined during /sdd:clarify on 2026-09-05: exact match after trimming leading/trailing whitespace (still no case or internal-whitespace normalization) — see AC-02/AC-03. -->
