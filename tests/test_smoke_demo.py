from __future__ import annotations

from pathlib import Path

import pytest

from msb.demo_flow import run_demo


@pytest.mark.smoke
def test_demo_flow_generates_expected_artifacts(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    artifacts_dir = tmp_path / "artifacts"

    run_demo(fixtures_dir=root / "fixtures", artifacts_dir=artifacts_dir)

    assert (artifacts_dir / "before" / "summary.json").exists()
    assert (artifacts_dir / "after" / "summary.json").exists()
    assert (artifacts_dir / "compare" / "compare.json").exists()
    assert (artifacts_dir / "report" / "report.md").exists()
    assert (artifacts_dir / "report" / "report.html").exists()
