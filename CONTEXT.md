---
status: Living
updated_at: "2026-09-05"
---

# Domain Context — Pawgress

## Glossary

- Category — one of exactly three fixed values (Basic, Household, Socialization) assigned to a Skill at creation and never changed. NOT Status (Status changes over time; Category is an enum-like classification fixed at creation — both are fixed-vocabulary tags on a Skill, easy to conflate).
- Owner — the single puppy owner, the sole actor of the app. NOT a professional trainer (Owner trains their own puppy; they are not a professional managing multiple clients).
- Skill — a named command or habit the owner wants the puppy to learn, belongs to exactly one fixed Category. NOT a Journal entry (a Journal entry records one training session against a Skill; the Skill itself is the thing being trained).
