from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime

from msb.io.fixtures import FixturePack
from msb.mappings import map_finding
from msb.models import (
    AssessmentSummary,
    DomainMaturity,
    MappedFinding,
    OrgAssessment,
    TargetAssessment,
)
from msb.scoring.risk import domain_for_category, risk_score_for_finding


@dataclass(frozen=True)
class CoverageTable:
    headers: list[str]
    rows: list[list[str]]

    def to_rows(self) -> list[list[str]]:
        return self.rows


def assess_fixture_pack(pack: FixturePack) -> AssessmentSummary:
    mapped: list[MappedFinding] = []
    for finding in pack.findings:
        nist, iso = map_finding(finding)
        risk = risk_score_for_finding(finding)
        domain = domain_for_category(finding.category)
        mapped.append(
            MappedFinding(
                finding=finding,
                nist=nist,
                iso=iso,
                risk_score=risk,
                domain=domain,
            )
        )

    # Score per target
    per_target_findings: dict[str, list[MappedFinding]] = defaultdict(list)
    for mf in mapped:
        per_target_findings[mf.finding.target_id].append(mf)

    target_assessments: list[TargetAssessment] = []
    org_domain_penalty: dict[str, float] = defaultdict(float)

    for target in pack.targets:
        t_findings = per_target_findings.get(target.target_id, [])
        domain_penalty: dict[str, float] = defaultdict(float)
        total_penalty = 0.0
        for mf in t_findings:
            # Penalty increases slightly with number of affected assets (synthetic blast radius).
            penalty = mf.risk_score * (1.0 + 0.05 * max(0, len(mf.finding.affected_assets) - 1))
            domain_penalty[mf.domain] += penalty
            org_domain_penalty[mf.domain] += penalty
            total_penalty += penalty

        posture = _posture_score_from_penalty(total_penalty)
        domain_maturity = _domain_maturity(domain_penalty)
        target_assessments.append(
            TargetAssessment(
                target_id=target.target_id,
                provider=target.provider,
                environment=target.environment,
                posture_score=posture,
                domain_maturity=domain_maturity,
                finding_count=len(t_findings),
            )
        )

    org_posture = _posture_score_from_penalty(sum(org_domain_penalty.values()))
    org_domain_maturity = _domain_maturity(org_domain_penalty)

    return AssessmentSummary(
        assessed_at=datetime.now(tz=UTC),
        org=OrgAssessment(posture_score=org_posture, domain_maturity=org_domain_maturity),
        targets=sorted(target_assessments, key=lambda x: x.target_id),
        mapped_findings=sorted(mapped, key=lambda x: (x.finding.target_id, x.finding.finding_id)),
    )


def _posture_score_from_penalty(total_penalty: float) -> float:
    # Deterministic scaling chosen to keep scores in a realistic consulting range.
    # Higher penalty => lower posture score.
    normalization = 450.0
    score = 100.0 - (min(total_penalty, normalization) / normalization) * 100.0
    return max(0.0, min(100.0, score))


def _domain_maturity(domain_penalty: dict[str, float]) -> list[DomainMaturity]:
    result: list[DomainMaturity] = []
    for domain, penalty in sorted(domain_penalty.items()):
        posture = _posture_score_from_penalty(penalty)
        maturity = (posture / 100.0) * 5.0
        result.append(
            DomainMaturity(domain=domain, maturity_0_to_5=maturity, posture_0_to_100=posture)
        )
    return result


def compute_controls_coverage(mapped_findings: list[MappedFinding]) -> CoverageTable:
    nist_counts: Counter[str] = Counter()
    iso_counts: Counter[str] = Counter()
    for mf in mapped_findings:
        for n in mf.nist:
            nist_counts[f"{n.function} | {n.category}"] += 1
        for i in mf.iso:
            iso_counts[f"{i.theme_id} | {i.theme_name}"] += 1

    rows: list[list[str]] = []
    for k, v in nist_counts.most_common():
        rows.append(["NIST CSF", k, str(v)])
    for k, v in iso_counts.most_common():
        rows.append(["ISO 27001 Theme", k, str(v)])

    return CoverageTable(headers=["framework", "control_theme", "finding_count"], rows=rows)
