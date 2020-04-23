import asyncio
import logging

import discord
from discord.ext import commands

logger = logging.getLogger("lyvego")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx: commands.Context):
        await ctx.send(f"{ctx.author.mention} help test command")


def setup(bot):
    bot.add_cog(Help(bot))
