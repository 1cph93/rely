from typing import Final, Any
from types import MappingProxyType

import aiohttp

from rely.clients.http_client import HTTPClient
from rely.clients.models.full_repository import FullRepository
from rely.clients.models.content_tree_list import ContentTreeList
from rely.core.models.repo_identifier import RepoIdentifier


class GitHubAPIError(Exception):
    """Generic exception for GitHub API errors."""

    pass


class GitHubAPIClient:
    """Minimal GitHub API client for interacting with repos."""

    API_BASE_URL: Final[str] = "https://api.github.com"

    def __init__(self, http_client: HTTPClient, personal_access_token: str) -> None:
        self._http_client = http_client
        self._personal_access_token = personal_access_token

    @property
    def headers(self) -> MappingProxyType[str, str]:
        return MappingProxyType(
            {
                "Authorization": f"Bearer {self._personal_access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    async def get_repo(self, repo_identifier: RepoIdentifier) -> FullRepository:
        """
        Get a repository.
        Reference: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository
        """

        url = f"{self.API_BASE_URL}/repos/{repo_identifier.repo_owner}/{repo_identifier.repo_name}"
        response = await self._perform_get_request(url)

        # TODO: Add error handling
        return FullRepository.model_validate(response)

    async def get_repo_contents(self, contents_url: str) -> ContentTreeList:
        """
        Get the contents of a repository.
        Reference: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28
        NOTE: We intentionally fetch the entire content tree list
        """

        # Remove "/{+path}" from the end of the contents URL
        url = contents_url.rstrip("/{+path}")
        response = await self._perform_get_request(url)

        # TODO: Add error handling
        return ContentTreeList(content_tree_list=response)

    async def _perform_get_request(self, url: str) -> Any:
        """
        Perform HTTP request and handle errors.
        Reference: https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28
        """

        try:
            return await self._http_client.get(
                url=url,
                headers=self.headers,
            )
        except aiohttp.ClientResponseError as error:
            raise GitHubAPIError(
                f"Received {error.status} response with message: {error.message}"
            )
