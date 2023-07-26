# import asyncio
from socket import AF_INET
from typing import Optional

import aiohttp

# By default aiohttp uses a total 300 seconds (5min) timeout,
# it means that the whole operation should finish in 5 minutes.
CLIENT_TIMEOUT_TOTAL = 10  # 10 seconds

# limits amount of parallel connections to the same endpoint.
# The default is 0 (no limit on per host bases)
SIZE_POOL_AIOHTTP = 100


class SingletonAiohttp:
    """
    Avoids creation of multiple aiohttp sessions
    session should be created once per service (not per request)
    """

    aiohttp_client: Optional[aiohttp.ClientSession] = None
    # sem: Optional[asyncio.Semaphore] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=CLIENT_TIMEOUT_TOTAL)
            connector = aiohttp.TCPConnector(
                family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP
            )
            cls.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector
            )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None
