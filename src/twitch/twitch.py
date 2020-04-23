from aiohttp import ClientSession
import asyncio


class FetchError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


async def fetch(url: str, session: ClientSession, **kwargs):
    resp = await session.request(
        method="GET",
        url=url,
        **kwargs
    )
    try:
        if resp.status >= 200 and resp.status <= 299:
            data = await resp.json()
        else:
            return None
    except Exception as e:
        return None

    return data

async def get_clip(url: str, session: ClientSession):
    session = ClientSession()
    url = "https://www.google.com/"
    tasks = []
    for i in range(15):
        tasks.append(fetch(
            url=url, session=session
        ))
    print(tasks)
    await asyncio.gather(*tasks)