from unittest import mock
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from rely.clients.github_api_client import GitHubAPIClient
from rely.core.models.repo_identifier import RepoIdentifier
from rely.core.models.repo_context import RepoContext, create_repo_context
from rely.clients.models.full_repository import FullRepository
from rely.clients.models.content_tree_list import ContentTreeList
from tests.conftest import ModelLoaderFunction


@pytest.fixture
def mock_github_api_client(
    mocker: MockerFixture,
    local_test_dir: Path,
    load_model_from_file: ModelLoaderFunction,
) -> GitHubAPIClient:
    """Fixture to create a mock GitHubAPIClient."""

    full_repository = load_model_from_file(
        FullRepository, local_test_dir / "fixtures" / "full_repository.json"
    )
    content_tree_list = load_model_from_file(
        ContentTreeList, local_test_dir / "fixtures" / "content_tree_list.json"
    )
    mocker.patch.object(
        GitHubAPIClient, "get_repo", mock.AsyncMock(return_value=full_repository)
    )
    mocker.patch.object(
        GitHubAPIClient,
        "get_repo_contents",
        mock.AsyncMock(return_value=content_tree_list),
    )

    return GitHubAPIClient(http_client=mock.AsyncMock(), personal_access_token="test")


def test_instantiate_repo_context(
    local_test_dir: Path,
    repo_identifier: RepoIdentifier,
    load_model_from_file: ModelLoaderFunction,
) -> None:
    """Ensure that we can instantiate a RepoContext."""

    full_repository = load_model_from_file(
        FullRepository, local_test_dir / "fixtures" / "full_repository.json"
    )
    content_tree_list = load_model_from_file(
        ContentTreeList, local_test_dir / "fixtures" / "content_tree_list.json"
    )

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
