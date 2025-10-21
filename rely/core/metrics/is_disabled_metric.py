import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class IsDisabledMetric(BaseMetric):
    """Is the repo disabled?"""

    metric_name = MetricName.IS_DISABLED_METRIC
    metric_weight = Decimal("0.99")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Return True if repo is disabled, otherwise return False."""

        return self.repo_context.full_repository.disabled

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Return poor score if repo is disabled, otherwise return good score."""

        is_disabled = self.compute_metric_value()

        return MetricScore.POOR if is_disabled else MetricScore.GOOD
