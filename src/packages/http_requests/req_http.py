import asyncio

import requests

def http_get_sync(url: str):
    response = requests.get(url)
    return response.json()


async def http_get(url: str):
    return await asyncio.to_thread(http_get_sync, url)