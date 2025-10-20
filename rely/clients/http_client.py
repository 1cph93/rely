from typing import Mapping, Any

import aiohttp


class HTTPClient:
    # TODO: Fix Any return type
    async def get(
        self,
        *,
        url: str,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Perform an HTTP GET request."""
        # TODO: Add error handling
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
