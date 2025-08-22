import asyncio
from typing import Optional, Tuple

import aiohttp
import requests


API_URL = "https://apitwo.classpoint.app/classcode/region/byclasscode?classcode={code}"


def fetch_code_info_sync(code: int) -> Tuple[bool, Optional[str]]:
    try:
        r = requests.get(API_URL.format(code=code), timeout=8)
    except Exception:
        return False, None

    if r.status_code != 200:
        return False, None

    try:
        data = r.json()
    except Exception:
        return False, None

    email = data.get("presenterEmail")
    if email:
        return True, email
    return False, None


async def fetch_code_info(session: aiohttp.ClientSession, code: int) -> Tuple[bool, Optional[str]]:
    url = API_URL.format(code=code)
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
            if resp.status != 200:
                return False, None
            try:
                data = await resp.json(content_type=None)
            except Exception:
                return False, None
            email = data.get("presenterEmail")
            if email:
                return True, email
            return False, None
    except asyncio.CancelledError:
        raise
    except Exception:
        return False, None
