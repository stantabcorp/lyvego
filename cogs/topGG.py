import asyncio
import datetime
import logging
import os

import dbl
import discord
from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""
    __slots__ = ("bot", "token", "dblpy")
    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ["DBL_TOKEN"]
        self.dblpy = dbl.DBLClient(self.bot, self.token, loop=self.bot.loop)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        while True:
            try:
                await self.dblpy.post_guild_count(shard_count=self.bot.shard_count)
            except Exception as e:
                pass
            await asyncio.sleep(900)

def setup(bot):
    bot.add_cog(TopGG(bot))
