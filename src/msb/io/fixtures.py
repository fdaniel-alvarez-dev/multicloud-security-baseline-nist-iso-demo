from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from msb.models import Finding, Target


@dataclass(frozen=True)
class FixturePack:
    targets: list[Target]
    findings: list[Finding]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_fixture_pack(root: Path) -> FixturePack:
    targets_path = root / "targets.json"
    findings_path = root / "findings.json"
    if not targets_path.exists():
        raise ValueError(f"Missing fixtures file: {targets_path}")
    if not findings_path.exists():
        raise ValueError(f"Missing fixtures file: {findings_path}")

    targets_obj = _load_json(targets_path)
    findings_obj = _load_json(findings_path)

    targets = [Target.model_validate(x) for x in targets_obj["targets"]]
    findings = [Finding.model_validate(x) for x in findings_obj["findings"]]

    target_ids = {t.target_id for t in targets}
    unknown = sorted({f.target_id for f in findings} - target_ids)
    if unknown:
        raise ValueError(f"Findings reference unknown target_id(s): {unknown}")

    return FixturePack(targets=targets, findings=findings)
