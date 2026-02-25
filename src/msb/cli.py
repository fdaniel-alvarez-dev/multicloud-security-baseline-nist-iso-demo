from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from msb.compare import compare_summaries
from msb.demo_flow import run_demo
from msb.io.artifacts import (
    ensure_dir,
    write_csv,
    write_json,
    write_text,
)
from msb.io.fixtures import load_fixture_pack
from msb.reporting import render_html_report, render_markdown_report
from msb.scoring import assess_fixture_pack, compute_controls_coverage
from msb.utils.logging import configure_logging

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


@app.callback()
def _global(
    json_logs: bool = typer.Option(
        False,
        "--json-logs/--no-json-logs",
        envvar="MSB_JSON_LOGS",
        help="Emit structured JSON logs (also controllable via MSB_JSON_LOGS=1).",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        envvar="MSB_LOG_LEVEL",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    ),
) -> None:
    configure_logging(json_logs=json_logs, level=log_level)


@app.command()
def assess(
    input: Path = typer.Option(..., "--input", exists=True, file_okay=False, dir_okay=True),
    out: Path = typer.Option(..., "--out"),
) -> None:
    """Assess a fixture pack (targets + findings) and write summary artifacts."""
    fixture_pack = load_fixture_pack(input)
    assessment = assess_fixture_pack(fixture_pack)
    coverage = compute_controls_coverage(assessment.mapped_findings)

    ensure_dir(out)
    write_json(out / "summary.json", assessment.model_dump(mode="json"))
    write_csv(out / "controls_coverage.csv", coverage.to_rows(), coverage.headers)

    table = Table(title="Assessment Summary")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Org posture score", f"{assessment.org.posture_score:.1f}")
    table.add_row("Targets assessed", str(len(assessment.targets)))
    table.add_row("Findings", str(len(assessment.mapped_findings)))
    console.print(table)


@app.command()
def compare(
    before: Path = typer.Option(..., "--before", exists=True, file_okay=True, dir_okay=False),
    after: Path = typer.Option(..., "--after", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out"),
) -> None:
    """Compare two assessment summaries and compute posture deltas."""
    before_obj = json.loads(before.read_text(encoding="utf-8"))
    after_obj = json.loads(after.read_text(encoding="utf-8"))
    comparison = compare_summaries(before_obj, after_obj)

    ensure_dir(out)
    write_json(out / "compare.json", comparison)

    delta = comparison["org"]["posture"]["delta"]
    pct = comparison["org"]["posture"]["percent_change"]
    console.print(f"[bold]Org posture delta:[/bold] {delta:+.1f} points ({pct:+.1f}%)")


@app.command()
def report(
    input: Path = typer.Option(..., "--input", exists=True, file_okay=False, dir_okay=True),
    out: Path = typer.Option(..., "--out"),
    title: str = typer.Option("Multi-Cloud Security Baseline Report", "--title"),
    author: str | None = typer.Option("Cloud Security / DevSecOps Consultant", "--author"),
) -> None:
    """Generate executive-friendly Markdown + HTML report from compare artifacts."""
    compare_path = input / "compare.json"
    if not compare_path.exists():
        raise typer.BadParameter(f"Missing compare.json at {compare_path}")

    compare_obj: dict[str, Any] = json.loads(compare_path.read_text(encoding="utf-8"))
    ensure_dir(out)

    backlog_csv = input / "remediation_backlog.csv"
    roadmap_csv = input / "roadmap.csv"
    controls_csv = input / "controls_coverage.csv"

    md = render_markdown_report(
        title=title,
        author=author,
        compare_obj=compare_obj,
        remediation_backlog_csv_path=backlog_csv,
        roadmap_csv_path=roadmap_csv,
        controls_coverage_csv_path=controls_csv,
    )
    html = render_html_report(
        title=title,
        author=author,
        compare_obj=compare_obj,
        remediation_backlog_csv_path=backlog_csv,
        roadmap_csv_path=roadmap_csv,
        controls_coverage_csv_path=controls_csv,
    )

    write_text(out / "report.md", md)
    write_text(out / "report.html", html)
    console.print(f"Wrote: {out / 'report.md'}")
    console.print(f"Wrote: {out / 'report.html'}")


@app.command()
def demo() -> None:
    """Run the full offline demo end-to-end (before/after assessment, compare, roadmap, report)."""
    base = Path("artifacts")

    console.rule("Demo (offline fixtures → artifacts)")
    run_demo(fixtures_dir=Path("fixtures"), artifacts_dir=base)

    before_obj = json.loads((base / "before" / "summary.json").read_text(encoding="utf-8"))
    after_obj = json.loads((base / "after" / "summary.json").read_text(encoding="utf-8"))
    org_before = float(before_obj["org"]["posture_score"])
    org_after = float(after_obj["org"]["posture_score"])
    delta = org_after - org_before
    pct = (delta / org_before) * 100.0 if org_before else 0.0
    console.print(
        f"[bold]Org posture:[/bold] {org_before:.1f} → {org_after:.1f} ({delta:+.1f}, {pct:+.1f}%)"
    )
    console.print(f"Artifacts written under: {base.resolve()}")
