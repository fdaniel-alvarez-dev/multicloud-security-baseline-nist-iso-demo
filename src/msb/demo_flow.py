from __future__ import annotations

from pathlib import Path

from msb.compare import compare_summaries
from msb.io.artifacts import ensure_dir, write_csv, write_json, write_text
from msb.io.fixtures import load_fixture_pack
from msb.prioritization import build_backlog_and_roadmap
from msb.reporting import render_html_report, render_markdown_report
from msb.scoring import assess_fixture_pack, compute_controls_coverage


def run_demo(*, fixtures_dir: Path, artifacts_dir: Path) -> None:
    before_out = artifacts_dir / "before"
    after_out = artifacts_dir / "after"
    compare_out = artifacts_dir / "compare"
    report_out = artifacts_dir / "report"

    fixture_before = load_fixture_pack(fixtures_dir / "before")
    assessment_before = assess_fixture_pack(fixture_before)
    coverage_before = compute_controls_coverage(assessment_before.mapped_findings)
    ensure_dir(before_out)
    write_json(before_out / "summary.json", assessment_before.model_dump(mode="json"))
    write_csv(
        before_out / "controls_coverage.csv", coverage_before.to_rows(), coverage_before.headers
    )

    fixture_after = load_fixture_pack(fixtures_dir / "after")
    assessment_after = assess_fixture_pack(fixture_after)
    coverage_after = compute_controls_coverage(assessment_after.mapped_findings)
    ensure_dir(after_out)
    write_json(after_out / "summary.json", assessment_after.model_dump(mode="json"))
    write_csv(after_out / "controls_coverage.csv", coverage_after.to_rows(), coverage_after.headers)

    comparison = compare_summaries(
        assessment_before.model_dump(mode="json"),
        assessment_after.model_dump(mode="json"),
    )
    ensure_dir(compare_out)
    write_json(compare_out / "compare.json", comparison)

    backlog, roadmap = build_backlog_and_roadmap(assessment_after.mapped_findings)
    write_csv(compare_out / "remediation_backlog.csv", backlog.to_rows(), backlog.headers)
    write_csv(compare_out / "roadmap.csv", roadmap.to_rows(), roadmap.headers)
    combined_coverage = compute_controls_coverage(assessment_after.mapped_findings)
    write_csv(
        compare_out / "controls_coverage.csv",
        combined_coverage.to_rows(),
        combined_coverage.headers,
    )

    ensure_dir(report_out)
    md = render_markdown_report(
        title="Multi-Cloud Security Baseline Report (Demo)",
        author="Cloud Security / DevSecOps Consultant",
        compare_obj=comparison,
        remediation_backlog_csv_path=compare_out / "remediation_backlog.csv",
        roadmap_csv_path=compare_out / "roadmap.csv",
        controls_coverage_csv_path=compare_out / "controls_coverage.csv",
    )
    html = render_html_report(
        title="Multi-Cloud Security Baseline Report (Demo)",
        author="Cloud Security / DevSecOps Consultant",
        compare_obj=comparison,
        remediation_backlog_csv_path=compare_out / "remediation_backlog.csv",
        roadmap_csv_path=compare_out / "roadmap.csv",
        controls_coverage_csv_path=compare_out / "controls_coverage.csv",
    )
    write_text(report_out / "report.md", md)
    write_text(report_out / "report.html", html)
