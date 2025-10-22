import datetime
import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class LastCommitMetric(BaseMetric):
    """How recent is the latest commit?"""

    _metric_name = MetricName.LAST_COMMIT_METRIC
    _metric_weight = Decimal("0.99")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Compute number of days since last commit."""

        pushed_at = self.repo_context.full_repository.pushed_at
        delta = datetime.datetime.now(datetime.timezone.utc) - pushed_at

        return delta.days

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Compute score based on time since last commit (shorter time equals better score)."""

        days_since_last_commit = self.compute_metric_value()

        # Less than 30 days
        if days_since_last_commit < 30:
            metric_score = MetricScore.GOOD
        # Between 30 days and 180 days
        elif 30 <= days_since_last_commit <= 180:
            metric_score = MetricScore.AVERAGE
        # Greater than 180 days
        else:
            metric_score = MetricScore.POOR

        return metric_score
