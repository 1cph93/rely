import enum
import functools
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Annotated, Type, Any

import annotated_types

from rely.core.models.repo_context import RepoContext


class MetricScore(enum.IntEnum):
    POOR = 1
    AVERAGE = 2
    GOOD = 3


type MetricValue = int | float | bool
# Decimal value between 0 and 1 (exclusive)
type MetricWeight = Annotated[
    Decimal, annotated_types.Gt((Decimal("0.0"))), annotated_types.Lt(Decimal("1.0"))
]
type MetricRegistry = dict[str, Type["BaseMetric"]]


class MetricName(enum.Enum):
    """Metric names."""

    LAST_COMMIT_METRIC = ("last_commit_metric", "Last commit (in days)")
    STAR_COUNT_METRIC = ("star_count_metric", "Number of stars")

    def __init__(self, normalized_name: str, prettified_name: str) -> None:
        self.normalized_name = normalized_name
        self.prettified_name = prettified_name


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

    def to_dict(self) -> dict[str, Any]:
        """Convert instance to dict."""

        return {
            "normalized_name": self.get_normalized_name(),
            "prettified_name": self.get_prettified_name(),
            "metric_weight": float(self.metric_weight),
            "metric_value": self.compute_metric_value(),
            "metric_score": self.compute_metric_score().value,
            "metric_weighted_score": float(self.compute_metric_weighted_score()),
        }
