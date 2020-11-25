import datetime as dt

from aiohttp import ClientSession
from discord.ext import commands

from src.constants import API_ROOT, AUTHORIZATION


def dctt():
    """
    Return discord timestamp
    """
    return dt.datetime.utcnow()

async def post_streamer(ctx: commands.Context, session: ClientSession, **kwargs):
    """
    POST - JSON settings for this guild
    """
    resp = await session.request(
        method="POST",
        url=f"{API_ROOT}settings/{ctx.guild.id}",
        headers={"Authorization": AUTHORIZATION},
        **kwargs
    )
    return resp

async def get_streamer(ctx: commands.Context, session: ClientSession):
    """
    GET - JSON settings for this guild
    """
    resp = await session.request(
        method="GET",
        url=f"{API_ROOT}settings/{ctx.guild.id}",
        headers={"Authorization": AUTHORIZATION}
    )
    if resp.status >= 200 and resp.status <= 299:
        return await resp.json()
    return None

async def top_clips(session: ClientSession, streamer: str, parameters: str=""):
    resp = await session.request(
        method="GET",
        url=f"{API_ROOT}clips?streamer={streamer}{parameters}",
        headers={"Authorization": AUTHORIZATION}
    )
    if resp.status >= 200 and resp.status <= 299:
        return await resp.json()
    return None
