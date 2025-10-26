from pathlib import Path

from typing import cast

from rely.core.models.repo_context import RepoContext
from rely.core.metrics.types import SerializedMetric
from rely.core.metrics.is_disabled_metric import IsDisabledMetric
from tests.conftest import ModelLoaderFunction


def test_compute_is_disabled_metric(
    local_test_dir: Path, load_model_from_file: ModelLoaderFunction
) -> None:
    """Ensure that IsDisabledMetric is properly computed and serialized."""

    model_instance = load_model_from_file(
        RepoContext, local_test_dir / "fixtures" / "repo_context.json"
    )
    repo_context = cast(RepoContext, model_instance)
    is_disabled_metric = IsDisabledMetric(repo_context)

    actual = is_disabled_metric.serialize()
    expected = SerializedMetric(
        normalized_name="is_disabled_metric",
        prettified_name="Disabled?",
        metric_weight=1.0,
        metric_value=False,
        metric_score=3,
        metric_weighted_score=3.0,
    )

    assert actual == expected
