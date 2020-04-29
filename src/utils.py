import datetime as dt
import os

from aiohttp import ClientSession
from discord.ext import commands

API_KEY       = os.environ["API_KEY"]
AUTHORIZATION = os.environ["AUTHORIZATION"]

def dctt():
    """
    Return discord timestamp
    """
    return dt.datetime.utcnow()

class RequestHandler:
    def __init__(self):
        self.api_root = os.environ["API_ROOT"]

    async def post_streamer(self, ctx: commands.Context, session: ClientSession, **kwargs):
        """
        POST - JSON settings for this guild
        """
        resp = await session.request(
            method="POST",
            url=f"{self.api_root}settings/{ctx.guild.id}",
            headers={"Authorization": AUTHORIZATION},
            **kwargs
        )
        if resp.status >= 200 and resp.status <= 299:
            return resp
        return None

    async def get_streamer(self, ctx: commands.Context, session: ClientSession):
        """
        GET - JSON settings for this guild
        """
        resp = await session.request(
            method="GET",
            url=f"{self.api_root}settings/{ctx.guild.id}",
            headers={"Authorization": AUTHORIZATION}
        )
        if resp.status >= 200 and resp.status <= 299:
            return await resp.json()
        return None

    async def top_clips(self, session: ClientSession, streamer: str):
        resp = await session.request(
            method="GET",
            url=f"{self.api_root}clips?streamer={streamer}",
            headers={"Authorization": AUTHORIZATION}
        )
        if resp.status >= 200 and resp.status <= 299:
            return await resp.json()
        return None
