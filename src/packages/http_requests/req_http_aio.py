import aiohttp

async def http_post(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url= url, json={'email':'umair@gmail.com'}) as response:
            return await response.json(), response.status