from pydantic import BaseModel, HttpUrl

from rely.config.settings import Settings
from rely.clients.http_client import HTTPClient
from rely.clients.github_api_client import GitHubAPIClient
from rely.core.models.repo_identifier import RepoIdentifier
from rely.core.models.repo_context import create_repo_context
from rely.core.metrics.types import SerializedMetric, MetricScore
from rely.core.metrics.base_metric import BaseMetric
from rely.core.metrics.metric_reducer import MetricReducer

# NOTE: We import these here in order to populate the registry
# TODO: Explore other solutions besides registry that are more explicit
from rely.core.metrics.last_commit_metric import LastCommitMetric  # noqa
from rely.core.metrics.star_count_metric import StarCountMetric  # noqa
from rely.core.metrics.fork_count_metric import ForkCountMetric  # noqa
from rely.core.metrics.watcher_count_metric import WatcherCountMetric  # noqa
from rely.core.metrics.open_issue_count_metric import OpenIssueCountMetric  # noqa
from rely.core.metrics.is_archived_metric import IsArchivedMetric  # noqa
from rely.core.metrics.is_disabled_metric import IsDisabledMetric  # noqa
from rely.core.metrics.has_license_metric import HasLicenseMetric  # noqa
from rely.core.metrics.has_description_metric import HasDescriptionMetric  # noqa
from rely.core.metrics.has_readme_metric import HasReadmeMetric  # noqa


class RepoResult(BaseModel):
    """Model to store the overall result output for a repo."""

    overall_score_decimal: float
    overall_score_int: int
    maximum_metric_score: int
    metrics: list[SerializedMetric]


async def score_repo(repo_url: str) -> RepoResult:
    """Patch components together and compute metrics for a repo, based on a URL."""

    settings = Settings()
    repo_identifier = RepoIdentifier(url=HttpUrl(repo_url))

    async with HTTPClient() as http_client:
        github_api_client = GitHubAPIClient(
            http_client=http_client,
            personal_access_token=settings.github_personal_access_token,
        )
        repo_context = await create_repo_context(repo_identifier, github_api_client)

    registry = BaseMetric.get_registry()
    metric_class_list = registry.values()
    metric_reducer = MetricReducer(metric_class_list, repo_context)
    overall_score = metric_reducer.compute_overall_score()

    return RepoResult(
        overall_score_decimal=float(overall_score),
        overall_score_int=int(overall_score * 100),
        maximum_metric_score=MetricScore.GOOD.value,
        metrics=[
            metric_instance.serialize()
            for metric_instance in metric_reducer.metric_instances
        ],
    )
