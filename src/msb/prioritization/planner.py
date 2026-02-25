from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from msb.models import Effort, MappedFinding


@dataclass(frozen=True)
class CsvTable:
    headers: list[str]
    rows: list[list[str]]

    def to_rows(self) -> list[list[str]]:
        return self.rows


def build_backlog_and_roadmap(mapped_findings: list[MappedFinding]) -> tuple[CsvTable, CsvTable]:
    backlog_rows: list[dict[str, str | float | int]] = []

    for mf in mapped_findings:
        for action in mf.finding.recommended_actions:
            effort_num = _effort_to_num(action.effort)
            impact = float(action.expected_impact)
            deps = len(action.dependencies)
            blast_radius = max(1, len(mf.finding.affected_assets))

            risk = float(mf.risk_score) * (1.0 + 0.05 * (blast_radius - 1))
            priority = (risk * impact) / effort_num
            priority *= 0.92**deps

            quick_win = effort_num <= 2 and risk >= 20.0
            phase = _phase_for(risk=risk, effort_num=effort_num)

            backlog_rows.append(
                {
                    "item_id": f"{mf.finding.finding_id}:{action.action_id}",
                    "target_id": mf.finding.target_id,
                    "domain": mf.domain,
                    "finding_title": mf.finding.title,
                    "action_title": action.title,
                    "risk_score": risk,
                    "impact_1_to_5": int(impact),
                    "effort": action.effort.value,
                    "dependencies": ",".join(action.dependencies),
                    "owner": action.owner,
                    "quick_win": "yes" if quick_win else "no",
                    "phase": phase,
                    "priority_score": priority,
                    "rationale": _rationale(
                        mf=mf, effort_num=effort_num, impact=impact, deps=deps, blast=blast_radius
                    ),
                }
            )

    backlog_rows.sort(key=lambda r: (-float(r["priority_score"]), str(r["item_id"])))

    backlog_table = _as_csv_table(
        backlog_rows,
        headers=[
            "item_id",
            "target_id",
            "domain",
            "finding_title",
            "action_title",
            "risk_score",
            "impact_1_to_5",
            "effort",
            "dependencies",
            "owner",
            "quick_win",
            "phase",
            "priority_score",
            "rationale",
        ],
        formatters={
            "risk_score": lambda v: f"{float(v):.2f}",
            "priority_score": lambda v: f"{float(v):.3f}",
        },
    )

    roadmap_rows = _roadmap_from_backlog(backlog_rows)
    roadmap_table = _as_csv_table(
        roadmap_rows,
        headers=["phase", "focus", "why_now", "example_items", "notes"],
        formatters={},
    )

    return backlog_table, roadmap_table


def _phase_for(*, risk: float, effort_num: int) -> str:
    if risk >= 30.0 and effort_num <= 2:
        return "Phase 0 (Immediate)"
    if risk >= 25.0:
        return "Phase 1 (0-30 days)"
    if risk >= 15.0:
        return "Phase 2 (30-90 days)"
    return "Phase 3 (90-180 days)"


def _effort_to_num(effort: Effort) -> int:
    return {Effort.small: 1, Effort.medium: 3, Effort.large: 5}[effort]


def _rationale(*, mf: MappedFinding, effort_num: int, impact: float, deps: int, blast: int) -> str:
    return (
        f"Risk is driven by {mf.finding.severity.value} severity and {mf.domain} control gap; "
        f"impact={int(impact)}/5, effort≈{effort_num}, deps={deps}, blast_radius≈{blast} assets."
    )


def _as_csv_table(
    rows: Iterable[dict[str, str | float | int]],
    headers: list[str],
    formatters: dict[str, Callable[[str | float | int], str]],
) -> CsvTable:
    formatted: list[list[str]] = []
    for r in rows:
        out_row: list[str] = []
        for h in headers:
            v = r.get(h, "")
            if h in formatters:
                out_row.append(formatters[h](v))
            else:
                out_row.append(str(v))
        formatted.append(out_row)
    return CsvTable(headers=headers, rows=formatted)


def _roadmap_from_backlog(
    backlog_rows: list[dict[str, str | float | int]],
) -> list[dict[str, str | float | int]]:
    by_phase: dict[str, list[dict[str, str | float | int]]] = {}
    for r in backlog_rows:
        by_phase.setdefault(str(r["phase"]), []).append(r)

    phases = [
        "Phase 0 (Immediate)",
        "Phase 1 (0-30 days)",
        "Phase 2 (30-90 days)",
        "Phase 3 (90-180 days)",
    ]

    def _top_items(phase: str, n: int = 3) -> str:
        items = by_phase.get(phase, [])[:n]
        return " | ".join(str(i["item_id"]) for i in items) if items else ""

    roadmap: list[dict[str, str | float | int]] = []
    for phase in phases:
        roadmap.append(
            {
                "phase": phase,
                "focus": _focus_for_phase(phase),
                "why_now": _why_for_phase(phase),
                "example_items": _top_items(phase),
                "notes": "Phases are deterministic outputs of the prioritization model for demo purposes.",
            }
        )
    return roadmap


def _focus_for_phase(phase: str) -> str:
    return {
        "Phase 0 (Immediate)": "Stop the bleeding: high-risk, low-effort control gaps",
        "Phase 1 (0-30 days)": "Baseline hardening: IAM + logging coverage + exposure reduction",
        "Phase 2 (30-90 days)": "Depth and consistency: governance + network segmentation patterns",
        "Phase 3 (90-180 days)": "Optimization: scale controls, reduce toil, formalize guardrails",
    }[phase]


def _why_for_phase(phase: str) -> str:
    return {
        "Phase 0 (Immediate)": "Quick wins that materially reduce likelihood of account compromise and blind spots.",
        "Phase 1 (0-30 days)": "Build detection and access-control foundations for repeatable, compliant operations.",
        "Phase 2 (30-90 days)": "Address structural gaps and reduce risk from inconsistency across clouds.",
        "Phase 3 (90-180 days)": "Mature the program through automation and policy-driven governance.",
    }[phase]
