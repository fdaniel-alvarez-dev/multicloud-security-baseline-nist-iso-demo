from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def render_markdown_report(
    *,
    title: str,
    author: str | None,
    compare_obj: dict[str, Any],
    remediation_backlog_csv_path: Path,
    roadmap_csv_path: Path,
    controls_coverage_csv_path: Path,
) -> str:
    backlog = _read_csv(remediation_backlog_csv_path)
    roadmap = _read_csv(roadmap_csv_path)
    coverage = _read_csv(controls_coverage_csv_path)

    org = compare_obj["org"]["posture"]
    deltas = compare_obj["org"]["domain_posture_deltas"]

    lines: list[str] = []
    lines.append(f"# {title}")
    if author:
        lines.append(f"_Author: {author}_")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(
        f"- Org posture: **{org['before']:.1f} → {org['after']:.1f}** "
        f"(**{org['delta']:+.1f}**, {org['percent_change']:+.1f}%)."
    )
    lines.append(
        "- This is a safe, offline simulation using synthetic fixtures (no cloud credentials, no scanning)."
    )
    lines.append("")
    lines.append("## Domain Improvements (Org)")
    lines.append("| Domain | Before | After | Delta |")
    lines.append("|---|---:|---:|---:|")
    for r in deltas:
        lines.append(
            f"| {r['domain']} | {r['before']:.1f} | {r['after']:.1f} | {r['delta']:+.1f} |"
        )
    lines.append("")

    lines.append("## Remediation Backlog (Top 10)")
    lines.append("| Priority | Item | Target | Domain | Risk | Effort | Phase |")
    lines.append("|---:|---|---|---|---:|---|---|")
    for idx, row in enumerate(backlog[:10], start=1):
        lines.append(
            f"| {idx} | {row['item_id']} | {row['target_id']} | {row['domain']} | "
            f"{float(row['risk_score']):.2f} | {row['effort']} | {row['phase']} |"
        )
    lines.append("")

    lines.append("## Roadmap (Phased Plan)")
    lines.append("| Phase | Focus | Why now | Example items |")
    lines.append("|---|---|---|---|")
    for row in roadmap:
        lines.append(
            f"| {row['phase']} | {row['focus']} | {row['why_now']} | {row['example_items']} |"
        )
    lines.append("")

    lines.append("## Framework Coverage Summary")
    lines.append("| Framework | Control theme | Findings |")
    lines.append("|---|---|---:|")
    for row in coverage[:20]:
        lines.append(f"| {row['framework']} | {row['control_theme']} | {row['finding_count']} |")
    lines.append("")

    return "\n".join(lines).strip() + "\n"


def render_html_report(
    *,
    title: str,
    author: str | None,
    compare_obj: dict[str, Any],
    remediation_backlog_csv_path: Path,
    roadmap_csv_path: Path,
    controls_coverage_csv_path: Path,
) -> str:
    env = Environment(
        loader=PackageLoader("msb.reporting", "templates"),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("report.html.j2")

    backlog = _read_csv(remediation_backlog_csv_path)
    roadmap = _read_csv(roadmap_csv_path)
    coverage = _read_csv(controls_coverage_csv_path)

    return template.render(
        title=title,
        author=author,
        org=compare_obj["org"]["posture"],
        domain_deltas=compare_obj["org"]["domain_posture_deltas"],
        backlog=backlog[:25],
        roadmap=roadmap,
        coverage=coverage[:40],
    )
