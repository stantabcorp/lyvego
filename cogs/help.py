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
        embed = discord.Embed(
            title="test"
        )
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
