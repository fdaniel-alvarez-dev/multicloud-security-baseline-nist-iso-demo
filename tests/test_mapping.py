from __future__ import annotations

from datetime import UTC, datetime

from msb.mappings import map_finding
from msb.models import Effort, Finding, FindingCategory, Rating, RecommendedAction, Severity


def test_map_finding_iam_contains_expected_themes() -> None:
    finding = Finding(
        finding_id="F-X",
        target_id="aws-prod",
        title="Test",
        description="Test",
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
                action_id="A-X",
                title="Do thing",
                description="Do thing",
                effort=Effort.small,
                expected_impact=3,
                dependencies=[],
                owner="Security",
            )
        ],
    )

    nist, iso = map_finding(finding)
    assert any(m.function == "Protect" for m in nist)
    assert any("PR.AC" in m.category for m in nist)
    assert any(m.theme_id == "A.5" for m in iso)
