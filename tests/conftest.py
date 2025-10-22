from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest  # NOTE: Deprecated
from pydantic import HttpUrl

from rely.core.models.repo_identifier import RepoIdentifier
from rely.core.models.repo_context import RepoContext
from rely.clients.models.full_repository import FullRepository
from rely.clients.models.content_tree_list import ContentTreeList


@pytest.fixture
def local_test_dir(request: SubRequest) -> Path:
    """Get the path of the current testing directory."""

    return Path(request.node.fspath).parent


@pytest.fixture
def repo_identifier() -> RepoIdentifier:
    """Fixture to create a RepoIdentifier."""

    return RepoIdentifier(url=HttpUrl("https://github.com/1cph93/rely"))


@pytest.fixture
def full_repository(local_test_dir: Path) -> FullRepository:
    """Fixture to create a FullRepository.  Loads content from a local JSON file."""

    file_path = local_test_dir / "full_repository.json"

    with open(file_path.resolve(), "r") as in_file:
        file_content = in_file.read()
        return FullRepository.model_validate_json(file_content)


@pytest.fixture
def content_tree_list(local_test_dir: Path) -> ContentTreeList:
    """Fixture to create a ContentTreeList.  Loads content from a local JSON file."""

    file_path = local_test_dir / "content_tree_list.json"

    with open(file_path.resolve(), "r") as in_file:
        file_content = in_file.read()
        return ContentTreeList.model_validate_json(file_content)


@pytest.fixture
def repo_context(
    repo_identifier: RepoIdentifier,
    full_repository: FullRepository,
    content_tree_list: ContentTreeList,
):
    return RepoContext(
        repo_identifier=repo_identifier,
        full_repository=full_repository,
        content_tree_list=content_tree_list,
    )
