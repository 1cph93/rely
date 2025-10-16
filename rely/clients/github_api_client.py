from typing import Final
from types import MappingProxyType

from rely.clients.http_client import HttpClient
from rely.clients.models.full_repository import FullRepository


class GithubAPIClient:
    """Super light GitHub API client for interacting with repos."""

    API_BASE_URL: Final[str] = "https://api.github.com"

    def __init__(self, http_client: HttpClient, personal_access_token: str) -> None:
        self._http_client = http_client
        self.headers: MappingProxyType[str, str] = MappingProxyType(
            {
                "Authorization": f"Bearer {personal_access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    async def get_repo(self, repo_owner: str, repo_name: str) -> FullRepository:
        """Get a repository.  Reference: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository"""

        url = f"{self.API_BASE_URL}/repos/{repo_owner}/{repo_name}"
        response = await self._http_client.get(
            url,
            headers=self.headers,
        )

        # TODO: Add error handling
        return FullRepository.model_validate(response)
