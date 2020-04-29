import asyncio
import logging

import discord
from discord.ext import commands

from src import rh
from src.utils import dctt

logger = logging.getLogger("lyvego")


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context):
        try:
            self.bot.loader(reloading=True)
            await ctx.send("Reloaded")
        except Exception as e:
            await ctx.send(e)


    @commands.command(name="stream")
    async def add_streamer(self, ctx, streamer, channel=""):
        resp = await rh.post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                "type": "live_announcement",
                "channel_id": ctx.channel.id,
                "streamer": streamer,
                "message": "Hey {streamer} is live on {game} ! Go check him out",
                "color": self.bot.color_str,
                "update_message_on_change": False,
                "delete_message_on_change": False
                }
            ]
        )
        d = await resp.json()
        if resp is not None:

            embed = discord.Embed(
                description="You can fully configure the bot on [lyvego.com](http://lyvego.com/)",
                color=self.bot.color,
                timestamp=dctt()
            )
            embed.set_author(
                name=f"{streamer} successfully added",
                icon_url=ctx.author.avatar_url
                )
            embed.set_thumbnail(
                url=ctx.me.avatar_url
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(d)

    @commands.command()
    async def clip(self, ctx, streamer):
        clips = await rh.top_clips(self.bot.http_session, streamer)
        embed = discord.Embed(
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_author(
            name=f'{clips[0]["streamer"]["name"]} - Most viewed clips',
            url=f"https://twitch.tv/{clips[0]['streamer']['name']}",
            icon_url=clips[0]["streamer"]["avatar"]
        )
        medals = {
            1: "🥇",
            2: "🥈",
            3: "🥉",
            4: "",
            5: ""
        }
        embed.set_thumbnail(
            url=clips[0]["thumbnail"]
        )
        for i, clip in enumerate(clips, start=1):
            embed.add_field(
                name=f"{medals[i]} {clip['title']}",
                value=f"[View clip]({clip['link']})"
            )
            embed.add_field(
                name="👁️ Views",
                value=clip["views"]
            )
            embed.add_field(
                name="Clipper",
                value=clip["creator"]
            )
        await ctx.send(embed=embed)

    @commands.command(name="get")
    async def get_streamer(self, ctx):
        resp = await rh.get_streamer(
            ctx,
            self.bot.http_session
        )
        await ctx.send(resp)

def setup(bot):
    bot.add_cog(Settings(bot))
