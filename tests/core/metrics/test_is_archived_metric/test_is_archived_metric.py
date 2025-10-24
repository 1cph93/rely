from pathlib import Path

from typing import cast

from rely.core.models.repo_context import RepoContext
from rely.core.metrics.types import SerializedMetric
from rely.core.metrics.is_archived_metric import IsArchivedMetric
from tests.conftest import ModelLoaderFunction


def test_compute_is_archived_metric(
    local_test_dir: Path, load_model_from_file: ModelLoaderFunction
) -> None:
    """Ensure that IsArchivedMetric is properly computed and serialized."""

    model_instance = load_model_from_file(
        RepoContext, local_test_dir / "fixtures" / "repo_context.json"
    )
    repo_context = cast(RepoContext, model_instance)
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
