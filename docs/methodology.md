# Methodology (Consulting-Style)

This repo simulates a multi-cloud baseline engagement in a safe, offline, reproducible way using fixtures.

## Engagement goals
1) Establish a consistent baseline across clouds (normalized categories and severity language).
2) Translate technical gaps into governance-ready reporting (NIST CSF + ISO 27001 themes).
3) Prioritize remediation with a pragmatic framework (risk, effort, impact, dependencies, blast radius).

## Guardrails (Safety Boundary)
- No real credentials.
- No live cloud access.
- No scanning or probing any targets.
- All findings and evidence are synthetic and included as local fixtures.

## What “posture score” means here
Posture is a deterministic score (0–100) derived from a weighted risk penalty computed from findings.

The model is designed to be:
- Explainable (weights are explicit)
- Stable (deterministic inputs -> deterministic outputs)
- Testable (unit + integration tests validate expected properties)

See `src/msb/scoring/assess.py` and `src/msb/scoring/risk.py`.
