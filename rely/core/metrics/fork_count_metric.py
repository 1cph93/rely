import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class ForkCountMetric(BaseMetric):
    """How many forks does the repo have?"""

    metric_name = MetricName.FORK_COUNT_METRIC
    metric_weight = Decimal("0.5")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Get number of forks for repo."""

        return self.repo_context.full_repository.forks_count

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Compute score based on number of forks (more forks equals better score)."""

        fork_count = self.compute_metric_value()

        # Between 0 and 20
        if fork_count < 20:
            metric_score = MetricScore.POOR
        # Between 20 and 200
        elif 20 <= fork_count <= 200:
            metric_score = MetricScore.AVERAGE
        # Over 200
        else:
            metric_score = MetricScore.GOOD

        return metric_score
