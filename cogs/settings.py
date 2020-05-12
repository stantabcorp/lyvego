import asyncio
import logging

import discord
from discord.ext import commands

from src import rh
from src.utils import dctt
import errors

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
    async def add_streamer(self, ctx, streamer):
        resp = await rh.post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                "type": "live_announcement",
                "channel_id": ctx.channel.id,
                "streamer": streamer,
                "message": "@everyone Hey {streamer} is live on {game} ! Go check him out",
                "color": self.bot.color_str,
                "update_message_on_change": False,
                "delete_message_on_change": True
                }
            ]
        )
        if resp.status in range(200, 300):

            embed = discord.Embed(
                description=f"⚙️ You can fully configure the bot on [lyvego.com]({self.bot.lyvego_url})",
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
            try:
                await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
            except:
                pass
            await ctx.send(embed=embed)
        else:
            raise errors.StreamerNotFound("This streamer doesn't exist, please retry with a valid one.")

    @commands.command(aliases=["clips", "c"])
    async def clip(self, ctx: commands.Context, streamer: str):
        try:
            clips = await rh.top_clips(self.bot.http_session, streamer)
            print(clips, type(clips))
            if clips == None:
                raise errors.StreamerNotFound("This streamer doesn't exist, please retry with a valid one.")
            clips = clips["clips"]
            if clips[0]:
                pass
        except KeyError:
            raise errors.ClipsNotFound("Sorry but there is no clips for this streamer.")
        embed = discord.Embed(
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_author(
            name=f'{clips[0]["streamer"]["name"]} - Most viewed clips of th week',
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
                name="Views",
                value=clip["views"]
            )
            embed.add_field(
                name="Clipper",
                value=clip["creator"]
            )
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
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
