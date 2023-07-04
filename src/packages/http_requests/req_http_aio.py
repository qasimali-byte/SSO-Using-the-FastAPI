import aiohttp
import json
async def http_post(url: str, email:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url= url, json={'email': email}) as response:
                return await response.json(), response.status
    except:
        return {'code':404},404
    
    
async def http_post_dr_iq(url: str, payload: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=payload) as response:
                response_text = await response.text()
                return json.loads(response_text), response.status
    except aiohttp.ClientError as e:
        return str(e), None