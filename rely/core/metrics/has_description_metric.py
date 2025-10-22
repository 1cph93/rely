import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class HasDescriptionMetric(BaseMetric):
    """Does the repo have a description?"""

    _metric_name = MetricName.HAS_DESCRIPTION_METRIC
    _metric_weight = Decimal("0.25")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Return True if repo has description, otherwise return False."""

        description = self.repo_context.full_repository.description

        return description is not None and description.strip() != ""

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Return good score if repo has description, otherwise return poor score."""

        has_description = self.compute_metric_value()

        return MetricScore.GOOD if has_description else MetricScore.POOR
