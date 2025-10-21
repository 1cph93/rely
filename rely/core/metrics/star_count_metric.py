import functools
from decimal import Decimal

from rely.core.metrics.metric import (
    BaseMetric,
    MetricScore,
    MetricValue,
    MetricName,
)


class StarCountMetric(BaseMetric):
    """How many stars does the repo have?"""

    metric_name = MetricName.STAR_COUNT_METRIC
    metric_weight = Decimal("0.65")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Get number of stars for repo."""

        return self.repo_context.full_repository.stargazers_count

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Compute score based on number of stars (more stars equals better score)."""

        star_count = self.compute_metric_value()

        # Between 0 and 50
        if star_count < 50:
            metric_score = MetricScore.POOR
        # Between 50 and 500
        elif 50 <= star_count <= 500:
            metric_score = MetricScore.AVERAGE
        # Over 500
        else:
            metric_score = MetricScore.GOOD

        return metric_score
