import asyncio
import datetime
import logging
import os

import dbl
import discord
from discord.ext import commands

logger = logging.getLogger("lyvego")


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ["DBL_TOKEN"] # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        while True:
            try:
                await self.dblpy.post_guild_count(shard_count=self.bot.shard_count)
            except Exception as e:
                logger.exception(e, exc_info=True)
            await asyncio.sleep(1800)

def setup(bot):
    bot.add_cog(TopGG(bot))
