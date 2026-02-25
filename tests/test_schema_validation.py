from __future__ import annotations

import json
from pathlib import Path

import pytest

from msb.io.fixtures import load_fixture_pack


def test_fixture_pack_rejects_unknown_target_id(tmp_path: Path) -> None:
    root = tmp_path / "fixtures"
    root.mkdir(parents=True)
    (root / "targets.json").write_text(
        json.dumps(
            {
                "targets": [
                    {
                        "target_id": "aws-prod",
                        "provider": "aws",
                        "environment": "prod",
                        "region": "us-east-1",
                        "owner": "x",
                        "assets": [],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (root / "findings.json").write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "schema_version": "1.0",
                        "finding_id": "F-1",
                        "target_id": "does-not-exist",
                        "title": "x",
                        "description": "x",
                        "category": "IAM",
                        "severity": "low",
                        "likelihood": "low",
                        "impact": "low",
                        "evidence": {"signal": "x", "source": "y"},
                        "affected_assets": [],
                        "detection_source": "unit-test",
                        "detected_at": "2026-02-01T00:00:00Z",
                        "tags": [],
                        "references": [],
                        "recommended_actions": [
                            {
                                "action_id": "A-1",
                                "title": "x",
                                "description": "x",
                                "effort": "S",
                                "expected_impact": 1,
                                "dependencies": [],
                                "owner": "x",
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unknown target_id"):
        load_fixture_pack(root)
