from __future__ import annotations

import asyncio
from typing import List, Optional, Tuple

import aiohttp

from src.api import fetch_code_info


async def scan_codes_async(
    start: int,
    end: int,
    concurrency: int = 64,
    output_path: Optional[str] = None,
) -> List[Tuple[int, str]]:
    sem = asyncio.Semaphore(concurrency)
    results: List[Tuple[int, str]] = []
    lock = asyncio.Lock()

    async def worker(session: aiohttp.ClientSession, code: int):
        async with sem:
            ok, email = await fetch_code_info(session, code)
            if ok and email:
                async with lock:
                    results.append((code, str(email)))

    connector = aiohttp.TCPConnector(limit=concurrency * 2, ssl=False)
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [asyncio.create_task(worker(session, code)) for code in range(start, end)]
        for i in range(0, len(tasks), 500):
            await asyncio.gather(*tasks[i : i + 500])
    return results
