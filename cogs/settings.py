import asyncio
import logging

import discord
from discord.ext import commands

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

def setup(bot):
    bot.add_cog(Settings(bot))
