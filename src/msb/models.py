from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Provider(StrEnum):
    aws = "aws"
    azure = "azure"
    gcp = "gcp"


class FindingCategory(StrEnum):
    iam = "IAM"
    logging = "Logging/Monitoring"
    network = "Network Controls"
    governance = "Governance"
    asset_inventory = "Asset Inventory"
    data_protection = "Data Protection"


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Rating(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Effort(StrEnum):
    small = "S"
    medium = "M"
    large = "L"


class Asset(BaseModel):
    asset_id: str
    asset_type: str
    name: str
    labels: dict[str, str] = Field(default_factory=dict)


class Target(BaseModel):
    target_id: str
    provider: Provider
    environment: Literal["prod", "dev", "staging"] = "prod"
    region: str
    owner: str
    assets: list[Asset]


class RecommendedAction(BaseModel):
    action_id: str
    title: str
    description: str
    effort: Effort
    expected_impact: Annotated[int, Field(ge=1, le=5)]
    dependencies: list[str] = Field(default_factory=list)
    owner: str = "Platform/Security"


class Finding(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    finding_id: str
    target_id: str
    title: str
    description: str
    category: FindingCategory
    severity: Severity
    likelihood: Rating
    impact: Rating
    evidence: dict[str, str]
    affected_assets: list[str]
    detection_source: str
    detected_at: datetime
    tags: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction]


class NistCsfMapping(BaseModel):
    function: str
    category: str
    rationale: str


class Iso27001ThemeMapping(BaseModel):
    theme_id: str
    theme_name: str
    rationale: str


class MappedFinding(BaseModel):
    finding: Finding
    nist: list[NistCsfMapping]
    iso: list[Iso27001ThemeMapping]
    risk_score: float
    domain: str


class DomainMaturity(BaseModel):
    domain: str
    maturity_0_to_5: float
    posture_0_to_100: float


class TargetAssessment(BaseModel):
    target_id: str
    provider: Provider
    environment: str
    posture_score: float
    domain_maturity: list[DomainMaturity]
    finding_count: int


class OrgAssessment(BaseModel):
    posture_score: float
    domain_maturity: list[DomainMaturity]


class AssessmentSummary(BaseModel):
    assessed_at: datetime
    org: OrgAssessment
    targets: list[TargetAssessment]
    mapped_findings: list[MappedFinding]
