from typing import Mapping, Any

import aiohttp


class HTTPClient:
    """Async HTTP client for performing requests."""

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

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
