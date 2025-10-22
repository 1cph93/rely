import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class IsArchivedMetric(BaseMetric):
    """Is the repo archived?"""

    _metric_name = MetricName.IS_ARCHIVED_METRIC
    _metric_weight = Decimal("0.99")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Return True if repo is archived, otherwise return False."""

        return self.repo_context.full_repository.archived

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Return poor score if repo is archived, otherwise return good score."""

        is_archived = self.compute_metric_value()

        return MetricScore.POOR if is_archived else MetricScore.GOOD
