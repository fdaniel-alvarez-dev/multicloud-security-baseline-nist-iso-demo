# Findings Schema (v1.0)

This repository uses a strict, versioned findings schema to normalize posture signals across simulated AWS, Azure, and GCP targets.

## `Finding` (core fields)
- `schema_version`: fixed to `"1.0"` for this demo
- `finding_id`: stable identifier (e.g., `F-001`)
- `target_id`: which simulated target the finding belongs to (e.g., `aws-prod`)
- `title`, `description`
- `category`: one of:
  - `IAM`
  - `Logging/Monitoring`
  - `Network Controls`
  - `Governance`
  - `Asset Inventory`
  - `Data Protection`
- `severity`: `low | medium | high | critical`
- `likelihood`: `low | medium | high`
- `impact`: `low | medium | high`
- `evidence`: synthetic key/value details used to justify the finding (safe and non-sensitive)
- `affected_assets`: list of asset IDs within the target
- `detection_source`: fixture path for traceability (local-only)
- `detected_at`: ISO timestamp
- `tags`: free-form keywords (e.g., `mfa`, `rotation`, `segmentation`)
- `references`: high-level references (no direct exploitation steps)
- `recommended_actions`: one or more structured remediation actions

## `RecommendedAction`
- `action_id`: stable identifier within the finding
- `title`, `description`
- `effort`: `S | M | L` (small/medium/large)
- `expected_impact`: 1–5
- `dependencies`: list of short dependency strings (used for prioritization)
- `owner`: ownership hint (e.g., Security, Platform, Governance)

Schema is implemented in `src/msb/models.py`.
