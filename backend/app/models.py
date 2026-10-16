from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class FindingSeverity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class Finding(BaseModel):
    id: str = Field(..., description="Unique finding ID")
    rule_id: str = Field(..., description="Tool-specific rule ID (e.g., B605 or no-eval)")
    title: str = Field(..., description="Short descriptive title of the issue")
    severity: FindingSeverity = Field(..., description="Severity level: HIGH, MEDIUM, LOW, or INFO")
    line_number: Optional[int] = Field(None, description="Starting line number in source code")
    column_number: Optional[int] = Field(None, description="Starting column number if available")
    code_snippet: Optional[str] = Field(None, description="Flagged code snippet or line content")
    description: str = Field(..., description="Technical description of what was flagged")
    risk_explanation: str = Field(..., description="Educational explanation of potential risks for students")
    recommendation: str = Field(..., description="Actionable recommendation to improve the code")
    code_fix_example: Optional[str] = Field(None, description="Concrete before/after or safe pattern example")
    reference_url: Optional[str] = Field(None, description="Documentation or rule guide reference")


class SeveritySummary(BaseModel):
    total_issues: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    info: int = 0


class AnalysisResponse(BaseModel):
    success: bool = True
    file_name: str
    file_type: str
    file_size_bytes: int
    scan_timestamp: str
    tool_used: str
    summary: SeveritySummary
    findings: List[Finding]
    disclaimer: str
    message: Optional[str] = None


class ToolStatus(BaseModel):
    name: str
    available: bool
    version_or_path: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    tools: Dict[str, ToolStatus]


class SampleItem(BaseModel):
    id: str
    title: str
    language: str
    filename: str
    description: str
    code: str
