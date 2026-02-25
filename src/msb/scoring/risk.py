from __future__ import annotations

from msb.models import Finding, FindingCategory, Rating, Severity


def domain_for_category(category: FindingCategory) -> str:
    return {
        FindingCategory.iam: "IAM",
        FindingCategory.logging: "Logging/Monitoring",
        FindingCategory.network: "Network Controls",
        FindingCategory.governance: "Governance",
        FindingCategory.asset_inventory: "Asset Inventory",
        FindingCategory.data_protection: "Data Protection",
    }[category]


def risk_score_for_finding(finding: Finding) -> float:
    severity_weight = {
        Severity.low: 1.0,
        Severity.medium: 3.0,
        Severity.high: 6.0,
        Severity.critical: 10.0,
    }[finding.severity]
    likelihood_weight = _rating_weight(finding.likelihood)
    impact_weight = _rating_weight(finding.impact)

    category_weight = {
        FindingCategory.iam: 1.25,
        FindingCategory.logging: 1.10,
        FindingCategory.network: 1.20,
        FindingCategory.governance: 1.00,
        FindingCategory.asset_inventory: 0.90,
        FindingCategory.data_protection: 1.15,
    }[finding.category]

    return severity_weight * likelihood_weight * impact_weight * category_weight


def _rating_weight(rating: Rating) -> float:
    return {Rating.low: 1.0, Rating.medium: 2.0, Rating.high: 3.0}[rating]
