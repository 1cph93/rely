from unittest import mock

import pytest
from pytest_mock import MockerFixture

from rely.clients.http_client import HTTPClient
from rely.clients.github_api_client import GitHubAPIClient
from rely.core.models.repo_identifier import RepoIdentifier
from rely.core.models.repo_context import RepoContext, create_repo_context
from rely.clients.models.full_repository import FullRepository
from rely.clients.models.content_tree_list import ContentTreeList


@pytest.fixture
def mock_http_client(mocker: MockerFixture) -> HTTPClient:
    """Fixture to create a mock HTTPClient."""

    mocker.patch.object(HTTPClient, "get", autospec=True)

    return HTTPClient()


@pytest.fixture
def mock_github_api_client(
    mocker: MockerFixture,
    mock_http_client: HTTPClient,
    full_repository: FullRepository,
    content_tree_list: ContentTreeList,
) -> GitHubAPIClient:
    """Fixture to create a mock GitHubAPIClient."""

    mocker.patch.object(
        GitHubAPIClient, "get_repo", mock.AsyncMock(return_value=full_repository)
    )
    mocker.patch.object(
        GitHubAPIClient,
        "get_repo_contents",
        mock.AsyncMock(return_value=content_tree_list),
    )

    return GitHubAPIClient(http_client=mock_http_client, personal_access_token="test")


def test_instantiate_repo_context(
    repo_identifier: RepoIdentifier,
    content_tree_list: ContentTreeList,
    full_repository: FullRepository,
) -> None:
    """Ensure that we can instantiate a RepoContext."""

    repo_context = RepoContext(
        repo_identifier=repo_identifier,
        full_repository=full_repository,
        content_tree_list=content_tree_list,
    )

    assert repo_context is not None


@pytest.mark.asyncio
async def test_create_repo_context(
    repo_identifier: RepoIdentifier,
    mock_github_api_client: GitHubAPIClient,
) -> None:
    """Ensure that create_repo_context returns a valid RepoContext."""

    repo_context = await create_repo_context(
        repo_identifier=repo_identifier,
        github_api_client=mock_github_api_client,
    )

    assert repo_context is not None
