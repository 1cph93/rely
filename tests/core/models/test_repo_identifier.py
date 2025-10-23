import pytest
from pydantic import HttpUrl

from rely.core.models.repo_identifier import RepoIdentifier


def test_create_repo_identifier_with_valid_host() -> None:
    """Ensure that a RepoIdentifier can be created with a valid host"""

    repo_identifier = RepoIdentifier(
        url=HttpUrl("https://github.com/test_repo_owner/test_repo_name")
    )

    assert repo_identifier is not None


def test_create_repo_identifier_with_invalid_host() -> None:
    """Ensure that a RepoIdentifier can't be created with an invalid host"""

    with pytest.raises(ValueError) as exception_info:
        RepoIdentifier(
            url=HttpUrl("https://test.github.com/test_repo_owner/test_repo_name")
        )

    assert "must include a GitHub domain" in str(exception_info.value)


def test_create_repo_identifier_with_valid_path() -> None:
    """Ensure that a RepoIdentifier can be created with a valid path"""

    repo_identifier = RepoIdentifier(
        url=HttpUrl("https://github.com/test_repo_owner/test_repo_name")
    )

    assert repo_identifier is not None


def test_create_repo_identifier_with_invalid_path() -> None:
    """Ensure that a RepoIdentifier can't be created with an invalid path"""

    with pytest.raises(ValueError) as exception_info:
        RepoIdentifier(url=HttpUrl("https://github.com/test_owner"))

    assert "path must follow the format OWNER/REPO" in str(exception_info.value)


def test_create_repo_identifier_with_empty_path() -> None:
    """Ensure that a RepoIdentifier can't be created with an empty path"""

    with pytest.raises(ValueError) as exception_info:
        RepoIdentifier(url=HttpUrl("https://github.com"))

    assert "path can not be empty" in str(exception_info.value)


def test_repo_identifier_get_repo_owner() -> None:
    """Ensure that a RepoIdentifier contains a repo_owner"""

    repo_identifier = RepoIdentifier(
        url=HttpUrl("https://github.com/test_repo_owner/test_repo_name")
    )

    assert repo_identifier.repo_owner == "test_repo_owner"


def test_repo_identifier_get_repo_name() -> None:
    """Ensure that a RepoIdentifier contains a repo_name"""

    repo_identifier = RepoIdentifier(
        url=HttpUrl("https://github.com/test_repo_owner/test_repo_name")
    )

    assert repo_identifier.repo_name == "test_repo_name"
