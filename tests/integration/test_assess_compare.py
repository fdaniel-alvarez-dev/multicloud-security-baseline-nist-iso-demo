from __future__ import annotations

from pathlib import Path

from msb.compare import compare_summaries
from msb.io.fixtures import load_fixture_pack
from msb.scoring import assess_fixture_pack


def test_before_after_improvement_is_about_30_percent() -> None:
    root = Path(__file__).resolve().parents[2]
    before_pack = load_fixture_pack(root / "fixtures" / "before")
    after_pack = load_fixture_pack(root / "fixtures" / "after")

    before = assess_fixture_pack(before_pack).model_dump(mode="json")
    after = assess_fixture_pack(after_pack).model_dump(mode="json")
    comp = compare_summaries(before, after)

    pct = float(comp["org"]["posture"]["percent_change"])
    assert 29.0 <= pct <= 31.0
