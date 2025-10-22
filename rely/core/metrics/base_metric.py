import functools
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Type, MutableMapping

from rely.core.metrics.types import (
    MetricName,
    MetricScore,
    MetricValue,
    MetricWeight,
    SerializedMetric,
)
from rely.core.models.repo_context import RepoContext


type MetricRegistry = MutableMapping[str, Type["BaseMetric"]]


class BaseMetric(ABC):
    """Abstract base class for computable metric subclasses."""

    _registry: MetricRegistry = {}
    _metric_name: MetricName
    _metric_weight: MetricWeight

    def __init__(self, repo_context: RepoContext) -> None:
        self.repo_context = repo_context

    @classmethod
    def __init_subclass__(cls) -> None:
        """
        Update registry every time BaseMetric is subclassed.
        Provides a simple way to keep track of all metric subclasses.
        """

        super().__init_subclass__()
        cls._registry[cls.get_normalized_name()] = cls

    @classmethod
    def get_registry(cls) -> MetricRegistry:
        """Get class registry."""

        return cls._registry

    @classmethod
    def get_normalized_name(cls) -> str:
        """Get normalized metric name."""

        normalized_name, _ = cls._metric_name.value

        return normalized_name

    @classmethod
    def get_prettified_name(cls) -> str:
        """Get prettified (human-readable) metric name."""

        _, prettified_name = cls._metric_name.value

        return prettified_name

    @classmethod
    def get_metric_weight(cls) -> MetricWeight:
        """Get metric weight."""

        return cls._metric_weight

    @functools.cache
    @abstractmethod
    def compute_metric_value(self) -> MetricValue:
        """
        Compute raw metric value.
        NOTE: This is an unaltered value that comes from the repo itself,
              like number of stars or time since last commit.
        """

        pass

    @functools.cache
    @abstractmethod
    def compute_metric_score(self) -> MetricScore:
        """
        Compute metric score.
        NOTE: This is a score that we assign based on the metric's value,
              like poor, average, or good.
        """

        pass

    def compute_metric_weighted_score(self) -> Decimal:
        """
        Compute metric weighted score.
        NOTE: We assign a weight to each metric to indicate how important it is.
              The weigted score is equal to weight * score.
        """

        metric_score = self.compute_metric_score().value

        return Decimal(metric_score) * self.get_metric_weight()

    def serialize(self) -> SerializedMetric:
        """Serialize computed metric fields."""

        return SerializedMetric(
            normalized_name=self.get_normalized_name(),
            prettified_name=self.get_prettified_name(),
            metric_weight=float(self.get_metric_weight()),
            metric_value=self.compute_metric_value(),
            metric_score=self.compute_metric_score(),
            metric_weighted_score=float(self.compute_metric_weighted_score()),
        )
