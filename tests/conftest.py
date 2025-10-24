from pathlib import Path
from typing import Callable, Type

import pytest
from _pytest.fixtures import SubRequest  # NOTE: Deprecated
from pydantic import BaseModel, HttpUrl

from rely.core.models.repo_identifier import RepoIdentifier


type ModelLoaderFunction = Callable[[Type[BaseModel], Path], BaseModel]


@pytest.fixture
def load_model_from_file() -> ModelLoaderFunction:
    """Factory fixture to load Pydantic model from JSON file."""

    def _load_model_from_file(
        model_class: Type[BaseModel], file_path: Path
    ) -> BaseModel:
        file_content = file_path.read_text()

        return model_class.model_validate_json(file_content)

    return _load_model_from_file


@pytest.fixture
def local_test_dir(request: SubRequest) -> Path:
    """Get path of current testing directory."""

    return Path(request.node.path).parent


@pytest.fixture
def repo_identifier() -> RepoIdentifier:
    """Fixture to create RepoIdentifier instance."""

    return RepoIdentifier(url=HttpUrl("https://github.com/1cph93/rely"))
