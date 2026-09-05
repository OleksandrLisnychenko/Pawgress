---
status: Living
updated_at: "2026-09-05"
---

# Domain Context — Pawgress

## Glossary

- Category — one of exactly three fixed values (Basic, Household, Socialization) assigned to a Skill at creation and never changed. NOT Status (Status changes over time; Category is an enum-like classification fixed at creation — both are fixed-vocabulary tags on a Skill, easy to conflate).
- Owner — the single puppy owner, the sole actor of the app. NOT a professional trainer (Owner trains their own puppy; they are not a professional managing multiple clients).
- Skill — a named command or habit the owner wants the puppy to learn, belongs to exactly one fixed Category. NOT a Journal entry (a Journal entry records one training session against a Skill; the Skill itself is the thing being trained).
- Status — the current stage of a Skill's training funnel; one of exactly four fixed values in order: Planned, In Progress, Consolidating, Mastered. Every new Skill starts at Planned (skill-catalog); moving it forward or backward through the other three values is done by the separate status-tracking feature (roadmap step 3), not by skill-catalog. NOT Category (Category is fixed at creation and never changes; Status changes over time — the two are easy to conflate as both are fixed-vocabulary tags on a Skill).
