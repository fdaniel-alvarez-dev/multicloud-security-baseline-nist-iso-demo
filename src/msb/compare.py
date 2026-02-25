from __future__ import annotations

from typing import Any


def compare_summaries(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    b_org = float(before["org"]["posture_score"])
    a_org = float(after["org"]["posture_score"])
    delta = a_org - b_org
    pct = (delta / b_org) * 100.0 if b_org else 0.0

    def _domain_index(summary: dict[str, Any]) -> dict[str, float]:
        out: dict[str, float] = {}
        for d in summary["org"]["domain_maturity"]:
            out[str(d["domain"])] = float(d["posture_0_to_100"])
        return out

    b_domains = _domain_index(before)
    a_domains = _domain_index(after)
    all_domains = sorted(set(b_domains) | set(a_domains))

    domain_rows: list[dict[str, Any]] = []
    for dom in all_domains:
        bv = b_domains.get(dom, 0.0)
        av = a_domains.get(dom, 0.0)
        dv = av - bv
        domain_rows.append({"domain": dom, "before": bv, "after": av, "delta": dv})

    domain_rows.sort(key=lambda r: r["delta"], reverse=True)

    return {
        "org": {
            "posture": {
                "before": b_org,
                "after": a_org,
                "delta": delta,
                "percent_change": pct,
            },
            "domain_posture_deltas": domain_rows,
        }
    }
