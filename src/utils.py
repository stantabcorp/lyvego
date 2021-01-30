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


async def get_guild_settings(ctx: commands.Context, session: ClientSession):
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


async def top_clips(session: ClientSession, streamer: str, parameters: str = ""):
    resp = await session.request(
        method="GET",
        url=f"{API_ROOT}clips?streamer={streamer}{parameters}",
        headers={"Authorization": AUTHORIZATION}
    )
    if resp.status >= 200 and resp.status <= 299:
        return await resp.json()
    return None


def get_data_from_uuid(dataset: list, streamer: str, event: str) -> list:
    streamer = streamer.lower()
    ret = []
    for data in dataset:
        if data["type"] == event and data["details"]["username"].lower() == streamer:
            ret.append(data)
    return ret


async def remove_user_event(ctx: commands.Context, session: ClientSession, event: str, streamer: str):
    guild_settings = await get_guild_settings(ctx, session)
    event = {
        "stream": "live_announcement",
        "follow": "follow_announcement",
        "clips": "clip_announcement",
        "clip": "clip_announcement"
    }[event.lower()]
    data_segments = get_data_from_uuid(guild_settings, streamer, event)
    for segment in data_segments:
        resp = await session.request(
            method="POST",
            url=f"{API_ROOT}settings/{ctx.guild.id}",
            headers={"Authorization": AUTHORIZATION},
            json=[
                {
                    "channel_id": None,
                    "uuid": segment["uuid"],
                    "type": segment["type"]
                }
            ]
        )
    return resp
