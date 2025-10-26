import functools
from decimal import Decimal

from rely.config.constants import SUPPORTED_README_EXTENSIONS
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
        possible_readme_paths = {
            f"readme.{extension}" for extension in SUPPORTED_README_EXTENSIONS
        }
        # Include README with no extension to possible paths
        possible_readme_paths.add("readme")

        return any(
            content_tree.type == "file"
            and content_tree.path.lower() in possible_readme_paths
            and content_tree.size > 0
            for content_tree in content_tree_list.content_tree_list
        )

    @functools.cache
    def compute_metric_score(self) -> MetricScore:
        """Return good score if repo has non-empty README in root directory, otherwise return poor score."""

        has_readme = self.compute_metric_value()

        return MetricScore.GOOD if has_readme else MetricScore.POOR
