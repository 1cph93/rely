from types import TracebackType
from typing import Mapping, Any, Self, Type

import aiohttp


class HTTPClient:
    """Async HTTP client for performing requests."""

    def __init__(self) -> None:
        """Initialize with reusable client session (enables connection pooling)."""

        self._client_session = aiohttp.ClientSession(raise_for_status=True)

    async def _close_client_session(self) -> None:
        """Clost client session."""

        await self._client_session.close()

    async def __aenter__(self) -> Self:
        """Return self when entering context manager."""

        return self

    async def __aexit__(
        self,
        exception_type: Type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType,
    ) -> bool | None:
        """Clost client session when exiting context manager."""

        await self._close_client_session()

        return None

    async def get(
        self,
        *,
        url: str,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """
        Perform an HTTP GET request.
        NOTE: Raises an exception if the response status code is >= 400
        """

        async with self._client_session.get(url, headers=headers) as response:
            return await response.json()
