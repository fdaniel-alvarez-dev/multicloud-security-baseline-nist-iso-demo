from __future__ import annotations

import json
from importlib.resources import files
from typing import cast

from msb.models import (
    Finding,
    Iso27001ThemeMapping,
    NistCsfMapping,
)


def _mapping_data() -> dict[str, object]:
    path = files("msb.mappings.data").joinpath("finding_category_to_controls.json")
    raw: str = path.read_text(encoding="utf-8")
    return cast(dict[str, object], json.loads(raw))


def map_finding(finding: Finding) -> tuple[list[NistCsfMapping], list[Iso27001ThemeMapping]]:
    data = _mapping_data()
    key = finding.category.value
    entry = data.get(key)
    if entry is None:
        return (
            [
                NistCsfMapping(
                    function="Identify", category="ID.GV (Governance)", rationale="Default mapping."
                )
            ],
            [
                Iso27001ThemeMapping(
                    theme_id="A.6",
                    theme_name="Information security governance",
                    rationale="Default mapping.",
                )
            ],
        )

    nist = [NistCsfMapping.model_validate(x) for x in entry["nist"]]  # type: ignore[index]
    iso = [Iso27001ThemeMapping.model_validate(x) for x in entry["iso"]]  # type: ignore[index]
    return nist, iso
