import functools
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Type

from rely.core.metrics.types import (
    MetricName,
    MetricScore,
    MetricValue,
    MetricWeight,
    SerializedMetric,
)
from rely.core.models.repo_context import RepoContext


type MetricRegistry = dict[str, Type["BaseMetric"]]


class BaseMetric(ABC):
    """Abstract base class for computable metric subclasses."""

    _registry: MetricRegistry = {}
    metric_name: MetricName
    metric_weight: MetricWeight

    def __init__(self, repo_context: RepoContext) -> None:
        self.repo_context = repo_context

    @classmethod
    def __init_subclass__(cls) -> None:
        """Update registry every time BaseMetric is subclassed."""

        super().__init_subclass__()
        cls._registry[cls.get_normalized_name()] = cls

    @classmethod
    def get_registry(cls) -> MetricRegistry:
        """Get class registry."""

        return cls._registry

    @classmethod
    def get_normalized_name(cls) -> str:
        """Get normalized metric name."""

        normalized_name, _ = cls.metric_name.value

        return normalized_name

    @classmethod
    def get_prettified_name(cls) -> str:
        """Get prettified metric name."""

        _, prettified_name = cls.metric_name.value

        return prettified_name

    @functools.cache
    @abstractmethod
    def compute_metric_value(self) -> MetricValue:
        """Compute metric value."""

        pass

    @functools.cache
    @abstractmethod
    def compute_metric_score(self) -> MetricScore:
        """Compute metric score."""

        pass

    def compute_metric_weighted_score(self) -> Decimal:
        """Compute metric weighted score."""

        metric_score = self.compute_metric_score().value

        return Decimal(metric_score) * self.metric_weight

    def serialize(self) -> SerializedMetric:
        """Serialize computed model fields."""

        return SerializedMetric(
            normalized_name=self.get_normalized_name(),
            prettified_name=self.get_prettified_name(),
            metric_weight=float(self.metric_weight),
            metric_value=self.compute_metric_value(),
            metric_score=self.compute_metric_score(),
            metric_weighted_score=float(self.compute_metric_weighted_score()),
        )
