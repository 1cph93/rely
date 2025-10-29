import json
from unittest import mock
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable

import pytest
from pytest_mock import MockerFixture

from rely.clients.http_client import HTTPClient
from rely.clients.github_api_client import GitHubAPIClient
from rely.core.models.repo_identifier import RepoIdentifier


@pytest.fixture
def get_repo_response(local_test_dir: Path) -> Any:
    """Fixture to create mock get_repo response dict."""

    response_path = local_test_dir / "fixtures" / "get_repo_response.json"

    return json.loads(response_path.read_text())


@pytest.fixture
def get_repo_contents_response(local_test_dir: Path) -> Any:
    """Fixture to create mock get_repo_contents response dict."""

    response_path = local_test_dir / "fixtures" / "get_repo_contents_response.json"

    return json.loads(response_path.read_text())


@pytest.fixture
def mock_get_with_response() -> Callable[[MockerFixture, Any], mock.AsyncMock]:
    """Factory fixture to mock aiohttp.ClientSession.get with a specific response."""

    def _mock_get(mocker: MockerFixture, mock_response_dict: Any) -> mock.AsyncMock:
        mock_return_value = mock.AsyncMock()
        mock_return_value.__aenter__.return_value.json.return_value = mock_response_dict

        return mocker.patch(
            "aiohttp.ClientSession.get",
            return_value=mock_return_value,
        )

    return _mock_get


@pytest.mark.asyncio
async def test_github_api_client_get_repo(
    mocker: MockerFixture,
    mock_get_with_response: Callable[[MockerFixture, Any], mock.AsyncMock],
    repo_identifier: RepoIdentifier,
    get_repo_response: Any,
) -> None:
    """Ensure that GitHubAPIClient.get_repo performs the correct calls."""

    test_personal_access_token = "test"

    m = mock_get_with_response(mocker, get_repo_response)

    async with HTTPClient() as http_client:
        github_api_client = GitHubAPIClient(http_client, test_personal_access_token)
        full_repository = await github_api_client.get_repo(repo_identifier)

    expected_url = f"{GitHubAPIClient.API_BASE_URL}/repos/{repo_identifier.repo_owner}/{repo_identifier.repo_name}"
    expected_headers = MappingProxyType(
        {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer test",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )

    m.assert_called_once_with(expected_url, headers=expected_headers)
    assert full_repository.name == "rely"


@pytest.mark.asyncio
async def test_github_api_client_get_repo_contents(
    mocker: MockerFixture,
    mock_get_with_response: Callable[[MockerFixture, Any], mock.AsyncMock],
    repo_identifier: RepoIdentifier,
    get_repo_contents_response: Any,
) -> None:
    """Ensure that GitHubAPIClient.get_repo_contents performs the correct calls."""

    test_personal_access_token = "test"
    test_contents_url = "https://test_contents_url.com"

    m = mock_get_with_response(mocker, get_repo_contents_response)

    async with HTTPClient() as http_client:
        github_api_client = GitHubAPIClient(http_client, test_personal_access_token)
        content_tree_list = await github_api_client.get_repo_contents(test_contents_url)

    expected_headers = MappingProxyType(
        {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer test",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )

    m.assert_called_once_with(test_contents_url, headers=expected_headers)
    assert len(content_tree_list.content_tree_list) == 15
