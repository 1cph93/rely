from typing import Annotated, Final

from pydantic import (
    AfterValidator,
    HttpUrl,
    computed_field,
    BaseModel,
)


_GITHUB_HOST: Final[str] = "github.com"


def _is_valid_path(path: str | None) -> tuple[str, str]:
    """Validates that a path follows the correct format (OWNER/REPO).  Returns repo owner and repo name if successful."""

    if path is None or path == "/":
        raise ValueError("path can not be empty")

    split_path = path.strip("/").split("/")

    if len(split_path) != 2:
        raise ValueError("path must follow the format OWNER/REPO")

    return (split_path[0], split_path[1])


def _is_github_repo_url(url: HttpUrl) -> HttpUrl:
    """Validates that a URL points to a valid GitHub repository."""

    if url.host != _GITHUB_HOST:
        raise ValueError(f"{url} must include a GitHub domain")

    _is_valid_path(url.path)

    return url


_GitHubRepoUrl = Annotated[HttpUrl, AfterValidator(_is_github_repo_url)]


class RepoIdentifier(BaseModel):
    """
    Model for storing fields that uniquely identify a repository.
    NOTE: We currently identify a GitHub repository by its full URL.
    """

    url: _GitHubRepoUrl

    @computed_field(return_type=str)
    @property
    def repo_owner(self) -> str:
        """Owner of the repository."""

        repo_owner, _ = _is_valid_path(self.url.path)

        return repo_owner

    @computed_field(return_type=str)
    @property
    def repo_name(self) -> str:
        """Name of the repository."""

        _, repo_name = _is_valid_path(self.url.path)

        return repo_name
