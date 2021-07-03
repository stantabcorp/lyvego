import asyncio
import logging
import math

import discord
from discord.ext import commands
from discord.ext.commands import bot

import errors
import src as utils
import src.commands as bot_commands

logger = logging.getLogger("lyvego")


class Settings(commands.Cog):
    __slots__ = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context):
        try:
            self.bot.load_cogs(reloading=True)
            await ctx.send("Reloaded")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name="follow")
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_follow(self, ctx: commands.Context, streamer: str, *, message):
        await bot_commands.add_follow_command(self.bot, ctx, streamer, message)

    @commands.command(name="clips", aliases=["clip"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_clips(self, ctx: commands.Context, streamer: str):
        await bot_commands.add_clip_command(self.bot, ctx, streamer)

    @commands.command(name="stream")
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_streamer(self, ctx: commands.Context, streamer: str, *, message):
        await bot_commands.add_streamer_command(self.bot, ctx, streamer, message)

    @commands.command(aliases=["remove"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def remove_event(self, ctx: commands.Context, event: str, streamer: str):
        await bot_commands.remove_event_command(self.bot, ctx, event, streamer)

    # @commands.command()
    # @commands.cooldown(4, 30, commands.BucketType.user)
    # @commands.has_permissions(administrator=True)
    # @commands.guild_only()
    # async def purge(self, ctx):
    #     def is_me(user):
    #         return ctx.me == user.author
    #
    #     deleted = await ctx.channel.purge(check=is_me)
    #     await ctx.message.delete()



    @commands.command(aliases=["topclips", "tc"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.guild_only()
    async def topclip(self, ctx: commands.Context, streamer: str, amount=5):
        await bot_commands.topclips_command(bot, ctx, streamer, amount)

    @commands.command(aliases=["locales"])
    @commands.is_owner()
    async def reload_locales(self, ctx):
        try:
            self.bot.load_locales()
        except Exception as e:
            return await ctx.send(f"Cannot load locales : {e}")

        await ctx.send(f"Locales loaded for those languages : **{' '.join(list(self.bot.locales.keys()))}**")


def setup(bot):
    bot.add_cog(Settings(bot))
