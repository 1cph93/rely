from decimal import Decimal

from pydantic import BaseModel

from rely.config.settings import Settings
from rely.clients.http_client import HttpClient
from rely.clients.github_api_client import GithubAPIClient
from rely.metrics import (
    MetricScore,
    LastCommitMetric,
    HasDescriptionMetric,
    IsArchivedMetric,
    IsDisabledMetric,
    HasLicenseMetric,
    HasCodeOfConductMetric,
    StarCountMetric,
    ForkCountMetric,
    WatcherCountMetric,
    OpenIssueCountMetric,
    compute_metrics,
    compute_overall_score,
)


class RepoScore(BaseModel):
    computed_metrics: list[tuple[str, MetricScore]]
    overall_score: Decimal


async def score_repo(owner_name: str, repo_name: str) -> RepoScore:
    settings = Settings()
    http_client = HttpClient()
    github_api_client = GithubAPIClient(
        http_client, settings.github_personal_access_token
    )
    full_repository = await github_api_client.get_repo(owner_name, repo_name)

    metrics_to_compute = frozenset(
        {
            LastCommitMetric(),
            HasDescriptionMetric(),
            IsArchivedMetric(),
            IsDisabledMetric(),
            HasLicenseMetric(),
            HasCodeOfConductMetric(),
            StarCountMetric(),
            ForkCountMetric(),
            WatcherCountMetric(),
            OpenIssueCountMetric(),
        }
    )

    # TODO: Resolve type: ignore
    computed_metrics = compute_metrics(metrics_to_compute, full_repository)  # type: ignore
    overall_score = compute_overall_score(computed_metrics)

    return RepoScore.model_validate(
        {"computed_metrics": computed_metrics, "overall_score": overall_score}
    )
