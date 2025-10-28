from unittest import mock

import pytest
from pytest_mock import MockerFixture

from rely.clients.http_client import HTTPClient


@pytest.fixture
def mock_get(mocker: MockerFixture) -> mock.AsyncMock:
    """Fixture to mock aiohttp.ClientSession.get."""

    return mocker.patch(
        "aiohttp.ClientSession.get", return_value=mock.AsyncMock(autospec=True)
    )


@pytest.mark.asyncio
async def test_http_client_get(
    mocker: MockerFixture,
    mock_get: mock.AsyncMock,
) -> None:
    """Ensure that HTTPClient.get performs the correct calls."""

    test_url = "https://test.com"

    async with HTTPClient() as http_client:
        await http_client.get(url=test_url)

    mock_get.assert_called_once_with(test_url, headers=None)
