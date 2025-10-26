from decimal import Decimal
from typing import Type, Collection
import functools

from rely.core.models.repo_context import RepoContext
from rely.core.metrics.types import MetricScore
from rely.core.metrics.base_metric import BaseMetric


class MetricReducer:
    """Compute overall values for a collection of metrics."""

    def __init__(
        self, metric_classes: Collection[Type[BaseMetric]], repo_context: RepoContext
    ) -> None:
        self._metric_classes = metric_classes
        self._repo_context = repo_context

    @property
    def metric_instances(self) -> list[BaseMetric]:
        """Create a list of metric instances."""

        return [
            metric_class(self._repo_context) for metric_class in self._metric_classes
        ]

    @property
    def _highest_possible_score(self) -> Decimal:
        """Compute the highest possible score that a repo can have."""

        metric_weights = [
            metric_instance.get_metric_weight()
            for metric_instance in self.metric_instances
        ]
        highest_possible_score = sum(
            [MetricScore.GOOD.value * metric_weight for metric_weight in metric_weights]
        )

        return Decimal(highest_possible_score)

    @functools.cache
    def _compute_weighted_sum(self) -> Decimal:
        """Compute the sum of all weighted scores."""

        weighted_sum = sum(
            [
                metric_instance.compute_metric_weighted_score()
                for metric_instance in self.metric_instances
            ]
        )

        return Decimal(weighted_sum)

    def compute_overall_score(self) -> Decimal:
        """
        Compute the overall score for a repo.
        NOTE: This is defined as weighted sum / hightest possible score
        """

        weighted_sum = self._compute_weighted_sum()

        return weighted_sum / self._highest_possible_score
