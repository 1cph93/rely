from pathlib import Path

from typing import cast

from rely.core.models.repo_context import RepoContext
from rely.core.metrics.types import SerializedMetric
from rely.core.metrics.has_description_metric import HasDescriptionMetric
from tests.conftest import ModelLoaderFunction


def test_compute_has_description_metric(
    local_test_dir: Path, load_model_from_file: ModelLoaderFunction
) -> None:
    """Ensure that HasDescriptionMetric is properly computed and serialized."""

    model_instance = load_model_from_file(
        RepoContext, local_test_dir / "fixtures" / "repo_context.json"
    )
    repo_context = cast(RepoContext, model_instance)
    has_description_metric = HasDescriptionMetric(repo_context)

    actual = has_description_metric.serialize()
    expected = SerializedMetric(
        normalized_name="has_description_metric",
        prettified_name="Has description?",
        metric_weight=0.25,
        metric_value=True,
        metric_score=3,
        metric_weighted_score=0.75,
    )

    assert actual == expected
