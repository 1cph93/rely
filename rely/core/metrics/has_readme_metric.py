import functools
from decimal import Decimal

from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.types import MetricName, MetricValue, MetricScore


class HasReadmeMetric(BaseMetric):
    """Does the repo have a non-empty README in the root directory?"""

    _metric_name = MetricName.HAS_README_METRIC
    _metric_weight = Decimal("0.99")

    @functools.cache
    def compute_metric_value(self) -> MetricValue:
        """Return True if repo has non-empty README in root directory, otherwise return False."""

        content_tree_list = self.repo_context.content_tree_list

        return any(
            content_tree.type == "file" and content_tree.size > 0
            for content_tree in content_tree_list.content_tree_list
        )

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Return good score if repo has non-empty README in root directory, otherwise return poor score."""

        has_readme = self.compute_metric_value()

        return MetricScore.GOOD if has_readme else MetricScore.POOR
