from __future__ import annotations

from datetime import UTC, datetime

from msb.models import Effort, Finding, FindingCategory, Rating, RecommendedAction, Severity
from msb.scoring.risk import risk_score_for_finding


def test_risk_score_is_deterministic() -> None:
    finding = Finding(
        finding_id="F-1",
        target_id="aws-prod",
        title="Root MFA not enforced",
        description="Test",
        category=FindingCategory.iam,
        severity=Severity.high,
        likelihood=Rating.medium,
        impact=Rating.high,
        evidence={"signal": "mfa=false", "source": "synthetic"},
        affected_assets=["iam-root"],
        detection_source="unit-test",
        detected_at=datetime.now(tz=UTC),
        tags=["mfa"],
        references=[],
        recommended_actions=[
            RecommendedAction(
                action_id="A-1",
                title="Enable MFA",
                description="Enable MFA",
                effort=Effort.small,
                expected_impact=5,
                dependencies=[],
                owner="Security",
            )
        ],
    )

    # high(6) * medium(2) * high(3) * iam_weight(1.25) = 45.0
    assert risk_score_for_finding(finding) == 45.0
