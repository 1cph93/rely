import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class HasLicenseMetric(BaseMetric):
    """Does the repo have a license?"""

    metric_name = MetricName.HAS_LICENSE_METRIC
    metric_weight = Decimal("0.5")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Return True if repo has license, otherwise return False."""

        return self.repo_context.full_repository.license is not None

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Return good score if repo has license, otherwise return poor score."""

        has_license = self.compute_metric_value()

        return MetricScore.GOOD if has_license else MetricScore.POOR
