from rely.core.models.repo_context import RepoContext
from rely.core.metrics.types import SerializedMetric
from rely.core.metrics.is_archived_metric import IsArchivedMetric


def test_compute_is_archived_metric(repo_context: RepoContext) -> None:
    """Ensure that IsArchivedMetric is properly computed and serialized."""

    is_archived_metric = IsArchivedMetric(repo_context)

    actual = is_archived_metric.serialize()
    expected = SerializedMetric(
        normalized_name="is_archived_metric",
        prettified_name="Archived?",
        metric_weight=0.99,
        metric_value=False,
        metric_score=3,
        metric_weighted_score=2.97,
    )

    assert actual == expected
