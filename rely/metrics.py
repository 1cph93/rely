import datetime
import decimal
import enum
from typing import Protocol

from rely.clients.models.full_repository import FullRepository
from rely.clients.models.content_tree import ContentTree


class MetricScore(enum.Enum):
    POOR = enum.auto()
    AVERAGE = enum.auto()
    GOOD = enum.auto()


type MetricValue = int | float | bool


# TODO: Possible change implementation, since we only have static methods
class Metric(Protocol):
    """Compute a metric based on a FullRepository instance."""

    @staticmethod
    def get_normalized_name() -> str:
        """Get the metric's normalized name."""
        ...

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> MetricValue:
        """Compute the metric's raw value."""
        ...

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Compute the metric's MetricScore."""
        ...


class LastCommitMetric:
    """How recent was the latest commit?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "last_commit_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> float:
        """Get the number of seconds since the last commit."""

        pushed_at = full_repository.pushed_at
        delta = datetime.datetime.now(datetime.timezone.utc) - pushed_at

        return delta.total_seconds()

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return a MetricScores based on time since last commit (shorter time leads to better score)."""

        computed_value = LastCommitMetric._compute_value(full_repository)
        ONE_DAY_IN_SECONDS = 86400

        # Less than 30 days
        if computed_value < ONE_DAY_IN_SECONDS * 30:
            metric_score = MetricScore.GOOD
        # Between 30 days and 180 days
        elif ONE_DAY_IN_SECONDS * 30 <= computed_value <= ONE_DAY_IN_SECONDS * 30 * 6:
            metric_score = MetricScore.AVERAGE
        # Greater than 180 days
        else:
            metric_score = MetricScore.POOR

        return metric_score


class HasDescriptionMetric:
    """Does the repo have a description?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "has_description_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> bool:
        """Return True if the description is present, otherwise return False."""

        description = full_repository.description

        return description is not None and description.strip() != ""

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return good MetricScore if the description is present, otherwise return poor MetricScore."""
        return (
            MetricScore.GOOD
            if HasDescriptionMetric._compute_value(full_repository)
            else MetricScore.POOR
        )


class HasReadmeMetric:
    """Does the repo have a README?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "has_readme_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> bool:
        """Return True if a README is present, otherwise return False."""

        breakpoint()

        return False

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return good MetricScore if a README is present, otherwise return poor MetricScore."""
        return (
            MetricScore.GOOD
            if HasReadmeMetric._compute_value(full_repository)
            else MetricScore.POOR
        )


class IsArchivedMetric:
    """Is the repo archived?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "is_archived_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> bool:
        """Return True if the repo is archived, otherwise return False."""

        return full_repository.archived

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return poor MetricScore if the repo is archived, otherwise return good MetricScore."""
        return (
            MetricScore.POOR
            if HasDescriptionMetric._compute_value(full_repository)
            else MetricScore.GOOD
        )


class IsDisabledMetric:
    """Is the repo disabled?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "is_disabled_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> bool:
        """Return True if the repo is disabled, otherwise return False."""

        return full_repository.disabled

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return poor MetricScore if the repo is disabled, otherwise return good MetricScore."""
        return (
            MetricScore.POOR
            if IsDisabledMetric._compute_value(full_repository)
            else MetricScore.GOOD
        )


class HasLicenseMetric:
    """Does the repo have a license?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "has_license_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> bool:
        """Return True if the repo has a license, otherwise return False."""

        return full_repository.license is not None

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return good MetricScore if the repo has a license, otherwise return poor MetricScore."""
        return (
            MetricScore.GOOD
            if HasLicenseMetric._compute_value(full_repository)
            else MetricScore.POOR
        )


class HasCodeOfConductMetric:
    """Does the repo have a code of conduct?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "has_code_of_conduct_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> bool:
        """Return True if the repo has a code of conduct, otherwise return False."""

        return full_repository.code_of_conduct is not None

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return good MetricScore if the repo has a code of conduct, otherwise return poor MetricScore."""
        return (
            MetricScore.GOOD
            if HasCodeOfConductMetric._compute_value(full_repository)
            else MetricScore.POOR
        )


class StarCountMetric:
    """How many stars does the repo have?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "star_count_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> int:
        """Return the number of stars a repo has."""

        return full_repository.stargazers_count

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return MetricScore based on star count (more stars leads to better score)."""
        star_count = StarCountMetric._compute_value(full_repository)

        # Between 0 and 50
        if star_count < 50:
            score = MetricScore.POOR
        # Between 50 and 500
        elif 50 <= star_count <= 500:
            score = MetricScore.AVERAGE
        # Over 500
        else:
            score = MetricScore.GOOD

        return score


class ForkCountMetric:
    """How many forks does the repo have?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "fork_count_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> int:
        """Return the number of forks a repo has."""

        return full_repository.forks_count

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return MetricScore based on fork count (more forks leads to better score)."""
        fork_count = ForkCountMetric._compute_value(full_repository)

        # Between 0 and 50
        if fork_count < 50:
            score = MetricScore.POOR
        # Between 50 and 500
        elif 50 <= fork_count <= 500:
            score = MetricScore.AVERAGE
        # Over 500
        else:
            score = MetricScore.GOOD

        return score


class WatcherCountMetric:
    """How many watchers does the repo have?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "watcher_count_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> int:
        """Return the number of watchers a repo has."""

        return full_repository.watchers_count

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return MetricScore based on watchers count (more watchers leads to better score)."""
        watcher_count = WatcherCountMetric._compute_value(full_repository)

        # Between 0 and 50
        if watcher_count < 50:
            score = MetricScore.POOR
        # Between 50 and 500
        elif 50 <= watcher_count <= 500:
            score = MetricScore.AVERAGE
        # Over 500
        else:
            score = MetricScore.GOOD

        return score


class OpenIssueCountMetric:
    """How many open issues does the repo have?"""

    @staticmethod
    def get_normalized_name() -> str:
        return "open_issue_count_metric"

    @staticmethod
    def _compute_value(
        full_repository: FullRepository, content_tree: ContentTree
    ) -> int:
        """Return the number of open issues a repo has."""

        return full_repository.open_issues_count

    @staticmethod
    def compute_score(full_repository: FullRepository) -> MetricScore:
        """Return MetricScore based on open issues count (more open issues leads to better score)."""
        open_issue_count = OpenIssueCountMetric._compute_value(full_repository)

        # Between 0 and 5
        if open_issue_count < 5:
            score = MetricScore.POOR
        # Between 5 and 20
        elif 5 <= open_issue_count <= 20:
            score = MetricScore.AVERAGE
        # Over 20
        else:
            score = MetricScore.GOOD

        return score


# TODO: Add security metrics (like has_security_scanning, etc.)


def compute_metrics(
    metrics: frozenset[Metric],
    full_repository: FullRepository,
) -> list[tuple[str, MetricScore]]:
    """Compute all of the provided metrics for a repository."""

    return [
        (metric.get_normalized_name(), metric.compute_score(full_repository))
        for metric in metrics
    ]


def compute_overall_score(
    computed_metrics: list[tuple[str, MetricScore]], precision: int = 2
) -> decimal.Decimal:
    """Compute the overall score of a repository, based on its computed metrics."""

    best_possible_score = MetricScore.GOOD.value * len(computed_metrics)
    actual_score = sum(
        [computed_metric[-1].value for computed_metric in computed_metrics]
    )

    decimal.getcontext().prec = precision

    return decimal.Decimal(actual_score) / decimal.Decimal(best_possible_score)
