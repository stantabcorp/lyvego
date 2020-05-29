import asyncio
import logging

import discord
from discord.ext import commands

import errors
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


    @commands.command(name="follow")
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_follow(self, ctx: commands.Context, streamer: str):
        resp = await rh.post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                "type": "follow_announcement",
                "channel_id": ctx.channel.id,
                "streamer": streamer,
                "message": self.bot.locales["en"]["message_started_following"],
                "color": self.bot.color_str,
                "update_message_on_change": False,
                "delete_message_on_change": False
                }
            ]
        )
        if resp.status in range(200, 300):

            embed = discord.Embed(
                description=self.bot.locales["en"]["description_configure_lyvego"],
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
            raise errors.StreamerNotFound(self.bot.locales["en"]["error_streamer_not_found"].format(ctx.author))

    @commands.command(name="stream")
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_streamer(self, ctx: commands.Context, streamer: str):
        resp = await rh.post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                "type": "live_announcement",
                "channel_id": ctx.channel.id,
                "streamer": streamer,
                "message": self.bot.locales["en"]["message_stream_live"],
                "color": self.bot.color_str,
                "update_message_on_change": False,
                "delete_message_on_change": False
                }
            ]
        )
        if resp.status in range(200, 300):

            embed = discord.Embed(
                description=self.bot.locales["en"]["description_configure_lyvego"],
                color=self.bot.color,
                timestamp=dctt()
            )
            embed.set_author(
                name=self.bot.locales["en"]["author_name_success_added"].format(streamer),
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
            raise errors.StreamerNotFound(self.bot.locales["en"]["error_streamer_not_found"].format(ctx.author))

    @commands.command(aliases=["clips", "c"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clip(self, ctx: commands.Context, streamer: str):
        try:
            clips = await rh.top_clips(self.bot.http_session, streamer)
            if clips == None:
                raise errors.StreamerNotFound(self.bot.locales["en"]["error_streamer_not_found"].format(ctx.author))
            clips = clips["clips"]
            if clips[0]:
                pass
        except KeyError:
            raise errors.ClipsNotFound(self.bot.locales["en"]["error_clips_not_found"].format(ctx.author))
        embed = discord.Embed(
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_author(
            name=self.bot.locales["en"]["author_name_most_viewed_clips"].format(clips[0]["streamer"]["name"]),
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
                value=self.bot.locales["en"]["field_value_view_clip"].format(clip['link'])
            )
            embed.add_field(
                name=self.bot.locales["en"]["field_name_views"],
                value=clip["views"]
            )
            embed.add_field(
                name=self.bot.locales["en"]["field_value_clipper"],
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
