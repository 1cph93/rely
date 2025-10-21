import enum
from decimal import Decimal
from typing import Annotated

import annotated_types
from pydantic import BaseModel


type MetricValue = int | float | bool
# Decimal value between 0 and 1 (exclusive)
type MetricWeight = Annotated[
    Decimal, annotated_types.Gt((Decimal("0.0"))), annotated_types.Lt(Decimal("1.0"))
]


class MetricScore(enum.IntEnum):
    """Metric scores."""

    POOR = 1
    AVERAGE = 2
    GOOD = 3


class MetricName(enum.Enum):
    """Metric names."""

    LAST_COMMIT_METRIC = ("last_commit_metric", "Last commit (in days)")
    STAR_COUNT_METRIC = ("star_count_metric", "Number of stars")
    FORK_COUNT_METRIC = ("fork_count_metric", "Number of forks")

    def __init__(self, normalized_name: str, prettified_name: str) -> None:
        self.normalized_name = normalized_name
        self.prettified_name = prettified_name


class SerializedMetric(BaseModel):
    """Model for storing serialized metric fields."""

    normalized_name: str
    prettified_name: str
    metric_weight: float
    metric_value: int | float | bool
    metric_score: int
    metric_weighted_score: float
