import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class OpenIssueCountMetric(BaseMetric):
    """How many open issues does the repo have?"""

    metric_name = MetricName.OPEN_ISSUE_COUNT_METRIC
    metric_weight = Decimal("0.85")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Get number of open issues for repo."""

        return self.repo_context.full_repository.open_issues_count

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Compute score based on number of open issues (more open issues equals better score)."""

        open_issue_count = self.compute_metric_value()

        # Between 0 and 5
        if open_issue_count < 5:
            metric_score = MetricScore.POOR
        # Between 5 and 20
        elif 5 <= open_issue_count <= 20:
            metric_score = MetricScore.AVERAGE
        # Over 20
        else:
            metric_score = MetricScore.GOOD

        return metric_score
