# Multi-Cloud Security Baseline Report (Demo)
_Author: Cloud Security / DevSecOps Consultant_

## Executive Summary
- Org posture: **57.5 → 74.8** (**+17.3**, +30.1%).
- This is a safe, offline simulation using synthetic fixtures (no cloud credentials, no scanning).

## Domain Improvements (Org)
| Domain | Before | After | Delta |
|---|---:|---:|---:|
| IAM | 90.0 | 94.8 | +4.8 |
| Network Controls | 95.0 | 96.6 | +1.7 |
| Asset Inventory | 97.6 | 98.8 | +1.2 |
| Logging/Monitoring | 84.6 | 84.6 | +0.0 |
| Data Protection | 90.3 | 0.0 | -90.3 |

## Remediation Backlog (Top 10)
| Priority | Item | Target | Domain | Risk | Effort | Phase |
|---:|---|---|---|---:|---|---|
| 1 | F-002:A-002 | aws-prod | Logging/Monitoring | 41.58 | M | Phase 1 (0-30 days) |
| 2 | F-007:A-007 | azure-prod | Logging/Monitoring | 27.72 | M | Phase 1 (0-30 days) |
| 3 | F-008:A-008 | aws-prod | IAM | 23.62 | M | Phase 2 (30-90 days) |
| 4 | F-003:A-003 | aws-dev | Network Controls | 15.12 | M | Phase 2 (30-90 days) |
| 5 | F-006:A-006 | aws-prod | Asset Inventory | 5.40 | M | Phase 3 (90-180 days) |

## Roadmap (Phased Plan)
| Phase | Focus | Why now | Example items |
|---|---|---|---|
| Phase 0 (Immediate) | Stop the bleeding: high-risk, low-effort control gaps | Quick wins that materially reduce likelihood of account compromise and blind spots. |  |
| Phase 1 (0-30 days) | Baseline hardening: IAM + logging coverage + exposure reduction | Build detection and access-control foundations for repeatable, compliant operations. | F-002:A-002 | F-007:A-007 |
| Phase 2 (30-90 days) | Depth and consistency: governance + network segmentation patterns | Address structural gaps and reduce risk from inconsistency across clouds. | F-008:A-008 | F-003:A-003 |
| Phase 3 (90-180 days) | Optimization: scale controls, reduce toil, formalize guardrails | Mature the program through automation and policy-driven governance. | F-006:A-006 |

## Framework Coverage Summary
| Framework | Control theme | Findings |
|---|---|---:|
| NIST CSF | Detect | DE.CM (Security Continuous Monitoring) | 2 |
| NIST CSF | Respond | RS.AN (Analysis) | 2 |
| NIST CSF | Protect | PR.PT (Protective Technology) | 1 |
| NIST CSF | Identify | ID.AM (Asset Management) | 1 |
| NIST CSF | Protect | PR.AC (Identity Management, Authentication, and Access Control) | 1 |
| NIST CSF | Identify | ID.GV (Governance) | 1 |
| ISO 27001 Theme | A.8 | Logging and monitoring | 2 |
| ISO 27001 Theme | A.7 | Network security | 1 |
| ISO 27001 Theme | A.5 | Asset management | 1 |
| ISO 27001 Theme | A.5 | Access control | 1 |
