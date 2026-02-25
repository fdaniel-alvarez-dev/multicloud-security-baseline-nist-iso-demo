from __future__ import annotations

from datetime import UTC, datetime

from msb.models import (
    Effort,
    Finding,
    FindingCategory,
    Iso27001ThemeMapping,
    MappedFinding,
    NistCsfMapping,
    Rating,
    RecommendedAction,
    Severity,
)
from msb.prioritization import build_backlog_and_roadmap


def _mapped_finding(
    *,
    finding_id: str,
    risk_score: float,
    effort: Effort,
    impact: int,
) -> MappedFinding:
    f = Finding(
        finding_id=finding_id,
        target_id="aws-prod",
        title="T",
        description="D",
        category=FindingCategory.iam,
        severity=Severity.high,
        likelihood=Rating.medium,
        impact=Rating.high,
        evidence={"signal": "x", "source": "y"},
        affected_assets=["a"],
        detection_source="unit-test",
        detected_at=datetime.now(tz=UTC),
        tags=[],
        references=[],
        recommended_actions=[
            RecommendedAction(
                action_id="A",
                title=f"Action {finding_id}",
                description="X",
                effort=effort,
                expected_impact=impact,
                dependencies=[],
                owner="Security",
            )
        ],
    )
    return MappedFinding(
        finding=f,
        nist=[NistCsfMapping(function="Protect", category="PR.AC", rationale="x")],
        iso=[Iso27001ThemeMapping(theme_id="A.5", theme_name="Access control", rationale="x")],
        risk_score=risk_score,
        domain="IAM",
    )


def test_prioritization_orders_by_priority_score_then_stable_id() -> None:
    mf1 = _mapped_finding(finding_id="F-1", risk_score=30.0, effort=Effort.small, impact=3)
    mf2 = _mapped_finding(finding_id="F-2", risk_score=40.0, effort=Effort.medium, impact=3)
    mf3 = _mapped_finding(finding_id="F-3", risk_score=30.0, effort=Effort.small, impact=3)

    backlog, roadmap = build_backlog_and_roadmap([mf2, mf3, mf1])
    assert backlog.headers[0] == "item_id"
    assert len(roadmap.rows) == 4

    # mf1 and mf3 have same risk/effort/impact, so their tie-break should be stable by item_id.
    item_ids = [r[0] for r in backlog.rows[:3]]
    assert item_ids[0] in {"F-1:A", "F-3:A"}
    assert item_ids[1] in {"F-1:A", "F-3:A"}
    assert item_ids[0] < item_ids[1]
