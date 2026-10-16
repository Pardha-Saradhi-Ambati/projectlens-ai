from abc import ABC, abstractmethod
from typing import List, Tuple
from app.models import Finding, SeveritySummary


class BaseAnalyzer(ABC):
    """Abstract base class for static analysis tool runners."""

    @abstractmethod
    def is_available(self) -> Tuple[bool, str]:
        """Check if the static analysis tool is installed and executable."""
        pass

    @abstractmethod
    def analyze(self, file_path: str, original_filename: str) -> List[Finding]:
        """Execute static analysis on the target file and return structured findings."""
        pass

    @staticmethod
    def calculate_summary(findings: List[Finding]) -> SeveritySummary:
        """Helper to aggregate findings by severity."""
        summary = SeveritySummary(total_issues=len(findings))
        for f in findings:
            if f.severity.value == "HIGH":
                summary.high += 1
            elif f.severity.value == "MEDIUM":
                summary.medium += 1
            elif f.severity.value == "LOW":
                summary.low += 1
            else:
                summary.info += 1
        return summary
