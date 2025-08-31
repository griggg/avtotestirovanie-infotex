import time
import httpx
import asyncio
from typing import List
from stats import HostResult, HttpPingStats

class HttpPing:
    def __init__(self, stats_collector: HttpPingStats):
        self.stats_collector = stats_collector

    async def _query(self, client: httpx.AsyncClient, url: str) -> HostResult:
        try:
            start = time.perf_counter()
            response = await client.get(url, timeout=10.0)
            end = time.perf_counter()
            return HostResult(url, response.status_code, end - start)
        except httpx.RequestError:
            return HostResult(url, None, 0.0)

    async def ping(self, hosts: List[str], count: int = 5):
        async with httpx.AsyncClient() as client:
            tasks = [
                self._query(client, url)
                for url in hosts
                for _ in range(count)
            ]
            results = await asyncio.gather(*tasks)
            self.stats_collector.collect(results)
