import datetime as dt
import os
import functools

from aiohttp import ClientSession
from discord.ext import commands

from src.constants import AUTHORIZATION


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
        return resp

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

    async def top_clips(self, session: ClientSession, streamer: str, parameters: str=""):
        resp = await session.request(
            method="GET",
            url=f"{self.api_root}clips?streamer={streamer}{parameters}",
            headers={"Authorization": AUTHORIZATION}
        )
        if resp.status >= 200 and resp.status <= 299:
            return await resp.json()
        return None
