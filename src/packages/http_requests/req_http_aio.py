import aiohttp

async def http_post(url: str, email:str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url= url, json={'email': email}) as response:
            return await response.json(), response.status