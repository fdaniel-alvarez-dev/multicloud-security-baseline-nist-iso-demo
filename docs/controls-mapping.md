# Controls Mapping (High-Level, Practical)

This repo maps normalized findings to:
- **NIST Cybersecurity Framework (CSF)** Functions + Categories (practical subset)
- **ISO 27001** control themes (high-level themes, not a full attestation catalog)

## Why themes (not audit checklists)?
For a baseline assessment and roadmap, the goal is to:
- Communicate posture in a framework language stakeholders recognize
- Preserve traceability from “finding → theme → remediation”
- Avoid false claims of audit-grade certification readiness

## How mapping works
Mapping is driven by explicit mapping data:
- `src/msb/mappings/data/finding_category_to_controls.json`

The mapping engine:
- selects NIST CSF function/category + ISO theme per finding category
- includes a short rationale for traceability in reports and exports

See `src/msb/mappings/mapper.py`.
