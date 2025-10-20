from pydantic import BaseModel

from rely.clients.models.full_repository import FullRepository
from rely.clients.models.content_tree_list import ContentTreeList
from rely.clients.github_api_client import GitHubAPIClient
from rely.core.models.repo_identifier import RepoIdentifier


class RepoContext(BaseModel):
    """Model for storing all context required for computing repository metrics."""

    repo_identifier: RepoIdentifier
    full_repository: FullRepository
    content_tree_list: ContentTreeList


async def create_repo_context(
    repo_identifier: RepoIdentifier,
    github_api_client: GitHubAPIClient,
) -> RepoContext:
    """Create a RepoContext instance."""

    full_repository = await github_api_client.get_repo(repo_identifier)
    content_tree_list = await github_api_client.get_repo_contents(
        full_repository.contents_url
    )

    return RepoContext(
        repo_identifier=repo_identifier,
        full_repository=full_repository,
        content_tree_list=content_tree_list,
    )
